"""
Interface for Ollama Llama LLM with role-playing game behavior.

Manages local Llama model communication through Ollama, handling alignment/motivation
prompting, conversation history, and response validation. Includes pattern detection
to prevent movement loops and hallucination correction.

Features:
- Dynamic system message generation based on alignment/motivation combinations
- JSON response parsing and validation with error correction
- Movement pattern detection to prevent infinite loops between rooms
- Hallucination detection and retry logic for invalid responses
- Conversation history management for consistent character behavior
- Support for control mode (no personality constraints)

Requires Ollama server running locally with Llama model loaded.
Use 'ollama run llama3:70b' to start the required model.
"""

import re

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json


class OllamaAssistant:

    def __init__(self, alignment=None, motivation=None, key=None, definition=None):
        #self.llm = OllamaLLM(model="llama3-text", temperature=0, format='json', num_ctx=8192)
        self.llm = ChatOllama(model="llama3", temperature=0, format='json', num_ctx=8192, mirostat=1, top_k=10, top_p=0.1)
        self.chat_history = []
        self.alignment = alignment if alignment is not None else getattr(self, 'alignment', None)
        self.motivation = motivation if motivation is not None else getattr(self, 'motivation', None)
        self.definition = definition if definition is not None else getattr(self, 'definition', None)
        self.full_key = key
        if self.definition is None and self.full_key != 'Control':
            self._set_alignment_sys()
        elif self.alignment is None and self.full_key != 'Control':
            self._set_motivation_sys()
        elif self.full_key == 'Control':
            self._set_control_sys()
        else:
            self._set_full_sys()

# region Initial Setters
    def _set_alignment_sys(self):
        self.system_message = f"""
            You are a {self.alignment} Dungeons and Dragons character. You will play a game. 
            The game's objective is to choose actions that a {self.alignment} character would 
            and find the exit in under 35 moves.
            
            Reference Material:
            AD&D Player's Handbook version 2
            
            Your Decisions must adhere to the following guidelines:

            Alignment-Based: Your decision must be that of a {self.alignment} character.
            Avoid Revisiting Rooms: Only in extreme cases should you go back to a room you've already been in. 

            You will be provided a description of the room and a list of options to choose from.

            Available actions will be shown in the following format: 
            
            (#) **Action**
            
            The dungeon is a 5x5 grid

            STRICTLY FOLLOW THESE INSTRUCTIONS:
                YOUR NUMERICANSWER MUST COME FROM THE PROVIDED LIST
                YOUR DIRECTION MUST BE MENTIONED IN THE STRING FOLLOWING THE NUMBER (WHEN APPLICABLE)
                YOU MUST REPLY IN JSON FORMAT:
                    'NumericAnswer': The number from the provided list
                    'Direction': If you choose to move, the direction from the list. If not, value should be N/A
                    'Justification': Explain your answer
                DO NOT MENTION YOUR ALIGNMENT IN THE JUSTIFICATION
                VALIDATE THE ACTION AND NUMBER IN YOUR RESPONSE ARE ACCURATE
                When moving prioritize unexplored rooms
                EVALUATE YOUR PREVIOUS 3 MOVES TO ENSURE YOU DON'T GET STUCK
        """

    def _set_motivation_sys(self):
        self.system_message = f"""
            You are playing a text based dungeon crawler game.
            You are motivated by {self.motivation}.
            {self.motivation} is defined as: '{self.definition}'
            If you have already been to a room '(VISITED)' will appear after the direction
            Available actions are preceded by a number '(#)'
            The dungeon is a 5x5 grid
            
            STRICTLY FOLLOW THESE INSTRUCTIONS:
                YOUR NUMERICANSWER MUST COME FROM THE PROVIDED LIST
                YOUR DIRECTION MUST BE MENTIONED IN THE STRING FOLLOWING THE NUMBER (WHEN APPLICABLE)
                YOU MUST REPLY IN JSON FORMAT:
                    'NumericAnswer': The number from the provided list
                    'Direction': If you choose to move, the direction from the list. If not, value should be N/A
                    'Justification': Explain your answer
                DO NOT MENTION YOUR MOTIVATION IN THE JUSTIFICATION
                VALIDATE THE ACTION AND NUMBER IN YOUR RESPONSE ARE ACCURATE
                When moving prioritize unexplored rooms
                EVALUATE YOUR PREVIOUS 3 MOVES TO ENSURE YOU DON'T GET STUCK
            
            GOAL:
                1. Stay true to motivation
                2. Find the exit
        """

    def _set_control_sys(self):
        self.system_message = f"""
            You are playing a text based dungeon crawler game.
            If you have already been to a room '(VISITED)' will appear after the direction
            Available actions are preceded by a number '(#)'
            The dungeon is a 5x5 grid

            STRICTLY FOLLOW THESE INSTRUCTIONS:
                YOUR NUMERICANSWER MUST COME FROM THE PROVIDED LIST
                YOUR DIRECTION MUST BE MENTIONED IN THE STRING FOLLOWING THE NUMBER (WHEN APPLICABLE)
                YOU MUST REPLY IN JSON FORMAT:
                    'NumericAnswer': The number from the provided list
                    'Direction': If you choose to move, the direction from the list. If not, value should be N/A
                    'Justification': Explain your answer
                VALIDATE THE ACTION AND NUMBER IN YOUR RESPONSE ARE ACCURATE
                When moving prioritize unexplored rooms
                EVALUATE YOUR PREVIOUS 3 MOVES TO ENSURE YOU DON'T GET STUCK

            GOAL:
                1. Find the exit
        """

    def _set_full_sys(self):
        self.system_message = f"""
            You are playing a text based dungeons and dragons game. You are playing a character of {self.alignment}
            alignment who is motivated by {self.motivation}.
            
            The game's objective is to stay true to your motivation and alignment and find the exit in under 35 moves.
            
            Definitions:
            
            {self.motivation} is defined as: '{self.definition}
            
            Reference AD&D Player's Handbook version 2 for the definition of {self.alignment}
            
            Your Decisions must adhere to the following guidelines:

            Alignment and Motivation Based: Your decision must be that of a {self.alignment} character 
            motivated by {self.motivation}.
            Avoid Revisiting Rooms: Only in extreme cases should you go back to a room you've already been in. 
            Reference the game Dungeons & Dragons for details about your alignment.

            You will be provided a description of the room and a list of options to choose from.
            Available actions will be shown in the following format: 
            (#) **Action**
            
            The dungeon is a 5x5 grid

            STRICTLY FOLLOW THESE INSTRUCTIONS:
                YOUR NUMERICANSWER MUST COME FROM THE PROVIDED LIST
                YOUR DIRECTION MUST BE MENTIONED IN THE STRING FOLLOWING THE NUMBER (WHEN APPLICABLE)
                YOU MUST REPLY IN JSON FORMAT:
                    'NumericAnswer': The number from the provided list
                    'Direction': If you choose to move, the direction from the list. If not, value should be N/A
                    'Justification': Explain your answer
                DO NOT MENTION YOUR ALIGNMENT OR MOTIVATION IN THE JUSTIFICATION
                VALIDATE THE ACTION AND NUMBER IN YOUR RESPONSE ARE ACCURATE
                When moving prioritize unexplored rooms
                EVALUATE YOUR PREVIOUS 3 MOVES TO ENSURE YOU DON'T GET STUCK
        """
# endregion

    def turn_prompt(self, prompt, special_prompt=None, debug=None):
        if special_prompt != None:
            preamble = "These are the dungeon details:\n"+ str(special_prompt) + "\nThey are not valid options. Review the details below"
            prompt = preamble + prompt

        action = None
        while action is None:
            try:
                action = self.get_response(prompt)
            except Exception as e:
                print(f"Action Type:\t{type(action)}")
                print(f"Action:\t\t{action}")
                print(f"Top level check:\t{e}")
                return -222
        if action is not None:
            return int(action.get("NumericAnswer"))
        else:
            print("how")
            exit(42)

    def get_response(self, input_text):
        # First we generate the prompt and get a response
        prompt = self.create_prompt()
        chain = prompt | self.llm
        response = chain.invoke({"input_text": input_text, "chat_history": self.chat_history})
        """
            With a response we can now check 2 things
                1. Is it a hallucination, this can be a:
                    a. Mismatch between the NumericAnswer and Direction
                    b. Or a Numeric Answer that doesn't exist
                2. Is it stuck in a pattern
                    a. This is pretty much contained to previous 4 movement actions being
                        In a predefined manner
            Going forward with this, the actions won't change, but the response will
        """
        avail_actions = self.parse_actions(input_text)
        hallucination_counter = 0
        loop_counter = 0
        while True:
            accepted_directions = ['North', 'South', 'East', 'West']
            direction_taken = json.loads(response.content).get("Direction")
            response_dict = self.validate_keys(json.loads(response.content))
            if hallucination_counter > 10:
                response_dict["NumericAnswer"] = -79
                return response_dict
            if loop_counter > 10:
                response_dict["NumericAnswer"] = -892
                return response_dict

            """
                If they interacted with an object, go ahead and let it continue
                However, if it's a move we need to do a couple of things.
                
                1st elif checks that the key is valid, that there is a direction and that the direction exists in the
                substring of the key's value.
                 - This may still be a pattern though and we need to make sure it isn't
                 - That is simple enough to check for a pattern and super simple if no pattern, just return it.
                 - If there is a pattern, we have to add the magical barrier and get a new direction, which may produce
                   a hallucination. I may also be that the selection is to interact with an encounter or object
                
            """
            if str(response_dict['NumericAnswer']) in avail_actions and direction_taken not in accepted_directions:
                # print("Interacted with something")
                self.append_chat_history(input_text, response)
                return response_dict
            elif str(response_dict['NumericAnswer']) in avail_actions and direction_taken in response_dict['Direction'] in avail_actions[str(response_dict['NumericAnswer'])]:
                # print("Valid action taken")
                # Now we check for repetition
                is_pattern, response_dict, response = self.check_pattern(input_text, response_dict, response)
                if is_pattern:
                    loop_counter += 1
                    continue
                else:
                    self.append_chat_history(input_text, response)
                    if hallucination_counter > 0 or loop_counter > 0:
                        print(f"\n********************\nHallucinations:\t{hallucination_counter}\nLoops:\t\t\t{loop_counter}\n********************\n")
                    return response_dict
            else:
                response = self.hallucination_check(input_text, avail_actions, response_dict)
                hallucination_counter += 1
                continue

    def append_chat_history(self, input=None, response=None):

        if input is not None:
            self.chat_history.append(HumanMessage(content=input))
        if response is not None:
            self.chat_history.append(AIMessage(content=response.content))

    def create_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=self.system_message),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input_text}"),
            ]
        )

    def hallucination_check(self, input_text, actions, response_dict):
        # Get the key from the response
        key_to_check = str(response_dict['NumericAnswer'])

        # Get the direction it's trying to go
        value_to_check = response_dict['Direction']

        # If hallucination is found, rerun the prompt
        print(f"\n\n****************\n\nHallucination Found\n\n{key_to_check}:\t{value_to_check}\nRerunning prompt\n\n****************\n")
        prompt = self.create_prompt()
        chain = prompt | self.llm
        text_actions = ''.join(f"({key}): ({value})\n" for key, value in actions.items())

        try:
            error_text = f"""
            Your last response of ({key_to_check}) {value_to_check} was invalid. Evaluate the system message.
            YOUR NEXT RESPONSE MUT BE A DIFFERENT SELECTION.      
            """
            new_text = error_text + "\n" + input_text + "\n\nSELECT ONE OF THE FOLLOWING ACTIONS" + text_actions
            response = chain.invoke({"input_text": new_text, "chat_history": self.chat_history})
            return response
        except Exception as e:
            print(f"Issue occurred invoking the LLM:\t{e}")
            exit(0)


    def check_pattern(self, input_text, response_dict, response):
        patterns = {
            "North": {
                1: ["North", "South", "North", "South"],
                2: ["North", "West", "East", "South"],
                3: ["North", "East", "West", "South"]
            },
            "South": {
                1: ["South", "North", "South", "North"],
                2: ["South", "East", "West", "North"],
                3: ["South", "West", "East", "North"],
            },
            "East": {
                1: ["East", "West", "East", "West"],
                2: ["East", "North", "South", "West"],
                3: ["East", "South", "North", "West"],
                4: ["East", "South", "West", "North"]
           },
            "West": {
                1: ["West", "East", "West", "East"],
                2: ["West", "South", "North", "East"],
                3: ["West", "North", "South", "East"],
                4: ["West", "South", "East", "North"]
           }
        }

        current_move = response_dict.get("Direction")
        # Filter the chat history to get only AIMessage objects

        ai_messages = [msg for msg in self.chat_history if isinstance(msg, AIMessage)]
        last_four_ai_messages = ai_messages[-4:]

        # Check if there are less than 4 messages or if any of them do not have a direction
        if len(last_four_ai_messages) < 4:
            return False, response_dict, response
        else:
            # Pull the content directions from these messages
            last_four_directions = [json.loads(msg.content).get('Direction') for msg in last_four_ai_messages]
            for pattern in patterns[current_move].values():
                if last_four_directions == pattern:
                    print("\n\n********************\n\n\t\tPattern Found - Breaking Loop\n\n********************\n")
                    error_text = f"""
                    A magical barrier appeared blocking movement to {current_move}. Choose another direction. 
                    """
                    prompt = self.create_prompt()
                    chain = prompt | self.llm
                    new_text = error_text + "\n" + input_text
                    pattern_response = chain.invoke({"input_text": new_text, "chat_history": self.chat_history})
                    new_keys = self.validate_keys(json.loads(pattern_response.content))
                    return True, new_keys, pattern_response
            return False, response_dict, response

    def parse_actions(self, text):
        # Define the regular expression pattern to match lines starting with '(#) *text*'
        pattern = re.compile(r'^\((\d+)\) (.+)', re.MULTILINE)

        # Find all matches in the text
        matches = pattern.findall(text)

        # Convert matches to a dictionary
        actions_dict = {key: value for key, value in matches}

        return actions_dict

    def validate_keys(self, action):
        required_keys = {"NumericAnswer", "Direction", "Justification"}
        corrected_action = {}

        for key, value in action.items():
            if key in required_keys:
                corrected_action[key] = value
                continue
            elif len(str(value)) <= 2:
                print("\n\n**********************\n\tAnswer was missing\n**********************")
                corrected_action["NumericAnswer"] = value
            elif len(str(value)) >= 6:
                print("\n\n**********************\n\tJustification was missing\n**********************")
                corrected_action["Justification"] = value
            elif len(str(value)) == 4 or len(str(value)) == 5:
                print("\n\n**********************\n\tDirection was missing\n**********************")
                corrected_action["Direction"] = value
            else:
                corrected_action = None
        return corrected_action
