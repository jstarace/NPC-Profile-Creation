from connections.mongo_db import get_connection_details

def insert_to_db(collection_name, data):
    client = get_connection_details()
    db = client["GameDetails"]
    collection = db[collection_name]
    result = collection.insert_one(data)
    return result.inserted_id

def insert(player = None, game_identifier = None, final_game_map = None, game_history = None, base_map = None, initial_pop_map = None):
    id_map = {
        0: "Base Map",
        1: "Initial Populated Map",
        2: "Player Details",
        3: "Final Game Map"
    }

    if base_map is not None:
        flattened_rooms = [room for row in base_map for room in row]
        base_map_dict = {f"Room {i}": {'Description ID': room[0],
                                           'Encounter ID': room[1],
                                           'Loot ID': room[2]} for i, room in enumerate(flattened_rooms)}
        id = insert_to_db("BaseMap", base_map_dict)
        del base_map_dict
    elif initial_pop_map is not None:
        initial_pop_map_dict = {f"Room {room.loc}": room.to_dict(initial_pop_map) for room in initial_pop_map}
        id = insert_to_db("InitialPopulatedMap", initial_pop_map_dict)
        del initial_pop_map_dict
    elif player is not None:
        player_dict = player.__dict__
        id = insert_to_db("PlayerDetails", player_dict)
        del player_dict
    elif game_identifier is not None:
        game_identifier_dict = {"Game IDs": {id_map[i]: game_identifier[i] if i < len(game_identifier) else None for i in id_map}}
        id = insert_to_db("GameIdentifier", game_identifier_dict)
        del game_identifier_dict
    elif final_game_map is not None:
        final_game_map_dict = {f"Room {room.loc}": room.to_dict(final_game_map) for room in final_game_map}
        id = insert_to_db("FinalPopulatedMap", final_game_map_dict)
        del final_game_map_dict
    elif game_history is not None:
        id = insert_to_db("GameHistory", game_history)

    return id

def replace_player(_id, player):
    client = get_connection_details()
    db = client["GameDetails"]
    collection = db["PlayerDetails"]
    player_dict = player.__dict__
    collection.replace_one({"_id": _id}, player_dict)

def update_ids(_id, final_game_map):
    client = get_connection_details()
    db = client["GameDetails"]
    collection = db["GameIdentifier"]
    collection.update_one({"_id": _id}, {"$set": {"Final Game Map": final_game_map}})