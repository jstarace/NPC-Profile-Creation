"""
Loads encounter data from MongoDB into room objects based on alignment testing.

Retrieves encounter details (descriptions, options, point values) from the
database and populates rooms that have encounter IDs assigned. Each encounter
is designed to test specific D&D alignment behaviors.

Sets room encounter properties:
- Encounter descriptions and available actions
- Alignment-specific point scoring for each action choice
- Area-of-effect descriptions for adjacent rooms
- Room descriptions updated to match encounter themes

Encounters test alignment consistency through moral/ethical decision scenarios
with scoring based on expected alignment behavior patterns.
"""

def load_encounters(room_encounters, client, alignment):
    try:
        db = client["GameDetails"]
        collection = db["RandomEncounters"]

        for room in room_encounters:
            if room.re_id != "None":
                result = collection.find_one({"_id": room.re_id})
                room.set_encounter(result["alignment"],
                                   result["description"],
                                   result["aoe"],
                                   result["aoe_desc"],
                                   result["aoe_option_desc"],
                                   result["options"],
                                   result["points"][alignment],
                                   result["aoe_points"][alignment]
                                   )
                room.set_description(room.d_id, result["room_description"])
        return room_encounters

    except Exception as e:
        print(e)

