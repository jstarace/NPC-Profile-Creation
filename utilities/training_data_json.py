from utilities.utilities import print_populated_map
import textwrap
import json

def generate_player_JSON(player):
    data = {}

    return data

def generate_initial_map_JSON(populated_map):
    rooms = {}

    # Build a dictionary of all of the in room items, descriptions, and actions
    for room in populated_map:
        full_description = room.room
        encounter_actions = {}
        loot_actions = {}
        move_actions = {}
        option_counter = 1
        if room.encounter_active:
            full_description += " " + room.encounter
            encounter_actions, option_counter = get_encounter_actions(room, option_counter)
        if room.loot_active:
            full_description += " " + room.loot
            loot_actions, option_counter = get_loot_actions(room, option_counter)

        aoe_actions, option_counter, full_description = get_adjacent_information(room, populated_map, full_description, option_counter)
        if aoe_actions:
            if room.encounter_active and room.loot_active:
                aoe_actions["preamble"] = "Ignore everything in the room and:"
            elif room.encounter_active:
                aoe_actions["preamble"] = "Ignore the encounter and:"
            elif room.loot_active:
                aoe_actions["preamble"] = "Ignore the loot and:"

        for direction in room.directions:
            if not any(direction in value for value in aoe_actions.values()):
                move_actions[option_counter] = direction
                option_counter += 1

        if move_actions:
            if room.encounter_active or room.loot_active or aoe_actions:
                move_actions["preamble"] = "Ignore everything and move:"
            else:
                move_actions["preamble"] = "Move:"

        full_description += "\n\nProvide the number of the action you'd like to take:\n"

        rooms[room.loc] = {
            "is_entrance": True if room.d_id == "entrance" else False,
            "is_exit": True if room.d_id == "exit" else False,
            "has_encounter": room.encounter_active,
            "has_encounter_aoe": True if room.aoe > 0 else False,
            "has_loot": room.loot_active,
            "has_loot_aoe": True if room.loot_aoe > 0 else False,
            "room_description": full_description,
            "encounter_actions": encounter_actions,
            "loot_actions": loot_actions,
            "aoe_actions": aoe_actions,
            "move_actions": move_actions
        }

    # Build all the AOE items
    # print_the_json(rooms)
    return(rooms)

def get_encounter_actions(room, option_counter):
    data = {}
    for key in room.encounter_options:
        temp_string = room.encounter_options[key].format(opt=option_counter)
        data[option_counter] = temp_string[4:]
        option_counter += 1
    return data, option_counter

def get_loot_actions(room, option_counter):
    data = {}
    temp_string = room.loot_options['1'].format(opt=option_counter)
    data[option_counter] = temp_string[4:]
    option_counter += 1
    return data, option_counter

def get_adjacent_information(room, populated_map, description, option_counter):
    data = {}
    direction_adjustment = {
        "North": -5,
        "South": 5,
        "East": 1,
        "West": -1
    }
    for direction in room.directions:
        adj_room_number = populated_map[room.loc+direction_adjustment[direction]].loc
        if populated_map[adj_room_number].aoe > 0:
            description += " " + populated_map[adj_room_number].encounter_small_desc.format(direction=direction)
            data[option_counter] = f"Explore the {populated_map[adj_room_number].encounter_aoe_option_desc} to the {direction}"
            option_counter += 1
        if populated_map[adj_room_number].loot_aoe > 0:
            description += " " + populated_map[adj_room_number].loot_small_desc.format(direction=direction)
            data[option_counter] = f"Explore the {populated_map[adj_room_number].loot_aoe_option_desc} to the {direction}"
            option_counter += 1

    return data, option_counter, description


def print_the_json(the_dict):
    print(json.dumps(the_dict, indent=4))