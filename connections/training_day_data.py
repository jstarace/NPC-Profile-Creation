from connections.mongo_trainingData_db import get_connection_details

def create_game_record(record):
    client = get_connection_details()
    db = client["GameInfo"]
    collection = db["GameRecords"]
    result = collection.insert_one(record)
    return result.inserted_id

def create_map_record():
    client = get_connection_details()
    db = client["GameInfo"]
    collection = db["MapDetails"]
    data = {"Player ID": None, "Rooms": None}
    result = collection.insert_one(data)
    return result.inserted_id

def insert_map_data(_id, player_id, map):
    client = get_connection_details()
    db = client["GameInfo"]
    collection = db["MapDetails"]
    data = convert_to_strings(map)
    full_data = {"Player ID": player_id, "Rooms": data}
    collection.replace_one({"_id":_id},full_data)

def create_player_record(name, alignment, motivation, map_id):
    client = get_connection_details()
    player_data = {"Name": name,
                   "Alignment": alignment,
                   "Motivation": motivation,
                   "Map_ID": map_id,
                   "Status": "Incomplete",
                   "Turns":{}
                   }
    db = client["GameInfo"]
    collection = db["PlayerDetails"]
    data = convert_to_strings(player_data)
    result = collection.insert_one(data)
    return result.inserted_id

def get_player_id(_id):
    pass

def get_turn_count(_id):
    client = get_connection_details()
    db = client["GameInfo"]
    record_collection = db["GameRecords"]
    player_collection = db["PlayerDetails"]
    record_db = record_collection.find_one({"_id": _id})
    player_id = record_db["player_id"] if record_db else None
    try:
        player_db = player_collection.find_one({"_id": player_id})
        last_key = get_last_key(player_db["Turns"])
        if not isinstance(last_key, int):
            trunc_key = last_key.split('-')[0]
            last_key = int(trunc_key)
        return last_key + 1
    except Exception as e:
        print(f"No player ID somehow:\n\n{e}\n")
        return 0

def update_player_turns(_id, turn_no, turn):
    client = get_connection_details()
    db = client["GameInfo"]
    record_collection = db["GameRecords"]
    player_collection = db["PlayerDetails"]
    record_db = record_collection.find_one({"_id": _id})
    player_id = record_db["player_id"] if record_db else None
    player_collection.find_one_and_update({"_id": player_id}, {"$set": {f"Turns.{turn_no}": turn}})

def update_player_status(_id, status):
    client = get_connection_details()
    db = client["GameInfo"]
    record_collection = db["GameRecords"]
    player_collection = db["PlayerDetails"]
    record_db = record_collection.find_one({"_id": _id})
    player_id = record_db["player_id"] if record_db else None
    player_collection.find_one_and_update({"_id": player_id}, {"$set": {"Status": status}})

def convert_to_strings(data):
    if isinstance(data, dict):
        return {str(k): convert_to_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_strings(i) for i in data]
    else:
        return str(data)

def get_last_key(d):
    if not d:
        return 0
    return list(d.keys())[-1]