from connections.mongo_db import get_connection_details

def insert_to_db_control(collection_name, data):
    client = get_connection_details()
    db = client["ControlData"]
    collection = db[collection_name]
    result = collection.insert_one(data)
    return result.inserted_id

def create_player_record(player_name, type):
    client = get_connection_details()
    db = client["ControlData"]
    collection = db["PlayerDetails"]
    data = {
        "Player Name": player_name,
        "Game Type": type
    }
    result = collection.insert_one(data)
    return result.inserted_id

def update_player_reccord(_id, activity_id, action, location, inroom_identifiers = None):
    client = get_connection_details()
    db = client["ControlData"]
    collection = db["PlayerDetails"]
    try:
        if not inroom_identifiers:
            other = "None"
        else:
            other = {str(i): item for i, item in enumerate(inroom_identifiers)}

        update_data = {
            f"{activity_id} ({location})": {
                "Selected Option": action,
                "Other ids": other
            }
        }

        collection.update_one({"_id": _id}, {"$set": update_data})
    except Exception as e:
        print(e)
        exit(37)

def create_game_ids(_id):
    client = get_connection_details()
    db = client["ControlData"]
    collection = db["GameIDs"]
    data = {
        "Player ID": _id
    }
    result = collection.insert_one(data)
    return result.inserted_id

def update_game_ids(game_id, id_name, _id):
    client = get_connection_details()
    db = client["ControlData"]
    collection = db["GameIDs"]
    collection.update_one({"_id": game_id}, {"$set":{id_name: _id}})

def upload_base_map(base_map):
    flattened_rooms = [room for row in base_map for room in row]
    base_map_dict = {f"Room {i}": {'Description ID': room[0],
                                        'Encounter ID': room[1],
                                        'Loot ID': room[2]} for i, room in enumerate(flattened_rooms)}
    id = insert_to_db_control("BaseMap", base_map_dict)
    del base_map_dict
    return id

def upload_populated_map(pop_map):
    pop_map_dict = {f"Room {room.loc}": room.to_dict(pop_map) for room in pop_map}
    id = insert_to_db_control("Populated Map", pop_map_dict)
    return id

def get_player_id(game_id):
    client = get_connection_details()
    db = client["ControlData"]
    collection = db["GameIDs"]
    the_dbs = collection.find_one({"_id": game_id})
    player_id = the_dbs["Player ID"] if the_dbs else None
    return player_id


def insert_control(player = None, game_identifier = None, final_game_map = None, game_history = None, base_map = None, initial_pop_map = None):
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
        id = insert_to_db_control("BaseMapControl", base_map_dict)
        del base_map_dict
    elif initial_pop_map is not None:
        initial_pop_map_dict = {f"Room {room.loc}": room.to_dict(initial_pop_map) for room in initial_pop_map}
        id = insert_to_db_control("InitialPopulatedMapControl", initial_pop_map_dict)
        del initial_pop_map_dict
    elif player is not None:
        player_dict = player.__dict__
        id = insert_to_db_control("PlayerDetailsControl", player_dict)
        del player_dict
    elif game_identifier is not None:
        game_identifier_dict = {"Game IDs": {id_map[i]: game_identifier[i] if i < len(game_identifier) else None for i in id_map}}
        id = insert_to_db_control("GameIdentifierControl", game_identifier_dict)
        del game_identifier_dict
    elif final_game_map is not None:
        final_game_map_dict = {f"Room {room.loc}": room.to_dict(final_game_map) for room in final_game_map}
        id = insert_to_db_control("FinalPopulatedMapControl", final_game_map_dict)
        del final_game_map_dict
    elif game_history is not None:
        id = insert_to_db_control("GameHistoryControl", game_history)

    return id

def replace_player_control(_id, player):
    client = get_connection_details()
    db = client["GameDetails"]
    collection = db["PlayerDetailsControl"]
    player_dict = player.__dict__
    collection.replace_one({"_id": _id}, player_dict)

def update_ids_control(_id, final_game_map):
    client = get_connection_details()
    db = client["GameDetails"]
    collection = db["GameIdentifierControl"]
    collection.update_one({"_id": _id}, {"$set": {"Final Game Map": final_game_map}})