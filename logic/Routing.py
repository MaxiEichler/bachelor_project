# This program will manage the routing of the traces
import hardware.ASA as ASA
from collections import deque, defaultdict

# Create a graph to represent the connections
graph = defaultdict(list)

# Add connections to the graph for BFS
def add_connection(node1, node2, connection_id):
    # node1, node2: e.g. "A", "B"
    # connection_id: e.g. "AB_1"
    graph[node1].append((node2, connection_id)) # from node1 to node2
    graph[node2].append((node1, connection_id)) # from node2 to node1

# create all connections
for i in range(1, 5):
    add_connection("A", "B", f"AB_{i}")
    add_connection("A", "C", f"AC_{i}")
    add_connection("A", "D", f"AD_{i}")
    add_connection("B", "D", f"BD_{i}")
    add_connection("B", "C", f"CB_{i}")
    add_connection("C", "D", f"CD_{i}")

# This function maps the desired connection to the ASA address_map
def map_connection_to_address(chip_start, chip_end, connection, start, end):
    # Map the start chip and connection to the X address index
    # chip_start: 'A', 'B', 'C' or 'D'
    # chip_end: 'A', 'B', 'C' or 'D'
    # connection: e.g. "AB_1"
    # start: e.g. "1" (Y1)
    # end: e.g. "10" (Y10)

    print(("received in map_connection_to_address:", chip_start, chip_end, connection, start, end))

    match chip_start:
        case 'A':
            address_index_start = ASA.connection_map_chip_A[connection]
            start = int(start) - 1 # BB1 --> Y0
        case 'B':
            address_index_start = ASA.connection_map_chip_B[connection]
            start = int(start) - 9 # BB9 --> Y0
        case 'C':
            address_index_start = ASA.connection_map_chip_C[connection]
            start = int(start) - 19 # BB18 --> Y0
        case 'D':
            address_index_start = ASA.connection_map_chip_D[connection]
            start = int(start) - 26 # BB25 --> Y0

    # Map the end chip and connection to the X address index
    match chip_end:
        case 'A':
            address_index_end = ASA.connection_map_chip_A[connection]
            end = int(end) - 1 # BB1 --> Y0
        case 'B':
            address_index_end = ASA.connection_map_chip_B[connection]
            end = int(end) - 9 # BB9 --> Y0
        case 'C':
            address_index_end = ASA.connection_map_chip_C[connection]
            end = int(end) - 19 # BB18 --> Y0
        case 'D':
            address_index_end = ASA.connection_map_chip_D[connection]
            end = int(end) - 26 # BB25 --> Y0

    # Create startpoint and endpoint strings for ASA.address_map
    startpoint = "Y" + str(start) + "_" + "X" + str(address_index_start)
    endpoint = "Y" + str(end) + "_" + "X" + str(address_index_end)
    return startpoint, endpoint

# Block directions
def block_connection(id):
    # id: connection id e.g. "AB_1"
    ASA.status_map[id] = 1  # Mark connection as used

# Unblock directions
def unblock_connection(id):
    # id: connection id e.g. "AB_1"
    ASA.status_map[id] = 0  # Mark connection as free

# Find shortest path with the help of BFS
def find_path(start, target):
    # start: starting node "A", "B", "C" or "D"
    # target: target node "A", "B", "C" or "D"

    queue = deque()
    queue.append((start, []))
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == target:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor, conn_id in graph[current]:
            if ASA.status_map[conn_id] == 0:  # Check if connection is free
                queue.append((neighbor, path + [(current, neighbor, conn_id)]))

    return None

def set_path(pin_start, pin_end):
    # pin_start: e.g. "1" (Y1)
    # pin_end: e.g. "10" (Y10)
    # both variables will come from the GUI

    print("Received pins:", pin_start, pin_end)

    match pin_start:
        case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8: start_chip = 'A'
        case 11 | 12 | 13 | 14 | 15 | 16 | 17 |18: start_chip = 'B'
        case 21 | 22 | 23 | 24 | 25 | 26 | 27 |28: start_chip = 'C'
        case 31 | 32 | 33 | 34 | 35 | 36 | 37 |38: start_chip = 'D'

    match pin_end:
        case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8: end_chip = 'A'
        case 11 | 12 | 13 | 14 | 15 | 16 | 17 |18: end_chip = 'B'
        case 21 | 22 | 23 | 24 | 25 | 26 | 27 |28: end_chip = 'C'
        case 31 | 32 | 33 | 34 | 35 | 36 | 37 |38: end_chip = 'D'

    path = find_path(start_chip, end_chip)  # Example: find path from A to D

    if path:
        print("Path found:")
        for step in path:
            print(step)
            start, end, connection = step
    else:
        print("No path found")

    for step in path:
        start, end, connection = step
        address_start, address_end = map_connection_to_address(start_chip, end_chip, connection, str(pin_start), str(pin_end)) # Map to ASA addresses   

        print("Address 1:", address_start)
        print("Start: ", start)
        print("Address 2:", address_end)
        print("End: ", end)

        #ASA.set_ASA(address_start, 1, start)  # Set startpoint to 1 (connected)
        #ASA.set_ASA(address_end, 1, end)      # Set endpoint to

        block_connection(connection)  # Mark connection as used in status_map
