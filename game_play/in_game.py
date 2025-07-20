"""
Core game engine that runs the dungeon crawler gameplay loop.

Handles player movement through the 5x5 dungeon grid, processes room interactions,
manages turn counting, and coordinates with LLM assistants for decision-making.

Key functions:
- run_game(): Main gameplay loop from entrance to exit
- find_entrance_exit(): Locates start/end positions on the map
- end_game_steps(): Saves final game state and player data

Integrates with LLM assistants (GPT-4o, Llama) and logs all
decisions for performance analysis.
"""
import random

import connections.training_day_data
import utilities.glossary

from map_visualization.ingame_map import print_ingame_map
from game_play.in_room import gpt_process_room
from classes.player import Player
from connections.insert_update_mongo import insert, replace_player, update_ids
from classes.the_assistant import GPTAssistant
from classes.llama_assistant import OllamaAssistant


def end_player_game_steps(record_id, status_message):
    connections.training_day_data.update_player_status(record_id, status_message)
    pass


def run_game(config):
#def run_game(game_map, game_ids, player_name, run, game_type = None, alignment = None, motivation = None, key = None, control = None):
    direction_map = {
        "North": -5,
        "South": 5,
        "East": 1,
        "West": -1
    }
    game_started = False
    game_map = config.populated_map
    player_name = config.player_name
    run = config.run_name
    alignment = config.alignment_key
    motivation = config.motivation_key
    key = config.key
    control = config.is_control
    llm = config.llm
    game_ids = config.game_ids
    starting_positions = config.starting_positions
    if config.training_data is not None:
        training_data = config.training_data
    else:
        training_data = 42
    turn_counter = 0

    try:
        entrance, the_exit = find_entrance_exit(game_map)
    except IndexError:
        print("Caught an IndexError: list index out of range in find_entrance_exit")
        exit(0)
        # return

    # Set Exit Path
    for room in game_map:
        if room.loc == the_exit.loc:
            continue
        else:
            room.set_exit_path(the_exit.loc)
    prev_loc = current_loc = new_loc = int(entrance.loc)

    # Create player object and insert into database
    player = Player(player_name, entrance.loc, run, alignment, motivation)
    player.set_completion("Error")
    if not control and int(training_data) == 1:
        player_id = insert(player=player)
        # Add player id to game_ids list and save game ids to database before game starts in case of crash
        try:
            game_ids.append(player_id)
        except IndexError:
            print("Caught an IndexError: list index out of range in while appending the player id")
            return
        master_game_id = insert(game_identifier=game_ids)
    elif not control and int(training_data) == 2:
        master_game_id = config.game_ids[0]
    elif control:
        master_game_id = game_ids
        player_id = game_ids[0]
        key = "Control"

    # Load the assistant for this round
    if llm == "ChatGPT4o":
        assistant = GPTAssistant(alignment, motivation, key)
    elif llm == "Llama":
        definition = None
        if motivation is not None:
            definition = utilities.glossary.get_definition(motivation)
        assistant = OllamaAssistant(alignment, motivation, key, definition)
    elif llm == "Anthropic":
        pass
    else:
        pass

    prev_direction = None
    blocked_dir = None
    opp_direction_map = {
        "North": "South",
        "South": "North",
        "East": "West",
        "West": "East"
    }

    # Do this while the player is not in the exit square
    while new_loc != int(the_exit.loc):
        print_ingame_map(game_map)
        player.room_visit(current_loc)
        if game_started:
            game_map[current_loc].set_active()
            game_map[prev_loc].set_inactive()
        try:
            if player.turns > 34:
                player.set_completion("Turns Exceeded")
                if int(training_data) == 1:
                    end_game_steps(game_map, master_game_id, player, player_id, assistant)
                else:
                    end_player_game_steps(master_game_id, "Turns Exceeded")
                return None
            else:
                # The player is only charged a turn if they move out of the room. So first step is to get the direction
                # There are some items the player can get that will impact the state of the game so they are handled
                # separately based on their codes after this step
                direction = gpt_process_room(game_map,
                                             current_loc,
                                             player,
                                             assistant,
                                             blocked_dir,
                                             player_id if control else None,
                                             control if control else None,
                                             master_game_id if int(training_data) == 2 else None
                                             )
                if direction == -42: # Send the player to the exit
                    new_loc = the_exit.loc
                elif direction == 42: # Send the player to a square next to the exit
                    print(f"Player's current location:\t {current_loc}")
                    new_loc = random.choice(get_adjacent_squares(the_exit.loc))
                    print(f"Player's new location:\t {new_loc}")
                    player.turns += 1
                elif direction == -892:
                    player.set_completion("Got Stuck")
                    if int(training_data) == 1:
                        end_game_steps(game_map, master_game_id, player, player_id, assistant, control)
                    else:
                        end_player_game_steps(master_game_id, "Got Stuck")
                    return None
                elif direction == -79:
                    player.set_completion("Invalid Action Selection")
                    if int(training_data) == 1:
                        end_game_steps(game_map, master_game_id, player, player_id, assistant, control)
                    else:
                        end_player_game_steps(master_game_id, "Invalid Action Selection")
                    return None
                elif str(direction).isdigit() and direction != '':
                    try:
                        direction_adjustment = direction_map[game_map[current_loc].directions[int(direction)]]
                        prev_direction = game_map[current_loc].directions[int(direction)]
                        blocked_dir = opp_direction_map[prev_direction]
                        new_loc = current_loc + direction_adjustment
                        player.turns += 1
                    except Exception as e:
                        print(f"Your directions are outta whack: {e}")
                        exit(0)
                else:
                    print("This shouldn't happen")
                    continue
        except Exception as e:
            print(e)
            if training_data == 1:
                end_game_steps(game_map, master_game_id, player, player_id, assistant, control)
            else:
                end_player_game_steps(master_game_id, "Error")
            return None
        if not game_started:
            game_started = True
        prev_loc = current_loc
        current_loc = new_loc
        if int(training_data) == 1:
            replace_player(player_id, player)
    player.set_completion("Complete")
    player.room_visit(the_exit.loc)
    game_map[current_loc].set_active()
    game_map[prev_loc].set_inactive()
    print_ingame_map(game_map)
    if int(training_data) == 1:
        end_game_steps(game_map, master_game_id, player, player_id, assistant, control)
    else:
        end_player_game_steps(master_game_id, "Complete")

def end_game_steps(game_map, master_id, player, player_id, assistant, control=False):
    final_map_id = insert(final_game_map=game_map)
    update_ids(master_id, final_map_id)
    replace_player(player_id, player)
    if not control:
        print_the_prints(assistant, player)

def find_entrance_exit(game_map):
    entrance = the_exit = None
    try:
        for room in game_map:
            if room.d_id == "entrance":
                entrance = room
            elif room.d_id == "exit":
                the_exit = room
    except IndexError:
        print("Caught an IndexError: list index out of range in the actual actual")
        exit(0)
    return entrance, the_exit

def print_the_prints(assistant, player):
    player.print_core_details()

def get_adjacent_squares(exit_loc):
    values = [exit_loc + 1, exit_loc - 1, exit_loc + 5, exit_loc - 5]
    if exit_loc // 5 == 0:
        values.remove(exit_loc - 5)
        if exit_loc == 0:
            values.remove(exit_loc - 1)
        elif exit_loc == 20:
            values.remove(exit_loc + 1)
    elif exit_loc // 5 == 4:
        values.remove(exit_loc + 5)
        if exit_loc == 4:
            values.remove(exit_loc - 1)
        elif exit_loc == 24:
            values.remove(exit_loc + 1)
    elif 0 < exit_loc < 4:
        values.remove(exit_loc - 5)
    elif 20 < exit_loc < 24:
        values.remove(exit_loc + 5)
    return values