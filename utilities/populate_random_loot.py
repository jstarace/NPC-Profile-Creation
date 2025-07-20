from Connections.mongo_db import get_connection_details

client = get_connection_details()
db = client["GameDetails"]
collection = db["RandomLoot"]

posts = {
    "post1": {
        "_id": "L1",
        "motivation": "Wealth",
        "item": "Gold Idol",
        "description": "In the corner of the room you see a medium size golden idol worth at least 1,000 gold pieces."
                       "You can tell by it's size that it will slow your movement",
        "options": {
            "1": "({opt}) Take the idol",
            "2": "({opt}) Leave"
        },
        "points":{
            "Wealth": (1.0, 0.0),
            "Safety": (0.0, 1.0),
            "Wanderlust": (0.0, 1.0),
            "Speed": (0.0, 1.0)
        },
        "aoe": 1,
        "aoe_desc": "From the {direction} you catch torchlight dancing on golden metal",
        "aoe_option_desc": "golden light",
        "aoe_points": {
            "Wealth": (0.95, 0.05),
            "Safety": (0.20, 0.80),
            "Wanderlust": (0.70, .030),
            "Speed": (0.15, 0.85)
        },
        "special": False
    },
    "post2": {
        "_id": "L2",
        "motivation": "Wealth",
        "item": "Treasure Pile",
        "description": "In the middle of the room lies a small mound of treasure worth at least 1,250 gold.  Gems, coins,"
                       " and jewels are glinting in the light. You can't help but wonder if the owner is near.",
        "options": {
            "1": "({opt}) Take the treasure",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.86, 0.14),
            "Safety": (0.00, 1.00),
            "Wanderlust": (0.71, 0.29),
            "Speed": (0.00, 1.00)
        },
        "aoe": 1,
        "aoe_desc": "Colorful lights dance in the hallway to the {direction}",
        "aoe_option_desc": "dancing lights",
        "aoe_points": {
            "Wealth": (0.30, 0.70),
            "Safety": (0.10, 0.90),
            "Wanderlust": (0.85, 0.15),
            "Speed": (0.10, 0.90)
        },
        "special": False
    },
    "post3": {
        "_id": "L3",
        "motivation": "Wealth",
        "item": "Small Treasure Chest",
        "description": "There is a small locked treasure chest in an small alcove, it can't be worth more than 150 gold."
                       "Breaking the lock would be easy enough, though it might draw attention or take some time",
        "options": {
            "1": "({opt}) Break the lock and take contents",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.67, 0.33),
            "Safety": (0.00, 1.00),
            "Wanderlust": (0.40, 0.60),
            "Speed": (0.00, 1.00)
        },
        "aoe": 0,
        "aoe_desc": "None",
        "aoe_option_desc": "None",
        "aoe_points": {
            "Wealth": (0.00, 0.00),
            "Safety": (0.00, 0.00),
            "Wanderlust": (0.00, 0.00),
            "Speed": (0.00, 0.00)
        },
        "special": False
    },
    "post4": {
        "_id": "L4",
        "motivation": "Safety",
        "item": "Shield of Protection",
        "description": "You see a shield leaning against the wall of no value. The shield is lightwieght and will protect the traveler from all danger.",
        "options": {
            "1": "({opt}) Take the shield",
            "2": "({opt}) Leave"
        },
        "points":{
            "Wealth": (0.00, 1.00),
            "Safety": (1.00, 0.00),
            "Wanderlust": (0.67, 0.33),
            "Speed": (0.75, 0.25)
        },
        "aoe": 1,
        "aoe_desc": "From the {direction} you feel a sense of safety and security",
        "aoe_option_desc": "feeling of safety",
        "aoe_points": {
            "Wealth": (.10, .90),
            "Safety": (.95, 0.05),
            "Wanderlust": (0.60, 0.40),
            "Speed": (0.30, 0.70)
        },
        "special": False
    },
    "post5": {
        "_id": "L5",
        "motivation": "Safety",
        "item": "Safe Passage spell",
        "description": "An open scroll on an alter tells you that you may advance directly to the exit if you wish. "
                       "This will happen immediately and no further exploration, treasure, or paths can be taken, but "
                       "you will be safe.",
        "options": {
            "1": "({opt}) Use the scroll",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.00, 1.00),
            "Safety": (1.00, 0.00),
            "Wanderlust": (0.00, 1.00),
            "Speed": (.60, 0.40)
        },
        "aoe": 0,
        "aoe_desc": "None",
        "aoe_option_desc": "None",
        "aoe_points": {
            "Wealth": (0.00, 0.00),
            "Safety": (0.00, 0.00),
            "Wanderlust": (0.00, 0.00),
            "Speed": (0.00, 0.00)
        },
        "special": "end_game"
    },
    "post6": {
        "_id": "L6",
        "motivation": "Safety",
        "item": "Charm of Safe Passage",
        "description": "There is a charm lying on a table with a note that reads. 'The bearer of this charm will face "
                       "no encounters and have a peaceful journey while under its protection.",
        "options": {
            "1": "({opt}) Take the charm",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.50, 0.50),
            "Safety": (1.00, 0.00),
            "Wanderlust": (0.33, 0.67),
            "Speed": (1.00, 0.00)
        },
        "aoe": 0,
        "aoe_desc": "None",
        "aoe_option_desc": "None",
        "aoe_points": {
            "Wealth": (0.00, 0.00),
            "Safety": (0.00, 0.00),
            "Wanderlust": (0.00, 0.00),
            "Speed": (0.00, 0.00)
        },
        "special": "encounter_deactivate"
    },
    "post7": {
        "_id": "L7",
        "motivation": "Wanderlust",
        "item": "Map of the Dungeon",
        "description": "On the wall is a map of the progress you've made so far.  The map will show you the rooms "
                       "you've visited and your current location, should you look at it.",
        "options": {
            "1": "({opt}) Study the map",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.60, 0.40),
            "Safety": (1.00, 0.00),
            "Wanderlust": (1.00, 0.00),
            "Speed": (0.75, 0.25)
        },
        "aoe": 0,
        "aoe_desc": "None",
        "aoe_option_desc": "None",
        "aoe_points": {
            "Wealth": (0.00, 0.00),
            "Safety": (0.00, 0.00),
            "Wanderlust": (0.00, 0.00),
            "Speed": (0.00, 0.00)
        },
        "special": "ingame_map"
    },
    "post8": {
        "_id": "L8",
        "motivation": "Wanderlust",
        "item": "Bell of turns",
        "description": "A weathered bell hangs in the center of the room, its surface etched with intricate carvings of "
                       "distant lands and unknown constellations. The inscription reads: 'Ring this bell to uncover the "
                       "time left for your journey, so you may plan your path and uncover every hidden corner before "
                       "the end.' The sound of the bell promises to echo far and wide, reverberating with a sense of "
                       "wonder but also hinting at the possibility of drawing unwanted attention, slowing progress for "
                       "those eager to rush ahead.",
        "options": {
            "1": "({opt}) Ring the bell",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.50, 0.50),
            "Safety": (0.50, 0.50),
            "Wanderlust": (1.00, 0.00),
            "Speed": (0.00, 1.00)
        },
        "aoe": 1,
        "aoe_desc": "Off to the {direction} you hear the soft ringing of a bell",
        "aoe_option_desc": "Ringing",
        "aoe_points": {
            "Wealth": (0.70, 0.30),
            "Safety": (0.20, 0.80),
            "Wanderlust": (0.90, 0.10),
            "Speed": (0.40, 0.60)
        },
        "special": "bell"
    },
    "post9": {
        "_id": "L9",
        "motivation": "Wanderlust",
        "item": "Big Red Button",
        "description": "Next to the door is a big red button with the inscription. Press it to reset all progress, allowing you to explore everything as if it were new.",
        "options": {
            "1": "({opt}) Press the button",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.67, 0.33),
            "Safety": (0.00, 1.00),
            "Wanderlust": (1.00, 0.00),
            "Speed": (0.00, 1.00)
        },
        "aoe": 0,
        "aoe_desc": "None",
        "aoe_option_desc": "None",
        "aoe_points": {
            "Wealth": (0.00, 0.00),
            "Safety": (0.00, 0.00),
            "Wanderlust": (0.00, 0.00),
            "Speed": (0.00, 0.00)
        },
        "special": "reset"
    },
    "post10": {
        "_id": "L10",
        "motivation": "Speed",
        "item": "Exit map",
        "description": "On the far wall is a simple, efficient map etched with clear lines and arrows. A brief note "
                       "beside it reads: 'Quickly reference this map to see your current location and the fastest route "
                       "to the exit.' The map focuses solely on providing the shortest and most direct path, with no "
                       "distractions or unnecessary details about unexplored areas.",
        "options": {
            "1": "({opt}) Study the map",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.50, 0.50),
            "Safety": (0.75, 0.25),
            "Wanderlust": (0.00, 1.00),
            "Speed": (1.00, 0.00)
        },
        "aoe": 0,
        "aoe_desc": "None",
        "aoe_option_desc": "None",
        "aoe_points": {
            "Wealth": (0.00, 0.00),
            "Safety": (0.00, 0.00),
            "Wanderlust": (0.00, 0.00),
            "Speed": (0.00, 0.00)
        },
        "special": "exit_map"
    },
    "post11": {
        "_id": "L11",
        "motivation": "Speed",
        "item": "Wheel of Time",
        "description": "In the center of the room sits a smooth, well-crafted stone table, holding a polished wheel. "
                       "An inscription reads: 'Turn this wheel to regain 5 turns and efficiently shorten your journey "
                       "through the dungeon.' The wheel gleams with precision, inviting those who value swift and "
                       "seamless progress to take action.",
        "options": {
            "1": "({opt}) Turn the wheel",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.34, 0.66),
            "Safety": (0.50, 0.0),
            "Wanderlust": (0.00, 1.00),
            "Speed": (1.00, 0.00)
        },
        "aoe": 0,
        "aoe_desc": "None",
        "aoe_option_desc": "None",
        "aoe_points": {
            "Wealth": (0.00, 0.00),
            "Safety": (0.00, 0.00),
            "Wanderlust": (0.00, 0.00),
            "Speed": (0.00, 0.00)
        },
        "special": "turn-5"
    },
    "post12": {
        "_id": "L12",
        "motivation": "Speed",
        "item": "Hidden Path",
        "description": "You notice a hidden doorway in the corner of the room. A message scrawled into the door reads, 'this ancient path will take you to a room next to the exit.'",
        "options": {
            "1": "({opt}) Enter the doorway",
            "2": "({opt}) Leave"
        },
        "points": {
            "Wealth": (0.75, 0.25),
            "Safety": (0.75, 0.25),
            "Wanderlust": (0.67, 0.33),
            "Speed": (1.00, 0.00)
        },
        "aoe": 0,
        "aoe_desc": "None",
        "aoe_option_desc": "None",
        "aoe_points": {
            "Wealth": (0.00, 0.00),
            "Safety": (0.00, 0.00),
            "Wanderlust": (0.00, 0.00),
            "Speed": (0.00, 0.00)
        },
        "special": "next_to_exit"
    }
}

for post in posts:
    collection.insert_one(posts[post])