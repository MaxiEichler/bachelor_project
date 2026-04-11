# This program will manage the routing of the traces
from hardware.ASA import set_ASA, connection_map_chip_A, connection_map_chip_B, status_map, reset_ASA
from collections import deque, defaultdict
from hardware.I2C import switch_expander


# Create a graph to represent the connections
graph = defaultdict(list)
last_connection = ""

# Add connections to the graph for BFS
def add_connection(node1, node2, connection_id):
    # node1, node2: e.g. "A", "B"
    # connection_id: e.g. "AB_1"
    graph[node1].append((node2, connection_id)) # from node1 to node2
    graph[node2].append((node1, connection_id)) # from node2 to node1

# create all connections
for i in range(1, 9):
    add_connection("A", "B", f"AB_{i}")
    add_connection("A", "A", f"AA_{i}")
    add_connection("B", "B", f"BB_{i}")

# This mapping is used to connect logic with hardware of the chip
conversion_map_A = {
    "0": 7, "1": 6, "2": 5, "3": 4,
    "4": 3, "5": 2, "6": 1, "7": 0
}

# This function maps the desired connection to the ASA address_map
def map_connection_to_address(chip_start, chip_end, connection, start, end):
    # Map the start chip and connection to the X address index
    # chip_start: "A" or "B"
    # chip_end: "A" or "B"
    # connection: e.g. "AB_1"
    # start: e.g. "1" (Y1)
    # end: e.g. "10" (Y10)

    print(("received in map_connection_to_address:", chip_start, chip_end, connection, start, end))

    # Map the start chip and connection to the X address index
    match chip_start:
        case 'A':
            address_index_start = connection_map_chip_A[connection]
            start = int(start) - 1 # BB1 --> Y0
        case 'B':
            address_index_start = connection_map_chip_B[connection]
            start = int(start) - 9 # BB9 --> Y0

    # Map the end chip and connection to the X address index
    match chip_end:
        case 'A':
            address_index_end = connection_map_chip_A[connection]
            end = int(end) - 1 # BB1 --> Y0
        case 'B':
            address_index_end = connection_map_chip_B[connection]
            end = int(end) - 9 # BB9 --> Y0

    # Create startpoint and endpoint strings for ASA.address_map
    if chip_start == "A":
        print("start", start)
        new_start = conversion_map_A[str(start)]
        print("new start: ", new_start)
        startpoint = "Y" + str(new_start) + "-" + "X" + str(address_index_start)
        new_end = conversion_map_A[str(end)]
        print("new end: ", new_end)
        endpoint = "Y" + str(new_end) + "-" + "X" + str(address_index_end)
    else:
        startpoint = "Y" + str(start) + "-" + "X" + str(address_index_start)
        endpoint = "Y" + str(end) + "-" + "X" + str(address_index_end)

    print("Mapped to ASA addresses:", startpoint, endpoint)
    return startpoint, endpoint

# Block directions
def block_connection(id):
    # id: connection id e.g. "AB_1"
    status_map[id] = 1  # Mark connection as used
    last_connection = id
    print("last connection: ", last_connection)

# Unblock directions
def unblock_connection(id):
    # id: connection id e.g. "AB_1"
    status_map[id] = 0  # Mark connection as free

# Unblock last connection
def unblock_last_connection():
    status_map[last_connection] = 0
    print("last connection unblocked: ", last_connection)

# Unblock all connections
def unblock_all_connections():
    for key in status_map.keys():
        status_map[key] = 0
    print("All connections unblocked")
    reset_ASA()  # Reset ASA to clear all connections

# Find path using BFS (Breadth First Search)
def find_path(start, target):
    queue = deque()
    # Add neighbors of the start node first to force movement
    for neighbor, conn_id in graph[start]:
        if status_map[conn_id] == 0:
            queue.append((neighbor, [(start, neighbor, conn_id)]))
    
    visited = set()
    
    while queue:
        current, path = queue.popleft()

        if current == target:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor, conn_id in graph[current]:
            if status_map[conn_id] == 0:
                queue.append((neighbor, path + [(current, neighbor, conn_id)]))

    return None

# This function sets the path on the ASA based on the start and end pins and the route type (data or power)
def set_path(pin_start, pin_end, route_type):
    # pin_start: e.g. "1" (Y1)
    # pin_end: e.g. "10" (Y10)
    # both variables will come from the GUI

    print("Received pins:", pin_start, pin_end)
    #print("route type: ", route_type)

    # set analogue switches for data or power trace
    #switch_expander(pin_start, "power")  # make sure power is off
    switch_expander(pin_start, "data")  # is always data since the signal otherwise would need to go through the op_amp
    #if route_type == "power":
    #    switch_expander(pin_end, "data")  # make sure data is off
    #    switch_expander(pin_end, "power")  # set routetype 
    #elif route_type == "data":
    #    switch_expander(pin_end, "power")  # make sure power is off
    #    switch_expander(pin_end, "data")  # set routetype

    switch_expander(pin_end, route_type)  # set routetype for endpoint
    

    # Determine start and end chip based on pin numbers
    match pin_start:
        case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 : start_chip = "A"
        case 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16: start_chip = "B"

    match pin_end:
        case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 : end_chip = "A"
        case 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16: end_chip = "B"

    print("Start chip: ", start_chip)
    print("End chip: ", end_chip)

    path = find_path(start_chip, end_chip)  # Example: find path from A to D

    # When a path is found split it into "A", "B", "AB_1"
    if path:
        print("Path found:")
        for step in path:
            print(step)
            start, end, connection = step
    else:
        print("No path found")

    # Check if start and end are on the same chip, if yes set direct connection, if not set path
    if start_chip == end_chip:
        print("Start and end are on the same chip, setting direct connection")
        start, end, connection = step
        address_start, address_end = map_connection_to_address(start_chip, end_chip, connection, str(pin_start), str(pin_end)) # Map to ASA addresses   
        #print("Set Start: ")
        print("Address 1:", address_start, type(address_start))
        print("Address 2:", address_end, type(address_end))
        print("Start: ", start, type(start))
        print("End: ", end, type(end))


        set_ASA(address_start, 1, start_chip)  # Set startpoint to 1 (connected)
        #print("Set End: ")
        set_ASA(address_end, 1, end_chip )      # Set endpoint to
        block_connection(connection)  # Mark connection as used in status_map
    else:
        for step in path:
            print("Processing step: ", step)
            start, end, connection = step
            address_start, address_end = map_connection_to_address(start_chip, end_chip, connection, str(pin_start), str(pin_end)) # Map to ASA addresses   

            #print("Address 1:", address_start)
            #print("Start: ", start)
            #print("Address 2:", address_end)
            #print("End: ", end)

            #print("Set Start: ")
            set_ASA(address_start, 1, start)  # Set startpoint to 1 (connected)
            #print("Set End: ")
            set_ASA(address_end, 1, end)      # Set endpoint to

            block_connection(connection)  # Mark connection as used in status_map

            #print("Connection blocked: ", ASA.status_map)
