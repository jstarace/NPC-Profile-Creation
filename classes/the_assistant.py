"""
Interface for OpenAI GPT-4o assistants with role-playing game behavior.

Manages communication with OpenAI's API using pre-configured assistants for
each D&D alignment, motivation, and combined profile. Handles token limits,
conversation thread management, and response validation.

Features:
- 49 pre-configured OpenAI assistants (9 alignments + 4 motivations + 36 combinations + control)
- Automatic token counting and thread pruning to stay within API limits
- Retry logic with rate limiting and error handling
- JSON response parsing and validation
- Thread history management for consistent character behavior

Each assistant is pre-loaded with specific instructions for maintaining
consistent alignment/motivation-based decision making throughout gameplay.
"""
import os
import re
import json
import time
import math
from datetime import datetime
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

class GPTAssistant:
    def __init__(self, alignment=None, motivation=None, key=None):
        load_dotenv()
        self.tokenizer = tiktoken.encoding_for_model("gpt-4o")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.alignment = alignment if alignment is not None else getattr(self, 'alignment', None)
        self.motivation = motivation if motivation is not None else getattr(self, 'motivation', None)
        self.full_key = key
        self.assistants = {
            "Lawful Good": "asst_wLepzw3UEgYXM84s1negICWI",
            "Lawful Neutral": "asst_l61GHwN6eL71nM0cjZtVPKsj",
            "Lawful Evil": "asst_jhoLlXKKBJ2CjsLTnrXezURD",
            "Neutral Good": "asst_ONl7K0TLfhrsgiaV5HtSOERm",
            "True Neutral": "asst_3MLYEh0Lg6uCoxpA5vlUspwA",
            "Neutral Evil": "asst_SCzBXEMLYbQUIca3oJTy4DFd",
            "Chaotic Good": "asst_McWH2ICrbyVTPEsixybyr0cd",
            "Chaotic Neutral": "asst_rRgIW7D6mwYQsX3nl638oh32",
            "Chaotic Evil": "asst_EVuyOA99b1bHJnl4LTExOSot",
            "Wealth": "asst_R3QloXixAJO4aI69vG4pxPoJ",
            "Safety": "asst_qnAoHqgUd6DTJJKxSG09Cmtk",
            "Wanderlust": "asst_UpFDGwAZZphU2hDwcl3VXwhf",
            "Speed": "asst_IKH40h8dbrfeD08MMWPfFuXj",
            "LG-Speed": "asst_fmZCfTuTQ8plX6ezE0OUsiKQ",
            "LG-Wealth": "asst_VAu9KBBBDa6MgWSwxsRaxfte",
            "LG-Safety": "asst_ydldDouHeCRqRzTEBkddHsVA",
            "LG-Wanderlust": "asst_WSy51HRslEBVhELOtqfRFXbT",
            "LN-Speed": "asst_S6sQu3RqksVBmZEMZ86VXxaK",
            "LN-Wealth": "asst_hAZcGyGSte7isbmiAzJAQ7ES",
            "LN-Safety": "asst_5SirOHXHoI2nSD0InmxxSWmc",
            "LN-Wanderlust": "asst_BeK2KEgFjAg6x8E0CDGBIwzt",
            "LE-Speed": "asst_0OEAHdh1EEcHuYbmtgLqvc7h",
            "LE-Wealth": "asst_aB0UIdUQD8XOrAhxw7rH8T6f",
            "LE-Safety": "asst_jc5CHOQOUVGnylgbMf8F3FpV",
            "LE-Wanderlust": "asst_0lRFGmdj2ShjsHsyj65LlPkM",
            "NG-Speed": "asst_Eh8Sb6f9dGJ5VcgVYEnFkkov",
            "NG-Wealth": "asst_oRi6inVdY1SYlK3ltZGc2fiU",
            "NG-Safety": "asst_kEWQAgkbKLC2NaDH6jNIaMXT",
            "NG-Wanderlust": "asst_qSYR4b8DkAnxprvMiFxSkg4L",
            "TN-Speed": "asst_kPMpJgNiwPC8HyEkZOKsgf6H",
            "TN-Wealth": "asst_WdaVECWNfBf9djVg9wGmn1Ak",
            "TN-Safety": "asst_p3nFYMPrR9nkdQR7OmL5qUdY",
            "TN-Wanderlust": "asst_n8wILqMW7WlBUC32YA1hZH2Y",
            "NE-Speed": "asst_QviE5lInekxOaR9zTHB385Ph",
            "NE-Wealth": "asst_GZJSvr6elRZhmygeKkRPThko",
            "NE-Safety": "asst_bLc8fgZLSUqqq67Y28bx68uP",
            "NE-Wanderlust": "asst_zb6lUveUrEgbO9YyhY5EwDLr",
            "CG-Speed": "asst_R5kR3YRT3cSGcjjjLytTd3sf",
            "CG-Wealth": "asst_P2Jj1yXNiZluP4hojeqCK5Wd",
            "CG-Safety": "asst_vPTOn8Hv9vvJfJVn1wfqmpBA",
            "CG-Wanderlust": "asst_Vg8eV3QKrvyHWmoBRKyllf5S",
            "CN-Speed": "asst_ZEP1THxOKx4nNitM83lkR66h",
            "CN-Wealth": "asst_PyAAL259ApdVy73BzvgW7tqM",
            "CN-Safety": "asst_T0jnNefgWhRPcZAqUcfSTrKB",
            "CN-Wanderlust": "asst_YdmI41JrFapbMItpUsOgXmxb",
            "CE-Speed": "asst_uLQIReo7Y7iCDPMWBIDiIJEJ",
            "CE-Wealth": "asst_radTz3SXG1Eb01uzKwfRUe5k",
            "CE-Safety": "asst_jgZDl2Aqi0b7SlQ3Go9YFLsZ",
            "CE-Wanderlust": "asst_F1lrEtAZWEAdgnzf90vYOr2U",
            "Control": "asst_KkuKiaITMehI6ctawuNYP203",
        }
        self.prompt_tokens = 0
        self.response_tokens = 0
        self.total_tokens = 0
        self.load_assistant(self.full_key)
        self.running_token_count = 0
        self.rateTPM = 30000
        self.first_call = True
        self.first_time = None
        self.limit = []

    def load_assistant(self, key):
        self.assistant = self.client.beta.assistants.retrieve(self.assistants[key])
        self.create_thread()
        self.id = self.assistant.id

    def create_thread(self):
        self.thread = self.client.beta.threads.create()

    def count_tokens(self, text):
        try:
            tokens = self.tokenizer.encode(text)
            return len(tokens)
        except IndexError:
            print("Caught an IndexError: list index out of range while counting tokens")
            exit(0)
            #return 0
    def get_current_minute(self):
        current_time = datetime.now()
        minute = current_time.minute
        return minute

    def call_gpt(self):
        action_error = None
        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
        ) as stream:
            for event in stream:
                next_event = event.to_dict()
                next_data = next_event["data"]
                if "run" not in next_data["id"]:
                    if next_data["object"] == "thread.run.step":
                        if next_data["status"] == "completed":
                            self.extract_tokens(next_data["usage"])
                        elif next_data["status"] == "failed":
                            print(f"Failed event the_assistant.py line 80: {next_data}")
                            exit(120)
                    elif next_data["object"] == "error":
                        print(f"Error event: {next_data}")
                        exit(123)
                    elif 'delta' not in next_data and next_data.get("completed_at") is not None:
                        action_error = self.extract_responses(next_data)
                        if not isinstance(action_error, int):
                            print("First chance for an error: Response is not an integer.")
                            raise Exception("Response is not an integer.")
                else:
                    if next_data["failed_at"] is not None:
                        message = next_data["last_error"]["message"]
                        print(f"Error in the run: {message}")
                        wait_time = re.findall(r'Please try again in (\d+(\.\d+)?(s|ms))', message)
                        if wait_time[0][2] == 'ms':
                            action_error = float(1.0)
                        else:
                            first_element = wait_time[0][0].replace('s', '')
                            action_error = float(first_element)
        return action_error

    # removing is_inroom, I don't think it's needed, but gotta test - Removed code - is_inroom=None,
    def turn_prompt(self, prompt,  map_dict=None, debug = None):
        instructions = ""
        map_json = None
        if map_dict is not None:
            try:
                map_json = json.dumps(map_dict)
            except (TypeError, ValueError) as e:
                print(f"Error serializing map_dict to JSON: {e}")
                map_json = None
        else:
            map_json = None

        if self.full_key == "Control":
            self.alignment = None
            self.motivation = None
            instructions = (
                "You are playing a dungeon crawler game, make decisions as you will. Your response must always be in JSON format with a single key 'Action' and its value must always be an integer."
            )
        elif self.alignment is not None and self.motivation is not None:
            instructions = (
                f"Use previous threads when making a choice. You are {self.alignment} and motivated by {self.motivation}, these drive your decision making process. Your response must always be in JSON format with a single key 'Action' and its value must always be an integer."
            )
        elif self.alignment is not None and self.motivation is None:
            instructions = (
                f"Analyze the thread for previous response when making a decision. Revisit rooms as a last resort. You are {self.alignment}, this drives your purpose in the game. Your response must always be in JSON format with a single key 'Action' and its value must always be an integer. You have the necessary skills and abilities to handle all encounters"
            )
        elif self.motivation is not None and self.alignment is None:
            instructions = (
                f"Analyze the to understand your previous decisions. You are motivated by {self.motivation}. Your response must always be in JSON format with a single key 'Action' and its value must always be an integer. Refer to the assistant instructions for the definition of your motivation."
            )
        action_response = None
        # purge old messages to keep the thread clean and avoid token limit
        if self.total_tokens > 1250:
            try:
                all_messages = self.client.beta.threads.messages.list(self.thread.id)
                user_message_ids = []
                while True:
                    # Add the ids of all 'user' messages in the current page to the list
                    user_message_ids.extend([message.id for message in all_messages.data if message.role == 'user'])
                    # If there are more pages, get the next page and continue the loop
                    if all_messages.has_more:
                        all_messages = self.client.beta.threads.messages.list(self.thread.id, after=all_messages.last_id)
                    else:
                        # If there are no more pages, break the loop
                        break
                for m_id in user_message_ids[4:]:
                    self.client.beta.threads.messages.delete(message_id=m_id, thread_id=self.thread.id)
            except IndexError:
                print("Caught an IndexError: list index out of range in turn prompt line 122")
                exit(0)
        #print("Passed the token check, creating the instruction message")
        try:
            self.client.beta.threads.messages.create(
                self.thread.id,
                role="user",
                content=instructions
            )
            self.client.beta.threads.messages.create(
                self.thread.id,
                role="user",
                content=prompt
            )
        except Exception as e:
            print(f"Error creating messages on the thread {e}")
            thread_messages = self.client.beta.threads.messages.list(self.thread.id)
            print(thread_messages.data)
        if map_json is not None:
            try:
                self.client.beta.threads.messages.create(
                    self.thread.id,
                    role="user",
                    content=map_json
                )
                print("Message sent successfully")
            except Exception as e:
                print(f"Error sending message: {e}")
        while action_response is None or type(action_response) is not int:
            max_retries = 5
            retry_delay = 2
            attempt = 0
            tried_delete = False

            while attempt < max_retries:
                try:
                    action_response = self.call_gpt()
                    break
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt}: {e}\nline 224 of assitant.py")
                    if attempt < max_retries:
                        print(f"Let's wait {retry_delay} seconds before trying again")
                        time.sleep(retry_delay)
                    elif attempt == max_retries:
                        print(f"Let's wait {60} seconds before trying again")
                    else:
                        error_message = str(e)
                        match = re.search(r'\brun_\w+', error_message)
                        if match and not tried_delete:
                            print(f"Let's try deleting the run")
                            run_id = match.group(0)
                            self.client.beta.threads.runs.cancel(run_id, thread_id=self.thread.id)
                            tried_delete = True
                        else:
                            print(f"Something new here {e}")
                            action_response = -892

            # Here we check token per minute limit and sleep if necessary
            if action_response is not None and type(action_response) is float:
                time.sleep(self.round_up(action_response))
                action_response = None
        #print(f"Here's your action... is it really not here? {action_response}")
        return action_response

    def round_up(self, value):
        return math.ceil((value*100)/100)

    def extract_tokens(self, useage):
        self.prompt_tokens = useage["prompt_tokens"]
        self.total_tokens = useage["total_tokens"]
        self.response_tokens = useage["completion_tokens"]
    def extract_responses(self, data):
        try:
            content = data['content'][0]['text']['value']
            content = content.lower()
            temp_dict = json.loads(content)
            #print(temp_dict)
            action_response = temp_dict["action"]
            if type(action_response) is not int:
                print(data)
                print("\n\n")
            return action_response
        except IndexError:
            print("Caught an IndexError: list index out of range while extracting responses")
            exit(0)
            #return None
