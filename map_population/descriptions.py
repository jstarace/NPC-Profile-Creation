# Import necessary modules
from connections.mongo_db import get_connection_details
from classes.room_layout import BlankRoom

# Function to load descriptions
def load_descriptions(the_map):
    # Get connection details
    client = get_connection_details()
    # Initialize room_encounters list
    room_encounters = []

    try:
        # Access the "GameDetails" database
        db = client["GameDetails"]
        # Access the "RoomDescriptions" collection
        collection = db["RoomDescriptions"]

        # Fetch all descriptions and store them in a dictionary
        descriptions = {desc["_id"]: desc["description"] for desc in collection.find()}

        # Iterate over the_map
        for i, row in enumerate(the_map):
            for j, col in enumerate(row):
                #print(i*5+j)
                # Get the description from the dictionary
                description = descriptions.get(col[0])
                # Create a new BlankRoom object and set its attributes
                room = BlankRoom(i*5+j)
                # Set the description, encounter_id, and loot_id
                room.set_description(col[0], description)
                room.set_encounter_id(col[1])
                room.set_loot_id(col[2])
                # Append the room to room_encounters
                room_encounters.append(room)
        # Return the room_encounters list

        return room_encounters, client
    except Exception as e:
        # Print any exceptions that occur
        print(e)
