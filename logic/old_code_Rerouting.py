from collections import deque, defaultdict

class Network:
    def __init__(self):
        # adjacency list: node -> list of (neighbor, connection_id)
        self.graph = defaultdict(list)
        # connection status: connection_id -> True (blocked) / False (free)
        self.blocked = {}

    def add_connection(self, node1, node2, connection_id):
        self.graph[node1].append((node2, connection_id))
        self.graph[node2].append((node1, connection_id))
        self.blocked[connection_id] = False

    def block_connection(self, connection_id):
        self.blocked[connection_id] = True

    def unblock_connection(self, connection_id):
        self.blocked[connection_id] = False

    def find_path(self, start, target):
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

            for neighbor, conn_id in self.graph[current]:
                if not self.blocked[conn_id]:
                    queue.append((neighbor, path + [(current, neighbor, conn_id)]))

        return None



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def check_same_chip(start, end):

    # Check if on the same ASA
    match start:
        case 1-8: start_chip = 'A'
        case 9-16: start_chip = 'B'
        case 18-25: start_chip = 'C'
        case 26-34: start_chip = 'D'

    match end:
        case 1-8: end_chip = 'A'
        case 9-16: end_chip = 'B'
        case 18-25: end_chip = 'C'
        case 26-34: end_chip = 'D'

    if start_chip == end_chip:
        same_ASA = True
    else:
        same_ASA = False

# This function returns the first free connection for a given ASA chip
def find_free_connection(chip):
    for key, value in ASA.status_map.items():
        pair = key.split("_")[0]   # "AB" from "AB_1"
        if chip in pair and value == 0: # 0 means free
            return key
        else:
            return "No direct path available"
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!