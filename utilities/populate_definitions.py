from Connections.mongo_db import get_connection_details

client = get_connection_details()
db = client["GameDetails"]
collection = db["GameDefinitons"]

posts = {
    "post1":{
        "_id": "DEF-Wealth",
        "type": "Motivation",
        "item": "Wealth",
        "definition": " If it has value, you must have it.  You have no qualms about risking life and limb in pursuing"
                      " riches."
    },
    "post2": {
        "_id": "DEF-Safety",
        "type": "Motivation",
        "item": "Safety",
        "definition": "Your personal Safety is your concern. Items that protect and ensure your safety are of the "
                      "utmost importance."
    },
    "post3": {
        "_id": "DEF-Wanderlust",
        "type": "Motivation",
        "item": "Wanderlust",
        "definition": "You want to explore as much as possible.  Items that extend your time or allow you to wander "
                      "further are important to you."
    },
    "post4": {
        "_id": "DEF-Speed",
        "type": "Motivation",
        "item": "Speed",
        "definition": "Efficiency is key.  Items that help reduce turns and make navigation easier are what you want "
                      "and must have.  Speed is efficiency."
    }
}

for post in posts:
    collection.insert_one(posts[post])