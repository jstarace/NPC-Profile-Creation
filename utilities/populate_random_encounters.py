from Connections.mongo_db import get_connection_details

client = get_connection_details()
db = client["GameDetails"]
collection = db["RandomEncounters"]

posts = {
    "post1": {
        "_id": "RE1",
        "alignment": "Lawful Good",
        "room_description": "You enter a radiant chamber adorned with intricate tapestries depicting legendary feats of valor."
                            " The room exudes an aura of righteousness and order, making it clear that this is a gathering of noble heroes.",
        "description": "You see a semi-circle of knights in resplendent, polished armor stand before a figure clad in white robes "
                       "who seems to be delivering an inspirational speech.",
        "aoe": 1,
        "aoe_desc": "From the {direction} you hear the harmonious blend of solemn oaths and uplifting hymns, carried by a chorus of strong, "
                    "determined voices.",
        "aoe_option_desc": "uplifting hymns",
        "options":{
            "1": "({opt}) Listen to the knights",
            "2": "({opt}) Mock the ritual"
        },
        # The points are broken down by element of the dictionary and the points received for each option
        "points": {
            "Lawful Good": (0.8, 0.0, 0.2),
            "Lawful Neutral": (0.4, 0.0, 0.6),
            "Lawful Evil": (0.3, 0.3, 0.4),
            "Neutral Good": (0.4, 0.0, 0.6),
            "True Neutral": (0.0, 0.0, 1.0),
            "Neutral Evil": (0.0, 0.4, 0.6),
            "Chaotic Good": (0.3, 0.3, 0.4),
            "Chaotic Neutral": (0.0, 0.4, 0.6),
            "Chaotic Evil": (0.0, 0.5, 0.5)
        },
        "aoe_points": {
            "Lawful Good": (0.80, 0.20),
            "Lawful Neutral": (0.50, 0.50),
            "Lawful Evil": (0.20, 0.80),
            "Neutral Good": (0.70, 0.30),
            "True Neutral": (0.40, 0.60),
            "Neutral Evil": (0.10, 0.90),
            "Chaotic Good": (0.60, 0.40),
            "Chaotic Neutral": (0.30, 0.70),
            "Chaotic Evil": (0.05, 0.95)
        }
    },
    "post2": {
        "_id": "RE2",
        "alignment": "Lawful Neutral",
        "room_description": "A grand hall, meticulously divided into sections, hums with a precise and orderly energy. "
                            "The walls are adorned with statutes, legal decrees, and scrolls documenting centuries of "
                            "governance and jurisprudence. ",
        "description": "Scribes and magistrates sit in perfectly aligned rows at their desks, their disciplined focus "
                       "a testament to the hall's unwavering dedication to law and order. At the center, an imposing "
                       "overseer ensures every task is carried out efficiently and without deviation. With measured "
                       "authority, they direct you to join the proceedings and contribute to the maintenance of this "
                       "structured and harmonious institution",
        "aoe": 1,
        "aoe_desc": "To the {direction} you hear the steady scratching of quills on parchment and the occasional authoritative command. ",
        "aoe_option_desc": "scratching of quills",
        "options": {
            "1": "({opt}) Find a desk and help",
            "2": "({opt}) Disrupt the proceedings"
        },
        # The points are broken down by element of the dictionary and the points received for each option
        "points": {
            "Lawful Good": (0.6, 0.0, 0.4),
            "Lawful Neutral": (0.9, 0.0, 0.1),
            "Lawful Evil": (0.6, 0.4, 0.0),
            "Neutral Good": (0.3, 0.0, 0.7),
            "True Neutral": (0.0, 0.0, 1.0),
            "Neutral Evil": (0.2, 0.3, 0.5),
            "Chaotic Good": (0.2, 0.3, 0.5),
            "Chaotic Neutral": (0.0, 0.5, 0.5),
            "Chaotic Evil": (0.0, 0.6, 0.4)
        },
        "aoe_points": {
            "Lawful Good": (0.60, 0.40),
            "Lawful Neutral": (0.70, 0.30),
            "Lawful Evil": (0.80, 0.20),
            "Neutral Good": (0.50, 0.50),
            "True Neutral": (0.40, 0.60),
            "Neutral Evil": (0.30, 0.70),
            "Chaotic Good": (0.40, 0.60),
            "Chaotic Neutral": (0.20, 0.80),
            "Chaotic Evil": (0.10, 0.90)
        }
    },
    "post3": {
        "_id": "RE3",
        "alignment": "Lawful Evil",
        "room_description": "The room is a dark, austere chamber filled with ominous symbols and orderly ranks of armored soldiers."
                            " The atmosphere is one of controlled malice.  ",
        "description": "At the center of the room, a cruel yet composed figure sits upon a high-backed chair, issuing commands to "
                       "subordinates who execute them with brutal efficiency. The figure looks up demands you assist them or face their wrath.",
        "aoe": 1,
        "aoe_desc": "From the {direction} you hear the echoed sounds of disciplined marching and authoritative, cold commands.",
        "aoe_option_desc": "disciplined marching",
        "options": {
            "1": "({opt}) Assist the soldiers",
            "2": "({opt}) Refuse to help"
        },
        # The points are broken down by element of the dictionary and the points received for each option
        "points": {
            "Lawful Good": (0.0, 0.4, 0.6),
            "Lawful Neutral": (0.6, 0.2, 0.2),
            "Lawful Evil": (0.83, 0.17, 0.0),
            "Neutral Good": (0.0, 0.4, 0.6),
            "True Neutral": (0.4, 0.2, 0.4),
            "Neutral Evil": (0.6, 0.3, 0.1),
            "Chaotic Good": (0.0, 0.5, 0.5),
            "Chaotic Neutral": (0.0, 0.5, 0.5),
            "Chaotic Evil": (0.36, 0.64, 0.0)
        },
        "aoe_points": {
            "Lawful Good": (0.50, 0.50),
            "Lawful Neutral": (0.80, 0.20),
            "Lawful Evil": (0.90, 0.10),
            "Neutral Good": (0.40, 0.60),
            "True Neutral": (0.50, 0.50),
            "Neutral Evil": (0.30, 0.70),
            "Chaotic Good": (0.20, 0.80),
            "Chaotic Neutral": (0.10, 0.90),
            "Chaotic Evil": (0.10, 0.90)
        }
    },
    "post4": {
        "_id": "RE4",
        "alignment": "Neutral Good",
        "room_description": "The doorway opens to a warm and cozy hall",
        "description": "A diverse group of individuals share stories of past adventures around a central hearth. "
                       "The air is filled with an atmosphere of camaraderie and mutual respect. Healers tend to the "
                       "wounded, and food and drink are freely distributed amongst the needy.",
        "aoe": 1,
        "aoe_desc": "From the {direction} you catch fragments of heartfelt laughter and lively conversation. The inviting aroma of freshly "
                    "cooked stew and baked bread waft through the corridor, mingling with a faint, comforting warmth.",
        "aoe_option_desc": "heartfelt laughter",
        "options":{
            "1": "({opt}) Regale them with your own tale",
            "2": "({opt}) Steal supplies"
        },
        # The points are broken down by element of the dictionary and the points received for each option
        "points": {
            "Lawful Good": (0.5, 0.2, 0.3),
            "Lawful Neutral": (0.3, 0.2, 0.5),
            "Lawful Evil": (0.2, 0.2, 0.6),
            "Neutral Good": (0.9, 0, 0.1),
            "True Neutral": (0.3, 0, 0.7),
            "Neutral Evil": (0.3, 0.3, 0.4),
            "Chaotic Good": (0.6, 0.2, 0.2),
            "Chaotic Neutral": (0.3, 0.3, 0.4),
            "Chaotic Evil": (0.3, 0.5, 0.2)
        },
        "aoe_points": {
            "Lawful Good": (0.80, 0.20),
            "Lawful Neutral": (0.60, 0.40),
            "Lawful Evil": (0.40, 0.60),
            "Neutral Good": (0.90, 0.10),
            "True Neutral": (0.70, 0.30),
            "Neutral Evil": (0.50, 0.50),
            "Chaotic Good": (0.80, 0.20),
            "Chaotic Neutral": (0.60, 0.40),
            "Chaotic Evil": (0.30, 0.70)
        }
    },
    "post5": {
        "_id": "RE5",
        "alignment": "True Neutral",
        "room_description": "The doorway opens to a perfectly balanced chamber, neither favoring nature nor "
                            "civilization. Every detail of the circular hall speaks to equilibrium—stone tiles and "
                            "natural vines seamlessly intertwined. At the center, a tranquil pool reflects the "
                            "chamber’s symmetry, its stillness unbroken. ",
        "description": "Around the pool, monks and druids sit in silent meditation, their presence neither imposing "
                       "nor intrusive. The air feels calm and neutral, inviting you to join without judgment "
                       "or expectation.",
        "aoe": 1,
        "aoe_desc": "To the {direction} you hear the sound of a gently trickling stream and soft chanting meld together "
                    "in the background.",
        "aoe_option_desc": "soft chanting",
        "options": {
            "1": "({opt}) Join in meditation",
            "2": "({opt}) Disrupt the meditation"
        },
        # The points are broken down by element of the dictionary and the points received for each option
        "points": {
            "Lawful Good": (0.6, 0.0, 0.4),
            "Lawful Neutral": (0.5, 0, 0.5),
            "Lawful Evil": (0.4, 0.4, 0.2),
            "Neutral Good": (0.4, 0.0, 0.6),
            "True Neutral": (1.0, 0.0, 0.0),
            "Neutral Evil": (0.3, 0.3, 0.4),
            "Chaotic Good": (0.4, 0.4, 0.2),
            "Chaotic Neutral": (0.2, 0.4, 0.4),
            "Chaotic Evil": (0.0, 0.5, 0.5)
        },
        "aoe_points": {
            "Lawful Good": (0.70, 0.30),
            "Lawful Neutral": (0.60, 0.40),
            "Lawful Evil": (0.30, 0.70),
            "Neutral Good": (0.80, 0.20),
            "True Neutral": (0.50, 0.50),
            "Neutral Evil": (0.40, 0.60),
            "Chaotic Good": (0.70, 0.30),
            "Chaotic Neutral": (0.40, 0.60),
            "Chaotic Evil": (0.20, 0.80)
        }
    },
    "post6": {
        "_id": "RE6",
        "alignment": "Neutral Evil",
        "room_description": "The chamber is dimly lit, its air heavy with power and secrets. Intricate arcane symbols "
                            "pulse faintly along the walls, their sinister patterns hinting at forbidden knowledge. "
                            "Shelves of cursed artifacts and ancient tomes radiate a dark allure, each promising untold "
                            "power to those daring enough to claim it.",
        "description": "At the center, a summoning circle glows ominously, surrounded by dark-robed figures chanting in "
                       "unison. Their ritual seeks to bind a demonic entity, its arrival promising both destruction and "
                       "opportunity. The figures seem unaware of your presence, leaving the question: Will you join, "
                       "take control, or seize the knowledge for yourself?",
        "aoe": 1,
        "aoe_desc": "From the {direction} you hear low, menacing chants and the occasional, unsettling whisper.",
        "aoe_option_desc": "menacing chants",
        "options": {
            "1": "({opt}) Join the ritual",
            "2": "({opt}) Stop the ritual"
        },
        # The points are broken down by element of the dictionary and the points received for each option
        "points": {
            "Lawful Good": (0.0, 0.5, 0.5),
            "Lawful Neutral": (0.4, 0.3, 0.3),
            "Lawful Evil": (0.4, 0.3, 0.3),
            "Neutral Good": (0.0, 0.4, 0.6),
            "True Neutral": (0.4, 0.3, 0.3),
            "Neutral Evil": (0.57, 0.43, 0.0),
            "Chaotic Good": (0.0, 0.4, 0.6),
            "Chaotic Neutral": (0.3, 0.3, 0.4),
            "Chaotic Evil": (0.3, 0.3, 0.4)
        },
        "aoe_points": {
            "Lawful Good": (0.30, 0.70),
            "Lawful Neutral": (0.40, 0.60),
            "Lawful Evil": (0.70, 0.30),
            "Neutral Good": (0.20, 0.80),
            "True Neutral": (0.50, 0.50),
            "Neutral Evil": (0.60, 0.40),
            "Chaotic Good": (0.30, 0.70),
            "Chaotic Neutral": (0.50, 0.50),
            "Chaotic Evil": (0.80, 0.20)
        }
    },
    "post7": {
        "_id": "RE7",
        "alignment": "Chaotic Good",
        "room_description": "You step into a cluttered but lively encampment. Adventurers and rebels alike hustle around"
                            " engaging in various acts of altruism, albeit in unorthodox manners.",
        "description": "They appear ready to defy any corrupt authority to protect the downtrodden.",
        "aoe": 1,
        "aoe_desc": "From the {direction} you hear the rustle of leaves and joyful shouts interspersed with bursts of hearty laughter, "
                    "accompanied by the distant sound of strumming lutes and singing.",
        "aoe_option_desc": "joyful shouts",
        "options":{
            "1": "({opt}) Join in the revelry",
            "2": "({opt}) Steal the supplies"
        },
        # The points are broken down by element of the dictionary and the points received for each option
        "points": {
            "Lawful Good": (0.3, 0.3, 0.4),
            "Lawful Neutral": (0.3, 0.3, 0.4),
            "Lawful Evil": (0.4, 0.3, 0.3),
            "Neutral Good": (0.4, 0.0, 0.6),
            "True Neutral": (0.4, 0.3, 0.3),
            "Neutral Evil": (0.6, 0.3, 0.1),
            "Chaotic Good": (0.8, 0.0, 0.2),
            "Chaotic Neutral": (0.5, 0.0, 0.5),
            "Chaotic Evil": (0.5, 0.3, 0.2)
        },
        "aoe_points": {
            "Lawful Good": (0.80, 0.20),
            "Lawful Neutral": (0.60, 0.40),
            "Lawful Evil": (0.40, 0.60),
            "Neutral Good": (0.90, 0.10),
            "True Neutral": (0.70, 0.30),
            "Neutral Evil": (0.50, 0.50),
            "Chaotic Good": (0.80, 0.20),
            "Chaotic Neutral": (0.60, 0.40),
            "Chaotic Evil": (0.30, 0.70)
        }
    },
    "post8": {
        "_id": "RE8",
        "alignment": "Chaotic Neutral",
        "room_description": "You walk into what appears to be a surreal, whimsical bazaar. Oddly shaped tents and stalls line "
                       "the area, filled with bizarre and fantastical items.",
        "description": "The vendors and customers seem to follow no conventional rules, creating an atmosphere of "
                       "unpredictability and freedom.",
        "aoe": 1,
        "aoe_desc": "To the {direction} the air is filled with a jumble of excited chatter, laughter, and the calls of salesfolk.",
        "aoe_option_desc": "excited chatter",
        "options": {
            "1": "({opt}) Browse the stalls",
            "2": "({opt}) Pickpockets"
        },
        # The points are broken down by element of the dictionary and the points received for each option
        "points": {
            "Lawful Good": (0.0, 0.2, 0.8),
            "Lawful Neutral": (0.0, 0.2, 0.8),
            "Lawful Evil": (0.2, 0.2, 0.6),
            "Neutral Good": (0.3, 0.2, 0.5),
            "True Neutral": (0.4, 0.0, 0.6),
            "Neutral Evil": (0.3, 0.2, 0.5),
            "Chaotic Good": (0.5, 0.0, 0.5),
            "Chaotic Neutral": (0.6, 0.0, 0.4),
            "Chaotic Evil": (0.5, 0.5, 0.0)
        },
        "aoe_points": {
            "Lawful Good": (0.70, 0.30),
            "Lawful Neutral": (0.60, 0.40),
            "Lawful Evil": (0.50, 0.50),
            "Neutral Good": (0.80, 0.20),
            "True Neutral": (0.70, 0.30),
            "Neutral Evil": (0.60, 0.40),
            "Chaotic Good": (0.70, 0.30),
            "Chaotic Neutral": (0.60, 0.40),
            "Chaotic Evil": (0.40, 0.60)
        }
    },
    "post9": {
        "_id": "RE9",
        "alignment": "Chaotic Evil",
        "room_description": "The room is a chaotic scene of utter carnage, filled with broken furniture and blood-stained walls."
                            "Dark altars with vile offerings stand covered in fresh blood, flickering torches casting eerie shadows.",
        "description": "Marauders and dark sorcerers indulge in reckless violence and sadistic revelry.",
        "aoe": 1,
        "aoe_desc": "You hear to the {direction} the harsh sounds of cruel laughter and the agonized screams of victims.",
        "aoe_option_desc": "cruel laughter",
        "options": {
            "1": "({opt}) Join the revelry",
            "2": "({opt}) Stop the violence"
        },
        # The points are broken down by element of the dictionary and the points received for each option
        "points": {
            "Lawful Good": (0.0, 0.5, 0.5),
            "Lawful Neutral": (0.0, 0.3, 0.7),
            "Lawful Evil": (0.5, 0.4, 0.1),
            "Neutral Good": (0.0, 0.4, 0.6),
            "True Neutral": (0.3, 0.3, 0.4),
            "Neutral Evil": (0.5, 0.3, 0.2),
            "Chaotic Good": (0.0, 0.3, 0.7),
            "Chaotic Neutral": (0.4, 0.0, 0.6),
            "Chaotic Evil": (0.6, 0.0, 0.4)
        },
        "aoe_points": {
            "Lawful Good": (0.90, 0.10), # The screams would draw someone of LG alignment these are flipped
            "Lawful Neutral": (0.30, 0.70),
            "Lawful Evil": (0.50, 0.50),
            "Neutral Good": (0.10, 0.90),
            "True Neutral": (0.20, 0.80),
            "Neutral Evil": (0.30, 0.70),
            "Chaotic Good": (0.20, 0.80),
            "Chaotic Neutral": (0.40, 0.60),
            "Chaotic Evil": (0.70, 0.30)
        }
    }
}


for post in posts:
    collection.insert_one(posts[post])

