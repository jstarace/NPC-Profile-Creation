import random

def assign_loot(layout):

    # Create Loot list
    loot_rooms = [f'L{i}' for i in range(1, 13)]
    # Shuffle list
    random.shuffle(loot_rooms)
    valid_rooms = ['None' for _ in range(1, 24)]
    x = 0
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            if layout[i][j][0] != 'entrance' and layout[i][j][0] != 'exit':
                valid_rooms[x] = i*5+j
                x += 1
    valid_rooms = random.sample(valid_rooms, len(loot_rooms))
    for pos in valid_rooms:
        row = pos // 5
        col = pos % 5
        layout[row][col][2] = loot_rooms.pop()
    return layout

