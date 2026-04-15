# This function formates the coordinates to the connection point

# Map which converts the x-coordinates to the connection point number
connection_map_x = {
    "50": 1, "70": 2, "90": 3, "110": 4, "130": 5, "150": 6, "170": 7, "190": 8,            # Chip A
    "210": 9, "230": 10, "250": 11, "270": 12, "290": 13, "310": 14, "330": 15, "350": 16   # Chip B
}

def process_coordinates(x1, x2):
    # x1: 50, 70, 90, ...
    # x2: 50, 70, 90, ...

    #print("Received coordinates:", x1, x2)

    # Convert the x-coordinates to connection points using the mapping
    connection_point_1 = connection_map_x[x1]
    connection_point_2 = connection_map_x[x2]
    
    #print("Connection Point 1:", connection_point_1, "Connection Point 2:", connection_point_2)

    return connection_point_1, connection_point_2

