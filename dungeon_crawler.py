"""
Main entry point for the NPC Profile Creation system.

This script runs a text-based dungeon crawler that tests how LLMs make decisions
when assigned D&D alignments and motivations. Creates procedural dungeons with
encounters and loot, then evaluates LLM behavior consistency.

The game supports three test modes:
- Alignment validation (9 D&D alignments)
- Motivation validation (4 motivations: Wealth, Safety, Wanderlust, Speed)
- Combined profile validation (36 alignment-motivation pairs)

Supports multiple LLMs: ChatGPT-4o, Llama, and Anthropic.
Data is stored in MongoDB for analysis.

Usage: python dungeon_crawler.py
"""

import random
import warnings
from datetime import datetime

import connections.insert_update_control_data_mongo
import utilities.training_data_json as TrainingDataJSON
import connections.training_day_data
from map_creation.room_assignment import generate_random_rooms
from map_creation.random_loot_assignment import assign_loot
from map_creation.random_encounter_assignment import assign_encounter
from map_visualization.print_map import print_map
from map_population.encounters import load_encounters
from map_population.descriptions import load_descriptions
from map_population.loot import load_loot
from game_play.in_game import run_game
from connections.insert_update_mongo import insert
from utilities.utilities import load_name
from classes.game_config import GameConfig


warnings.filterwarnings("ignore")


def main():
    names = load_name()

    alignment_map = {
        "Lawful Good": 1,
        "Lawful Neutral": 2,
        "Lawful Evil": 3,
        "Neutral Good": 4,
        "True Neutral": 5,
        "Neutral Evil": 6,
        "Chaotic Good": 7,
        "Chaotic Neutral": 8,
        "Chaotic Evil": 9
    }
    motivation_map = {
        "Wealth": 1,
        "Safety": 2,
        "Wanderlust": 3,
        "Speed": 4
    }
    key_map = {
        "LG": "Lawful Good",
        "LN": "Lawful Neutral",
        "LE": "Lawful Evil",
        "NG": "Neutral Good",
        "TN": "True Neutral",
        "NE": "Neutral Evil",
        "CG": "Chaotic Good",
        "CN": "Chaotic Neutral",
        "CE": "Chaotic Evil"
    }
    full_map = {
        "LG-Speed": 1,
        "LG-Wanderlust": 2,
        "LG-Wealth": 3,
        "LG-Safety": 4,
        "LN-Speed": 5,
        "LN-Wanderlust": 6,
        "LN-Wealth": 7,
        "LN-Safety": 8,
        "LE-Speed": 9,
        "LE-Wanderlust": 10,
        "LE-Wealth": 11,
        "LE-Safety": 12,
        "NG-Speed": 13,
        "NG-Wanderlust": 14,
        "NG-Wealth": 15,
        "NG-Safety": 16,
        "TN-Speed": 17,
        "TN-Wanderlust": 18,
        "TN-Wealth": 19,
        "TN-Safety": 20,
        "NE-Speed": 21,
        "NE-Wanderlust": 22,
        "NE-Wealth": 23,
        "NE-Safety": 24,
        "CG-Speed": 25,
        "CG-Wanderlust": 26,
        "CG-Wealth": 27,
        "CG-Safety": 28,
        "CN-Speed": 29,
        "CN-Wanderlust": 30,
        "CN-Wealth": 31,
        "CN-Safety": 32,
        "CE-Speed": 33,
        "CE-Wanderlust": 34,
        "CE-Wealth": 35,
        "CE-Safety": 36
    }
    alignment_group_map = {
        "Lawful": {
            "Lawful Good": 1,
            "Lawful Neutral": 2,
            "Lawful Evil": 3
        },
        "Neutral": {
            "Neutral Good": 4,
            "True Neutral": 5,
            "Neutral Evil": 6
        },
        "Chaotic": {
            "Chaotic Good": 7,
            "Chaotic Neutral": 8,
            "Chaotic Evil": 9
        },
        "Good": {
            "Lawful Good": 1,
            "Neutral Good": 4,
            "Chaotic Good": 7
        },
        "Neutrals": {
            "Lawful Neutral": 2,
            "True Neutral": 5,
            "Chaotic Neutral": 8
        },
        "Evil": {
            "Lawful Evil": 3,
            "Neutral Evil": 6,
            "Chaotic Evil": 9
        }
    }
    group_map = {
        "LG": {
            "LG-Speed": 1,
            "LG-Wanderlust": 2,
            "LG-Wealth": 3,
            "LG-Safety": 4
        },
        "LN": {
            "LN-Speed": 5,
            "LN-Wanderlust": 6,
            "LN-Wealth": 7,
            "LN-Safety": 8
        },
        "LE": {
            "LE-Speed": 9,
            "LE-Wanderlust": 10,
            "LE-Wealth": 11,
            "LE-Safety": 12
        },
        "NG": {
            "NG-Speed": 13,
            "NG-Wanderlust": 14,
            "NG-Wealth": 15,
            "NG-Safety": 16
        },
        "TN": {
            "TN-Speed": 17,
            "TN-Wanderlust": 18,
            "TN-Wealth": 19,
            "TN-Safety": 20
        },
        "NE": {
            "NE-Speed": 21,
            "NE-Wanderlust": 22,
            "NE-Wealth": 23,
            "NE-Safety": 24
        },
        "CG": {
            "CG-Speed": 25,
            "CG-Wanderlust": 26,
            "CG-Wealth": 27,
            "CG-Safety": 28
        },
        "CN": {
            "CN-Speed": 29,
            "CN-Wanderlust": 30,
            "CN-Wealth": 31,
            "CN-Safety": 32
        },
        "CE": {
            "CE-Speed": 33,
            "CE-Wanderlust": 34,
            "CE-Wealth": 35,
            "CE-Safety": 36
        },
        "Lawful": {
            "LG-Speed": 1,
            "LG-Wanderlust": 2,
            "LG-Wealth": 3,
            "LG-Safety": 4,
            "LN-Speed": 5,
            "LN-Wanderlust": 6,
            "LN-Wealth": 7,
            "LN-Safety": 8,
            "LE-Speed": 9,
            "LE-Wanderlust": 10,
            "LE-Wealth": 11,
            "LE-Safety": 12
        },
        "Neutral_LC": {
            "LN-Speed": 5,
            "LN-Wanderlust": 6,
            "LN-Wealth": 7,
            "TN-Speed": 17,
            "TN-Wanderlust": 18,
            "TN-Wealth": 19,
            "TN-Safety": 20,
            "CN-Speed": 29,
            "CN-Wanderlust": 30,
            "CN-Wealth": 31,
            "CN-Safety": 32
        },
        "Chaotic": {
            "CG-Speed": 25,
            "CG-Wanderlust": 26,
            "CG-Wealth": 27,
            "CG-Safety": 28,
            "CN-Speed": 29,
            "CN-Wanderlust": 30,
            "CN-Wealth": 31,
            "CN-Safety": 32,
            "CE-Speed": 33,
            "CE-Wanderlust": 34,
            "CE-Wealth": 35,
            "CE-Safety": 36
        },
        "Good": {
            "LG-Speed": 1,
            "LG-Wanderlust": 2,
            "LG-Wealth": 3,
            "LG-Safety": 4,
            "NG-Speed": 13,
            "NG-Wanderlust": 14,
            "NG-Wealth": 15,
            "NG-Safety": 16,
            "CG-Speed": 25,
            "CG-Wanderlust": 26,
            "CG-Wealth": 27,
            "CG-Safety": 28
        },
        "Neutral_GE": {
            "NG-Speed": 13,
            "NG-Wanderlust": 14,
            "NG-Wealth": 15,
            "NG-Safety": 16,
            "TN-Speed": 17,
            "TN-Wanderlust": 18,
            "TN-Wealth": 19,
            "TN-Safety": 20,
            "NE-Speed": 21,
            "NE-Wanderlust": 22,
            "NE-Wealth": 23,
            "NE-Safety": 24
        },
        "Evil": {
            "LE-Speed": 9,
            "LE-Wanderlust": 10,
            "LE-Wealth": 11,
            "LE-Safety": 12,
            "NE-Speed": 21,
            "NE-Wanderlust": 22,
            "NE-Wealth": 23,
            "NE-Safety": 24,
            "CE-Speed": 33,
            "CE-Wanderlust": 34,
            "CE-Wealth": 35,
            "CE-Safety": 36
        }
    }
    llm_map = {
        1: "ChatGPT4o",
        2: "Llama",
        3: "Anthropic"
    }

    # Prompt user to select game type
    training_data = ""
    while not training_data.isdigit() or int(training_data) not in range(1,3):
        training_data = input("Please select the game type:\n1.\tValidate player control\n2.\tGenerate Training Data\n")

    # Prompt user to select the LLM
    chosen_llm = ""
    if int(training_data) == 1:
        while not chosen_llm.isdigit() or int(chosen_llm) not in range(1, 4):
            chosen_llm = input("Please select the LLM you'd like to control your character (enter the number):\n1. ChatGPT4o\n2. Llama70B\n3. Anthropic?\n")
            if int(chosen_llm) == 2:
                print("Make sure you initiated the llama server. We used Ollama, the terminal command is 'ollama run llama3:70b'\n")
        chosen_llm = llm_map[int(chosen_llm)]
        is_control = control_check()
    else:
        chosen_llm = llm_map[2]
        is_control = False

    # Check if control data should be generated

    run_name = get_run_name(is_control)
    game_type_map = {}

    if not is_control:
        # Prompt user for the number of loops
        loops = input("Enter how many times you want to run the game:\t")
        while not loops.isdigit():
            loops = input("Please enter a valid number:\t")
        loops = int(loops)

        # Prompt user for the type of game
        if int(training_data) == 1:
            valid_inputs = ['a', 'l', 'b']
            game_type = input("What type of game (A)lignment, (L)oot, or (B)oth?\t").lower()
            while game_type not in valid_inputs: game_type = input("Invalid input. Please enter A, L, or B.\t").lower()
            # Get the sets based on the game type
            if game_type == "a":
                game_type_map = game_type_a(alignment_map, alignment_group_map)
            elif game_type == "l":
                game_type_map = game_type_l(motivation_map)
            elif game_type == "b":
                game_type_map = game_type_b(full_map, group_map)
        else:
            game_type = "b"
            game_type_map = full_map

        # Run the game
        run_the_game(loops, game_type, game_type_map, key_map, names, run_name, chosen_llm, training_data)
    else:
        # Run control game
        loops = 100
        game_type_set = ['a', 'l', 'b']
        for element in game_type_set:
            run_control_game(loops, names, element, run_name, chosen_llm)

def run_control_game(loops, names, game_type, run_name, llm):
    # Print the start time of the batch
    print_the_time("Batch Start")
    training_data = None
    starting_positions = None
    """
    Function to run the control game.
    It runs the game for a specified number of loops with predefined settings.
    """
    for i in range(0, int(loops)):
        game_ids = []
        # Select a random player name
        player_name = random.choice(names)
        # Create a player record and game IDs in the database
        player_id = connections.insert_update_control_data_mongo.create_player_record(player_name, game_type)
        game_id = connections.insert_update_control_data_mongo.create_game_ids(player_id)
        game_ids.append(player_id)
        game_ids.append(game_id)
        # Generate a random game map
        the_map = generate_random_rooms()
        populated_map, client = None, None
        # Assign encounters or loot based on the game type
        if game_type == 'a':
            alignment_key = "Lawful Good"
            motivation_key = None
            the_map = assign_encounter(the_map)
            populated_map, client = load_descriptions(the_map)
            populated_map = load_encounters(populated_map, client, alignment_key)
        elif game_type == 'l':
            alignment_key = None
            motivation_key = "Wealth"
            the_map = assign_loot(the_map)
            populated_map, client = load_descriptions(the_map)
            populated_map = load_loot(populated_map, client, motivation_key)
        elif game_type == 'b':
            alignment_key = "Lawful Good"
            motivation_key = "Wealth"
            the_map = assign_encounter(the_map)
            the_map = assign_loot(the_map)
            populated_map, client = load_descriptions(the_map)
            populated_map = load_encounters(populated_map, client, alignment_key)
            populated_map = load_loot(populated_map, client, motivation_key)
        else:
            print("This should literally never happen")
            exit(666)
        # Update the game IDs with the base and populated maps
        connections.insert_update_control_data_mongo.update_game_ids(game_id,
                                                                     "Base Map",
                                                                     connections.insert_update_control_data_mongo.upload_base_map(
                                                                         the_map))
        connections.insert_update_control_data_mongo.update_game_ids(game_id,
                                                                     "Populated Map",
                                                                     connections.insert_update_control_data_mongo.upload_populated_map(
                                                                         populated_map))
        # Print the game map
        print_map(the_map)
        # Create a game configuration object
        config = GameConfig(populated_map, game_ids, player_name, run_name, game_type, alignment_key, motivation_key, game_type, True, llm, training_data, starting_positions)
        print(f"_________________________________\n"
              f"Welcome Player\t {player_name}\n"
              f"Alignment is: \t {alignment_key}\n"
              f"Motivation is:\t {motivation_key}\n"
              f"Run {i+1} of {loops}\n"
              f"_________________________________\n")
        # Print the start time of the run
        print_the_time("Run Start")
        # Run the game
        run_game(config)
        # Print the end time of the run
        print_the_time("Run End")
    # Print the end time of the batch
    print_the_time("Batch End")

def run_the_game(loops, game_type, game_type_map, key_map, names, run_name, llm, training_data):
    # Print the start time of the batch
    print_the_time("Batch Start")

    starting_positions = None

    # Loop through the number of iterations specified by 'loops'
    for i in range(0, int(loops)):
        print(f"Batch: {i+1} of: {loops}")
        # Loop through each key in the game_type_map
        for key in game_type_map:
            # Generate a random map
            the_map = generate_random_rooms()

            # Assign encounters or loot based on the game type
            if game_type == "a":
                alignment_key = key
                motivation_key = None
                the_map = assign_encounter(the_map)
            elif game_type == "l":
                alignment_key = None
                motivation_key = key
                the_map = assign_loot(the_map)
            elif game_type == "b":
                alignment_key = key_map[key.split("-")[0]]
                motivation_key = key.split("-")[1]
                the_map = assign_encounter(the_map)
                the_map = assign_loot(the_map)
            else:
                print("Something went horribly wrong")
                exit(339)

            # Select a random player name
            player_name = random.choice(names)
            game_ids = []

            # Insert the base map into the database and its ID
            if training_data == 1:
                base_id = insert(base_map=the_map)
                game_ids.append(base_id)

            # Load descriptions into the game map
            populated_map, client = load_descriptions(the_map)

            # Load encounters or loot into the populated map based on the game type
            if game_type == "a":
                populated_map = load_encounters(populated_map, client, alignment_key)
            elif game_type == "l":
                populated_map = load_loot(populated_map, client, motivation_key)
            elif game_type == "b":
                populated_map = load_encounters(populated_map, client, alignment_key)
                populated_map = load_loot(populated_map, client, motivation_key)

            if int(training_data) == 2:
                game_record = {"map_id":None, "player_id":None}
                game_record["map_id"] = connections.training_day_data.create_map_record()
                game_record["player_id"] = connections.training_day_data.create_player_record(player_name,alignment_key, motivation_key, game_record["map_id"])
                the_id = connections.training_day_data.create_game_record(game_record)
                starting_positions = TrainingDataJSON.generate_initial_map_JSON(populated_map)
                connections.training_day_data.insert_map_data(game_record["map_id"], game_record["player_id"], starting_positions)
                game_ids.append(the_id)

            # Insert the populated map into the database and get its ID
            if int(training_data) == 1:
                pop_map_id = insert(initial_pop_map=populated_map)
                game_ids.append(pop_map_id)

            # Print the game map
            print_map(the_map)

            # Create a game configuration object
            config = GameConfig(populated_map, game_ids, player_name, run_name, game_type, alignment_key, motivation_key, key, False, llm, training_data, starting_positions)

            # Print player details
            print(f"_________________________________\n"
                  f"Welcome Player\t {player_name}\n"
                  f"Alignment is: \t {alignment_key}\n"
                  f"Motivation is:\t {motivation_key}\n"
                  f"_________________________________\n")

            # Print the start time of the run
            print_the_time("Run Start")

            # Run the game
            run_game(config)

            # Print the end time of the run
            print_the_time("Run End")

        # Print the end time of the batch

    print_the_time("Batch End")

def game_type_b(full_map, group_map):
    # Ask the user if they want to run the game with a specific alignment and motivation
    full_test = input("Would you like to run the game with a specific alignment and motivation? (y/n): ").lower()
    while full_test not in ['y', 'n']:
        # Prompt the user to enter a valid input if the input is not 'y' or 'n'
        print("Invalid input. Please enter 'y' or 'n'.")
        full_test = input("Would you like to run the game with a specific alignment and motivation? (y/n): ").lower()

    if full_test.lower() == "y":
        # If the user wants to run the game with a specific alignment and motivation
        full = input("Please enter the alignment and motivation you would like to use: ")
        while full not in full_map:
            # Prompt the user to enter a valid alignment and motivation if the input is not in full_map
            print("Invalid Input. Please enter a valid alignment and motivation")
            full = input("Please enter the alignment and motivation you would like to use: ")
        game_type_map = {full: full_map[full]}
    else:
        # Ask the user if they want to run tests on a specific group
        group_test = input("Would you like to run tests on a specific group? (y/n): ").lower()
        while group_test not in ['y', 'n']:
            # Prompt the user to enter a valid input if the input is not 'y' or 'n'
            print("Invalid input. Please enter 'y' or 'n'.")
            group_test = input("Would you like to run tests on a specific group? (y/n): ").lower()

        if group_test.lower() == "y":
            # If the user wants to run tests on a specific group
            group = input("Which group would you like to test: ")
            while group not in group_map:
                # Prompt the user to enter a valid group if the input is not in group_map
                print("Invalid input. Please enter the group... jerk")
                group = input("Which group would you like to test: ")
            game_type_map = group_map[group]
        else:
            # If the user does not want to run tests on a specific group, use the full_map
            game_type_map = full_map

    return game_type_map

def game_type_l(motivation_map):
    # Ask the user if they want to run the game with a specific motivation
    motivation_test = input("Would you like to run the game with a specific motivation? (y/n): ").lower()
    while motivation_test not in ['y', 'n']:
        # Prompt the user to enter a valid input if the input is not 'y' or 'n'
        print("Invalid input. Please enter 'y' or 'n'.")
        motivation_test = input("Would you like to run the game with a specific motivation? (y/n): ").lower()

    if motivation_test.lower() == "y":
        # If the user wants to run the game with a specific motivation
        motivation = input("Please enter the motivation you would like to use: ")
        while motivation not in motivation_map:
            # Prompt the user to enter a valid motivation if the input is not in motivation_map
            print("Invalid Input. Please enter a valid motivation")
            motivation = input("Please enter the motivation you would like to use: ")
        game_type_map = {motivation: motivation_map[motivation]}
    else:
        # If the user does not want to run the game with a specific motivation, use the entire motivation_map
        game_type_map = motivation_map

    return game_type_map

def game_type_a(alignment_map, alignment_group_map):
    # Define valid answers for yes/no questions
    valid_answers = ['y', 'n']
    group_check = ""
    specific_check = ""

    # Ask the user if they want to check a specific group of alignments
    while group_check not in valid_answers:
        group_check = input("Would you like to check a specific group of alignments? (y/n)\t")

    if group_check == 'y':
        # If the user wants to check a specific group, ask for the group name
        group = input("Enter the group you'd like to test:\nLawful == LG, LN, LE\nNeutral == NG, TN, NE\nChaotic == CG, CN, CE\n"
                      "Good == LG, NG, CG\nNeutrals == LN, TN, NE\nEvil == LE, NE, CE\nEnter here:\t")
        return alignment_group_map[group]

    # Ask the user if they want to run the game with a specific alignment
    while specific_check not in valid_answers:
        specific_check = input("Would you like to run the game with a specific alignment? (y/n)\t").lower()

    if specific_check == 'y':
        # If the user wants to run the game with a specific alignment, ask for the alignment
        alignment = input("Please enter the alignment you would like to use:\t")
        while alignment not in alignment_map:
            # Prompt the user to enter a valid alignment if the input is not in alignment_map
            print("Invalid Input. Please enter a valid alignment")
            alignment = input("Please enter the alignment you would like to use:\t")
        return {alignment: alignment_map[alignment]}
    elif group_check == 'n' and specific_check == 'n':
        # If the user does not want to check a specific group or run the game with a specific alignment, return the entire alignment_map
        return alignment_map

def get_run_name(is_control):
    name = ""
    while name == "":
        name = input("Please enter the name of the run:\t")
    if is_control:
        name = "Control_"+name
    return name.upper()

def control_check():
    the_check = ""
    while the_check.lower() not in ['y', 'n']:
        the_check = input("Do you want to generate control data (y/n)?:\t")
    if the_check == 'y':
        return True
    else:
        return False

def print_the_time(message):
    now = datetime.now()
    human_readable_time = now.strftime("%H:%M:%S")
    print(f"{message} time:\t", human_readable_time)
    print("______________________________________________\n\n")

if __name__ == '__main__':
    main()