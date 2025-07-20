"""
Handles individual room processing and LLM decision-making within the dungeon.

Processes player actions in each room including encounters, loot interactions,
and movement decisions. Manages the interface between the game state and LLM
assistants, handles special room effects, and tracks decision scoring.

Key functions:
- gpt_process_room(): Main room processing loop for LLM decisions
- get_player_action(): Gets and validates LLM responses with retry logic
- process_action(): Handles encounter/loot interactions and special effects
- get_room_prompt(): Generates prompts sent to LLM with available actions

Includes pattern detection to prevent LLMs from getting stuck in movement loops.
"""
import re
import time
import connections.training_day_data
from connections.insert_update_control_data_mongo import update_player_reccord

def gpt_process_room(game_map, loc, player, assistant, blocked_dir, player_id = None, is_control = None, master_id = None):
    room = game_map[loc]
    special_message = None
    turn = 0
    sub_turn=0
    if master_id is not None:
        turn = connections.training_day_data.get_turn_count(master_id)

    if is_control:
        print(f"Room:\t{room.loc}")
    same_room = False
    while True:
        if same_room:
            sub_turn += 1
        indexed_turn = create_index(turn, sub_turn)
        same_room = True
        turn_detail = {}
        if not isinstance(special_message, dict) and special_message != None:
            if isinstance(special_message, list) and special_message and special_message[0] == blocked_dir:
                # blocked_dir is the first element of special_message
                blocked_dir = None
            message, point_dict = get_room_prompt(room, game_map, blocked_dir, special_message=special_message)
            special_message = None
        else:
            message, point_dict = get_room_prompt(room, game_map, blocked_dir, special_message=None)
        if master_id is not None:
            turn_detail["Grid Location"] = loc
            turn_detail["Prompt"] = message

        # Now with the prompt (message) and points we can send it to the API
        action = get_player_action(assistant, message, point_dict, player.alignment, room.encounter_active, special_message)
        if action == -892 or action == -79:
            return action

        expected_points = 0
        actual_points = 0
        ignore_inroom_points = 0
        inroom_identifiers = []

        event = point_dict[action][3]
        if master_id is None:
            try:
                if event[0].lower() == 'r':
                    expected_points = max(point_dict[action][1])
                    actual_points = point_dict[action][1][action-1]
                elif event[0].lower() == 'l':
                    expected_points = max(point_dict[action][1])
                    actual_points = point_dict[action][1][0]
                elif event[0].lower() == 'i':
                    for item in point_dict.values():
                        if item[3][0].lower() == 'r':
                            if actual_points < item[1][2]:
                                actual_points = item[1][2]
                            if expected_points < max(item[1]):
                                expected_points = max(item[1])
                            inroom_identifiers.append(item[3])
                        elif item[3][0].lower() == 'l':
                            if actual_points < item[1][1]:
                                actual_points = item[1][1]
                            if expected_points < max(item[1]):
                                expected_points = max(item[1])
                            inroom_identifiers.append(item[3])
                elif event[0].lower() == 's':
                    actual_points = 0
                    expected_points = 0
                else:
                    actual_points = point_dict[action][1][0]
                    expected_points = max(point_dict[action][1])
                    for item in point_dict.values():
                        if item[3][0].lower() == 'r':
                            if max(item[1][:2]) > expected_points:
                                expected_points = max(item[1][:2])
                            if item[1][2] > actual_points:
                                actual_points = item[1][2]
                        elif item[3][0].lower() == 'l':
                            if item[1][0] > expected_points:
                                expected_points = item[1][0]
                            if item[1][1] > actual_points:
                                actual_points = item[1][1]
            except Exception as e:
                print(f"The error:\t{e}")
                print(f"Some data:\nPoint Dictionary:\t{point_dict}\nAction:\t\t\t{action}")
                exit(37)

            if is_control and master_id is None:
                update_player_reccord(player_id, point_dict[action][3], action, room.loc, inroom_identifiers)

            player.set_points(actual_points)
            player.set_expected_points(expected_points)
        else:
            turn_detail["Selected Action"] = action
            turn_detail["Action Type"] = determine_action_type(event)
            turn_detail["Action Text"] = extract_action_string(turn_detail["Prompt"], action)
            connections.training_day_data.update_player_turns(master_id, indexed_turn, turn_detail)
        try:
            if point_dict[action][0] in ["loot", "encounter"]:
                action_check, special_message = process_action(room, action, point_dict, player, game_map, special_message, loc)
                if action_check != 1:
                    return action_check
            else:
                return room.directions.index(point_dict[action][0])
        except Exception as e:
            print(f"Time to dive in: {e}")
            print(point_dict)
            exit(43)

def get_player_action(assistant, message, point_dict, alignment, encounter_active, special_message):
    # action = 99
    stuck_counter = 0
    retry_attempts = 3
    attempt = 0
    delay = 1
    debug = False

    for attempt in range(retry_attempts):
        try:
            while True:
                action = assistant.turn_prompt(message, special_message, debug)
                if action <= len(point_dict):
                    return action
                else:
                    print("Getting Stuck")
                    print(action)
                    print(point_dict)
                    stuck_counter += 1
                    if stuck_counter >= 3:
                        return -892
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}\nScript: in_room.py")
            if attempt + 1 == retry_attempts:
                print("Max retry attempts reached. Exiting.")
                exit(71)
            else:
                print(f"Retrying in {delay} seconds")
                print(f"Here's the action that's failing\n {e}")
                debug = True
                time.sleep(delay)

def process_action(room, action, point_dict, player, game_map, special_message, loc):
    try:
        action_check = 1
        action_type = point_dict[action][0]
        getattr(player, action_type)(getattr(room, f"{action_type}_id"))
        player.decisions(action_type, getattr(room, f"{action_type}_id"))
        room.set_active_loot_enc(action_type, False)
        if action_type == "loot" and room.special:
            action_check, special_message = handle_special_room(room, player, game_map, special_message, loc)
        return action_check, special_message
    except Exception as e:
        print(f"Error processing action: {e}\nAction Type is {action_type}")
        exit(92)

def handle_special_room(room, player, game_map, special_message, loc):
    action_check = 1
    if room.special:
        if room.special == "end_game":  # Teleport to end, do not collect $200
            action_check = -42
        elif room.special == "ingame_map":  # Map of Dungeon
            special_message = {}
            for current_room in game_map:
                if current_room.visited:
                    special_message[current_room.loc] = {
                        "Had Loot": current_room.l_id != "None",
                        "Had Encounter": current_room.re_id != "None",
                        "Connecting Room": current_room.directions,
                        "Is entrance": current_room.d_id == "entrance",
                        "Current Location": current_room.player_active
                    }
        elif room.special == "bell":  # Bell of turns
            special_message = 35 - player.turns
        elif room.special == "reset":  # Big red button
            player.turns = 0
            for current_room in game_map:
                if current_room.re_id != "None":
                    current_room.encounter_active = True
                if current_room.l_id != "None" and current_room.l_id != room.l_id:
                    current_room.loot_active = True
                current_room.visited = False
        elif room.special == "exit_map":  # exit map?
            special_message = build_exit_path(game_map, loc)
        elif room.special == "next_to_exit":  # Hidden path
            action_check = 42
        elif room.special == "turn-5":  # wheel of time
            player.turns -= 5
        elif room.special == "encounter_deactivate":  # The charm
            if player.alignment:
                for cycle_room in game_map:
                    if cycle_room.re_id:
                        cycle_room.encounter_active = False
        return action_check, special_message
    else:
        special_message = None
    return action_check, special_message

def get_room_prompt(room, game_map, blocked_dir, special_message=None):
    try:
        prompt, point_dict = room.print_ingame_description(game_map, blocked_dir, special_message=special_message)
        return prompt, point_dict
    except Exception as e:
        print(f"Error while generating the room prompt: {e}")
        print("Figure out a retry")
        exit(42)

def build_exit_path(game_map, loc, exit_directions=None):
    if exit_directions is None:
        exit_directions = []

    # Base case: If exit_map_dir_loc is None, stop recursion
    if game_map[loc].exit_map_dir_loc is None:
        return exit_directions
    else:
        # Add the current direction to the path if it exists
        dir = game_map[loc].exit_map_dir
        if dir:
            exit_directions.append(dir)

        # Recurse with the next location
        next_loc = loc + game_map[loc].exit_map_dir_loc
        return build_exit_path(game_map, next_loc, exit_directions)

def extract_action_string(prompt, action):
    pattern = rf'\({action}\)(.*?)(?=\(|$)'
    match = re.search(pattern, prompt, re.DOTALL)
    if match:
        return match.group(1).strip().split('\n')[0]
    else:
        return None

def determine_action_type(code):
    if code[0].lower() == 'r':
        return "interact with encounter"
    elif code[0].lower() == 'l':
        return "interact with loot"
    elif code[0].lower() == 'i':
        return "ignored loot or encounter"
    elif code[0].lower() == 's':
        return "move"
    else:
        return "AOE interaction"

def create_index(num, dec):
    temp_num = str(num)
    temp_dec = str(dec)
    return temp_num + "-" + temp_dec