# This program will manage the routing of the traces

def route_trace(start, end):

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

    # Same ASA --> Y is for both the same
    if same_ASA:
        # Check which Y is avalaible

        