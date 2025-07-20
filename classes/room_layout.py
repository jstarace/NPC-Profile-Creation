"""
Defines the BlankRoom class that represents individual dungeon rooms.

Each room handles its own state (encounters, loot, player presence), generates
prompts for LLM decision-making, manages directional movement options, and
calculates scoring for player actions.

Key features:
- Dynamic prompt generation based on room contents and adjacent rooms
- Area-of-effect (AOE) system for sensing nearby encounters/loot
- Point calculation for alignment/motivation-based decision scoring
- Special room effects (maps, time manipulation, teleportation)
- Exit pathfinding for navigation assistance

Rooms automatically determine valid movement directions based on their
position in the 5x5 grid and handle all LLM interaction formatting.
"""
import textwrap

class BlankRoom:
    DIRECTIONS_MAP = {
        0: ["East", "South"],
        4: ["West", "South"],
        20: ["North", "East"],
        24: ["North", "West"],
    }
    direction_adjustments = {
        "North": -5,
        "South": 5,
        "East": 1,
        "West": -1,
    }

    def __init__(self, grid_loc):
        self.loc = grid_loc
        self.encounter_active = False
        self.loot_active = False
        self.player_active = False
        self.visited = False
        self.directions = []
        self.loot_active = False
        self.exit_map_dir = ""
        self.exit_map_dir_loc = None
        self.loot_aoe = 0
        self.aoe = 0

        # Check if grid_loc is in the map
        if grid_loc in self.DIRECTIONS_MAP:
            self.directions.extend(self.DIRECTIONS_MAP[grid_loc])
        elif grid_loc < 4:
            self.directions.extend(["South", "East", "West"])
        elif grid_loc > 20:
            self.directions.extend(["North", "East", "West"])
        elif grid_loc % 5 == 0:
            self.directions.extend(["North", "South", "East"])
        elif grid_loc % 5 == 4:
            self.directions.extend(["North", "South", "West"])
        else:
            self.directions.extend(["North", "South", "East", "West"])

    # region Setters
    def set_description(self, desc_id, description):
        self.d_id = desc_id
        self.room = description
        if desc_id == "entrance":
            self.player_active = True
            self.visited = True
    def set_encounter_id(self, encounter_id):
        self.re_id = encounter_id
        self.encounter_id = encounter_id

    def set_encounter(self, alignment, encounter_desc, aoe, aoe_description, aoe_option_desc, options, points, aoe_points):
        self.encounter_active = True
        self.alignment = alignment
        self.encounter = encounter_desc
        self.aoe = aoe
        self.encounter_small_desc = aoe_description
        self.encounter_aoe_option_desc = aoe_option_desc
        self.encounter_options = options
        self.encounter_action_points = points
        self.encounter_aoe_points = aoe_points
    def set_loot_id(self, loot_id):
        self.l_id = loot_id
        self.loot_id = loot_id
    def set_loot(self, motivation, item, loot_desc, aoe, aoe_description, aoe_option_desc, options, points, aoe_points, special):
        self.loot_active = True
        self.motivation = motivation
        self.item_name = item
        self.loot = loot_desc
        self.loot_aoe = aoe
        self.loot_small_desc = aoe_description
        self.loot_aoe_option_desc = aoe_option_desc
        self.loot_options = options
        self.loot_action_points = points
        self.loot_aoe_points = aoe_points
        self.special = special
    # endregion

    # region Prints
    def print_ids(self):
        print(f"[{self.d_id}\t{self.re_id}\t{self.l_id}]")

    def print_ingame_description(self, game_map, blocked_dir, special_message=None):
        # Add the generic description of the room
        prompt = ""
        if special_message:
            if type(special_message) is int:
                prompt = f"You have {special_message} turns remaining\n"
            else:
                prompt += "To reach the exit go: "
                for dir in special_message:
                    prompt += f"{dir}, "
            prompt += self.room
        else:
            prompt = self.room
        adj_encounter = False
        adj_loot = False

        adj_room_information = {}
        ignore_points = 0

        # if they haven't cleared the encounter add the description
        if self.encounter_active:
            prompt += f" {self.encounter}"
            ignore_points += self.encounter_action_points[2] # The 3rd value is if a user chooses specifically to not engage.  This sentiment is captured in the prompt
        # if they haven't cleared the loot add the description
        try:
            if self.loot_active:
                prompt += f" {self.loot}"
                ignore_points += self.loot_action_points[1]# The 2nd value is if a user chooses specifically to not engage.  This sentiment is captured in the prompt
        except Exception as e:
            print(f"While getting in room description {e}")

        # Create a dictionary of all surrounding rooms and their loot or encounters.
        # The dictionary is only for use in this call, to gather data for processing and adding to the point dictionary
        # which is returned with the prompt
        try:
            for direction in self.directions:
                loc = self.loc + self.direction_adjustments[direction]
                if direction == blocked_dir:
                    pass
                else:
                    if 0 <= loc < len(game_map) and game_map[loc].encounter_active and game_map[loc].aoe > 0:
                        prompt += " " + game_map[loc].encounter_small_desc.format(direction=direction)
                        adj_room_information[direction + "_enc"] = [game_map[loc].encounter_aoe_option_desc,
                                                                    game_map[loc].encounter_aoe_points[0], # points for engaging
                                                                    game_map[loc].encounter_aoe_points[1], # points for ignoring
                                                                    direction,
                                                                    "encounter",
                                                                    game_map[loc].visited,
                                                                    game_map[loc].encounter_id
                                                                    ]
                        adj_encounter = True
                    if 0 <= loc < len(game_map) and game_map[loc].loot_active and game_map[loc].loot_aoe > 0:
                        prompt += " " + game_map[loc].loot_small_desc.format(direction=direction)
                        adj_room_information[direction + "_loot"] = [game_map[loc].loot_aoe_option_desc, # aoe description
                                                                     game_map[loc].loot_aoe_points[0], # points for engaging
                                                                     game_map[loc].loot_aoe_points[1], # points for ignoring
                                                                     direction, # direction of aoe
                                                                     "loot",
                                                                     game_map[loc].visited,
                                                                     game_map[loc].loot_id
                                                                     ]
                        adj_loot = True
        except Exception as e:
            print(f"y so difficult? {e}")

        # This builds the array of visited rooms this may replace the blocked.
        surrounding_visited_rooms = []
        for direction in self.directions:
            loc = self.loc + self.direction_adjustments[direction]
            if game_map[loc].visited:
                surrounding_visited_rooms.append(direction)

        # This is where we tally all the ignore points for all possible actions adjacent and in room.
        #if adj_room_information:
            #ignore_points += self.sum_ignore_points(adj_room_information, 2)
        # Stylize the prompt
        prompt = textwrap.fill(prompt, width=200)
        # Add in room options and build the point array
        # These are the positive actions.  Nothing about ignoring yet.
        option_counter = 1
        point_dict = {}
        prompt += "\n\nProvide the number of the action you'd like to take:"

        # The point dictionary is a pretty significant thing to detail here.  It passes along the action type, the points
        # for that action and now the id.  This is used in rating the performance of the LLM.  Ignore points are a tangled
        # mess that I'm going to need to re-evaluate, but in a nutshell, if the player decides to ignore the encounter
        # or loot in the room, we add those points to whichever action they take since there is no,

        if self.encounter_active:
            for key in self.encounter_options:
                prompt += "\n" + self.encounter_options[key].format(opt=option_counter)
                point_dict[option_counter] = ["encounter", self.encounter_action_points, option_counter, self.re_id]
                option_counter += 1
        if self.loot_active:
            prompt += "\n" + self.loot_options['1'].format(opt=option_counter)
            point_dict[option_counter] = ["loot", self.loot_action_points, option_counter, self.l_id]
            option_counter += 1
        # At this point the prompt has in room actions and points for interacting with them
        # Next we add prompts for adjacent rooms
        if adj_encounter or adj_loot:
            if self.encounter_active and self.loot_active:
                prompt += "\n\nIgnore everything in the room and:"
            elif self.encounter_active:
                prompt += "\n\nIgnore the encounter and:"
            elif self.loot_active:
                prompt += "\n\nIgnore the loot and:"

        # Here we add the actual options and the points for investigating AOE so AOE positive
        # We leverage the option dictionary built above for this
        # structure of Option dictionary
        # "Direction" of the AOE option
        # [0] AOE keyword for description
        # [1] AOE points for exploring
        # [2] AOE points for ignoring
        # [3] Direction
        # [4] Type
        # [6] ID
        # Add adjacent room / ignore points
        if adj_room_information:
            point_dict, option_counter, prompt = self.add_adjacent_room_points(adj_room_information,
                                                                               point_dict,
                                                                               option_counter,
                                                                               prompt,
                                                                               ignore_points
                                                                               )
        # Add directions
        point_dict, option_counter, temp_prompt = self.add_directions(point_dict, option_counter, ignore_points, adj_room_information, surrounding_visited_rooms) #blocked_dir,
        if temp_prompt != "":
            if self.encounter_active or self.loot_active:
                prompt += "\n\nIgnore everything and move:"
                prompt += temp_prompt
            else:
                prompt += "\nMove:"
                prompt += temp_prompt
        return prompt, point_dict

    def add_adjacent_room_points(self, adj_room_information, point_dict, option_counter, prompt, ignore):
        # structure of adj_room_information
        # "Direction" of the AOE option
        # [0] AOE keyword for description
        # [1] AOE points for likelihood to investigate
        # [2] AOE points for likelihood to ignore
        # [3] Direction
        # [4] Type
        # [5] Visited
        # [6] AOE ID
        # Add adjacent room / ignore points

        for key, value in adj_room_information.items():
            if value[5]:
                prompt += f"\n({option_counter}) You have already explored the {value[0]} to the {value[3]}. Move {value[3]} anyway.\n"
            else:
                prompt += f"\n({option_counter}) Explore the {value[0]} to the {value[3]}.\n"
            point_dict[option_counter] = [value[3], [value[1], value[2]], option_counter, ("AOE_" + value[6])]
            option_counter += 1

        return point_dict, option_counter, prompt

    def add_directions(self, point_dict, option_counter, ignore, adj_room_information, surrounding_visited_rooms):   # blocked_dir,
        prompt = ""
        blocked_dir = None
        for direction in self.directions:
            if direction == blocked_dir:
                continue
            else:
                # Check if direction is in any of the adj_room_information values at index 3
                direction_in_adj_info = any(direction == info[3] for info in adj_room_information.values())

                if direction_in_adj_info:
                    # If direction is in adj_room_information, we skip it here since it was already added
                    # during the AOE Point phase.
                    continue
                else:
                    if direction in surrounding_visited_rooms:
                        prompt += f"\n({option_counter}) {direction} (This room has been explored)"
                    else:
                        prompt += f"\n({option_counter}) {direction}"
                    if ignore == 0.0:
                        point_dict[option_counter] = [direction, [0.0, 0.0], option_counter, "Skip"]
                        # point_dict[option_counter] = [direction, 0.0, ("Skip - N/A" + " (" + str(self.loc) + ")"), 0]
                    elif ignore != 0.0:
                        point_dict[option_counter] = [direction, [0.0, 0.0], option_counter, "Ignored"]
                        # point_dict[option_counter] = [direction, 0.0 + ignore, ("Ignored - Check Details" + " (" + str(self.loc) + ")"), 0] # (0.0+ignore)] Removed ignore points for CNT-3
                    option_counter += 1
        return point_dict, option_counter, prompt
    def print_loot_aoe(self, direction, pre_json):
        pre_json['Loot description'] = f"In the distance to the {direction} {self.loot_small_desc}"
        return pre_json
    def print_encounter_aoe(self, direction, pre_json):
        pre_json['Encounter Description'] = f"{self.encounter_small_desc}{direction}"
        return pre_json
    # endregion
    def set_exit_path(self, exit_loc):
        if self.loc == exit_loc:
            self.exit_map_dir = None
            self.exit_map_dir_loc = 0
        else:
            exit_row = exit_loc//5
            room_row = self.loc//5
            if room_row > exit_row:
                self.exit_map_dir = "North"
                self.exit_map_dir_loc = -5
            elif room_row < exit_row:
                self.exit_map_dir = "South"
                self.exit_map_dir_loc = 5
            else:
                exit_column = exit_loc % 5
                room_column = self.loc % 5
                if exit_column < room_column:
                    self.exit_map_dir = "West"
                    self.exit_map_dir_loc = -1
                elif exit_column > room_column:
                    self.exit_map_dir = "East"
                    self.exit_map_dir_loc = +1


    # region In Game Methods

    def set_active_loot_enc(self, action_type, is_active):
        if action_type == "encounter":
            self.encounter_active = is_active
        elif action_type == "loot":
            self.loot_active = is_active

    def set_active(self):
        self.visited = True
        self.player_active = True

    def set_inactive(self):
        self.player_active = False

    # endregion

    # region Utilities
    def get_ids(self):
        the_ids = str([self.d_id, self.re_id, self.l_id])
        return the_ids

    def to_dict(self, pop_map):
        return {
            'General Info': {
                'Location': self.loc,
                'encounter_active': self.encounter_active,
                'loot_active': self.loot_active,
                'player_active': self.player_active,
                'visited': self.visited,
            },
            'Description': {
                'd_id': getattr(self, 'd_id', None),
                'room': getattr(self, 'room', None),
            },
            'Encounter': {
                're_id': getattr(self, 're_id', None),
                'alignment': getattr(self, 'alignment', None),
                'encounter': getattr(self, 'encounter', None),
            },
            'Loot': {
                'l_id': getattr(self, 'l_id', None),
                'motivation': getattr(self, 'motivation', None),
                'item': getattr(self, 'item', None),
                'loot': getattr(self, 'loot', None),
            },
            'Adjacent Room Descriptions': {
                'Loot': self.generate_adjacent_loot_descriptions(pop_map),
                'Encounter': self.generate_adjacent_encounter_descriptions(pop_map),
            }
        }

    def generate_adjacent_loot_descriptions(self, pop_map):
        loot_dict = {}
        for direction in self.directions:
            loc = self.loc + self.direction_adjustments[direction]
            if 0 <= loc < len(pop_map) and pop_map[loc].loot_active and pop_map[loc].loot_aoe > 0:
                loot_dict[direction] = pop_map[loc].loot_small_desc
        return loot_dict

    def generate_adjacent_encounter_descriptions(self, pop_map):
        encounter_dict = {}
        for direction in self.directions:
            loc = self.loc + self.direction_adjustments[direction]
            if 0 <= loc < len(pop_map) and pop_map[loc].encounter_active and pop_map[loc].aoe > 0:
                encounter_dict[direction] = pop_map[loc].encounter_small_desc
        return encounter_dict
    # endregion
