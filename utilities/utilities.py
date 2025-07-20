import csv
import json

def print_the_json(the_dict):
    print(json.dumps(the_dict, indent=4))

def gpt_adjacent_room_print(game_map, current_loc, direction_map, message):
    for direction in game_map[current_loc].directions:
        loc = current_loc + direction_map[direction]
        if game_map[loc].loot_active and game_map[loc].loot_aoe > 0:
            message = game_map[loc].print_loot_aoe(direction, message)
        if game_map[loc].encounter_active and game_map[loc].aoe > 0:
            message = game_map[loc].print_encounter_aoe(direction, message)
    return message


def single_player_adjacent_room_print(game_map, current_loc, direction_map):
    for direction in game_map[current_loc].directions:
        loc = current_loc + direction_map[direction]
        if game_map[loc].loot_active and game_map[loc].loot_aoe > 0:
            game_map[loc].print_loot_aoe(direction)
        if game_map[loc].encounter_active and game_map[loc].aoe > 0:
            game_map[loc].print_encounter_aoe(direction)

def print_populated_map(populated_map):
    counter = 0
    accumulated_lines = ""

    for room in populated_map:
        line = room.get_ids()
        accumulated_lines += line + " "
        counter += 1
        if counter % 5 == 0:
            print(accumulated_lines)
            accumulated_lines = ""

def print_base_map(the_map):
    for i in range(len(the_map)):
        for j in range(len(the_map[i])):
            # Truncate each item to no more than 4 characters
            truncated_items = [item[:4] for item in the_map[i][j]]
            # Print the truncated items in a formatted way
            formatted_group = f"[{truncated_items[0]:<6}\t{truncated_items[1]:<6}\t{truncated_items[2]:<6}]"
            print(formatted_group, end="")
        print()  # Move to the next line after each row

def load_name():
    names = []
    with open("misc_files/names.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            names.append(row[0])
    return names