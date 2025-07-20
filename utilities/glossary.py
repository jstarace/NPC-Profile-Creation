def get_definition(term):
    glossary = {
        "Wealth": " If it has value, you must have it.  You have no qualms about risking life and limb in pursuing riches.",
        "Safety": "Your personal Safety is your concern. Items that protect and ensure your safety are of the utmost importance.",
        "Wanderlust": "You want to explore as much as possible.  Items that extend your time or allow you to wander further are important to you.",
        "Speed": "Efficiency is key.  Items that help reduce turns and make navigation easier are what you want and must have.  Speed is efficiency."
    }
    return glossary.get(term, "Term not found")