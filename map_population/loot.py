"""
Loads loot data from MongoDB into room objects based on motivation testing.

Retrieves loot details (descriptions, options, point values) from the
database and populates rooms that have loot IDs assigned. Each loot item
is designed to test specific player motivations.

Sets room loot properties:
- Loot descriptions and interaction options
- Motivation-specific point scoring for take/ignore decisions
- Area-of-effect descriptions for adjacent rooms
- Special effects (teleportation, time manipulation, etc.)

Loot items test motivation consistency through resource/risk scenarios
with scoring based on expected motivation-driven behavior patterns.
"""

def load_loot(room_encounters, client, motivation):
    try:
        db = client["GameDetails"]
        collection = db["RandomLoot"]

        for room in room_encounters:
            if room.l_id != "None":
                result = collection.find_one({"_id": room.l_id})
                room.set_loot(result["motivation"],
                              result["item"],
                              result["description"],
                              result["aoe"],
                              result["aoe_desc"],
                              result["aoe_option_desc"],
                              result["options"],
                              result["points"][motivation],
                              result["aoe_points"][motivation],
                              result["special"]
                              )

        return room_encounters

    except Exception as e:
        print(e)

