import random
def assign_encounter(layout):
    """
    This function assigns random encounters to the rooms in the layout.

    Parameters:
    layout (list): A 2D list representing the layout of the rooms.

    Returns:
    layout (list): The updated layout with the assigned encounters.
    """

    # Create a list of encounter room IDs from 'RE1' to 'RE9'
    encounter_rooms = [f'RE{i}' for i in range(1, 10)]

    # Shuffle the list of encounter rooms to ensure randomness
    random.shuffle(encounter_rooms)

    # Initialize a list of valid rooms with 'None' placeholders
    valid_rooms = ['None' for _ in range(1, 24)]
    x = 0

    # Iterate over the layout to find valid rooms (not 'entrance' or 'exit')
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            if layout[i][j][0] != 'entrance' and layout[i][j][0] != 'exit':
                # If a valid room is found, store its position in the valid_rooms list
                valid_rooms[x] = i*5+j
                x += 1

    # Randomly select rooms from the valid_rooms list equal to the number of encounter rooms
    valid_rooms = random.sample(valid_rooms, len(encounter_rooms))

    # Assign an encounter room to each of the selected valid rooms
    for pos in valid_rooms:
        row = pos // 5
        col = pos % 5
        layout[row][col][1] = encounter_rooms.pop()

    # Return the updated layout with the assigned encounters
    return layout