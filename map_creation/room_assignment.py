"""
Generates randomized 5x5 dungeon layouts with entrance and exit placement.

Creates procedural dungeons by randomly assigning room descriptions and
ensuring entrance/exit are not adjacent. Produces one of ~5.7×10^14
possible map configurations.

Key constraints:
- Entrance and exit cannot be adjacent rooms
- All 25 rooms get unique description IDs
- Random placement with collision avoidance

Returns a 3D array structure: [row][column][description_id, encounter_id, loot_id]
where encounter_id and loot_id are initially set to 'None' and populated
by separate assignment functions.
"""

import random

def generate_random_rooms():
    num_rooms = 25  # Total number of rooms in the grid

    # List of rooms including 'entrance' and 'exit', followed by 23 other rooms labeled 'D1' to 'D23'
    rooms = ['entrance', 'exit'] + [f'D{i}' for i in range(1, 24)]

    # Ensure the length of the rooms list is equal to the number of rooms
    assert len(rooms) == num_rooms

    # Define constraints for each position, specifying which positions are adjacent
    constraints = {
        0: [1, 5], 1: [0, 2, 6], 2: [1, 3, 7], 3: [2, 4, 8], 4: [3, 9],
        5: [0, 6, 10], 6: [1, 5, 7, 11], 7: [2, 6, 8, 12], 8: [3, 7, 9, 13], 9: [4, 8, 14],
        10: [5, 11, 15], 11: [6, 10, 12, 16], 12: [7, 11, 13, 17], 13: [8, 12, 14, 18], 14: [9, 13, 19],
        15: [10, 16, 20], 16: [11, 15, 17, 21], 17: [12, 16, 18, 22], 18: [13, 17, 19, 23], 19: [14, 18, 24],
        20: [15, 21], 21: [16, 20, 22], 22: [17, 21, 23], 23: [18, 22, 24], 24: [19, 23]
    }

    positions = list(range(num_rooms))  # List of all possible room positions
    entrance_pos = random.choice(positions)  # Randomly choose a position for the entrance
    invalid_exits = constraints.get(entrance_pos, [])  # Get positions that are invalid for the exit
    # Get positions that are valid for the exit (not the entrance and not adjacent to the entrance)
    valid_exits = [pos for pos in positions if pos != entrance_pos and pos not in invalid_exits]
    exit_pos = random.choice(valid_exits)  # Randomly choose a position for the exit from valid positions

    dim1, dim2, dim3 = 5 , 5, 3
    array_3d = [[['None' for _ in range(dim3)] for _ in range(dim2)] for _ in range(dim1)]

    # assign entrance to array
    array_3d[entrance_pos//dim2][entrance_pos%dim2][0] = 'entrance'

    # assign exit to array
    array_3d[exit_pos//dim2][exit_pos%dim2][0] = 'exit'

    # Get the remaining rooms (excluding 'entrance' and 'exit')
    remaining_rooms = [room for room in rooms if room not in ['entrance', 'exit']]

    # Shuffle the room descriptions
    random.shuffle(remaining_rooms)

    # Assign room descriptions to the remaining rooms
    for pos in positions:
        row = pos//dim2
        col = pos % dim2
        if array_3d[row][col][0] == 'None':
            array_3d[row][col][0] = remaining_rooms.pop()

    return array_3d  # Return the final array of rooms
