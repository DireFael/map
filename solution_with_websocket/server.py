from datetime import datetime
import random
import json

import asyncio

import websockets

connected_clients = set()

AUTONOMOUS_ENTITY = {
    "name": "Autonomous Entity",
    "coordinates": {"x": 0, "y": 0},
    "last_move": {"x": 0, "y": 0, "user_id": "itself"},
}
USER_ENTITY = {
    "name": "User Entity",
    "coordinates": {"x": 0, "y": 0},
    "last_move": {"x": 0, "y": 0, "user_id": "user1"},
    "history_moves": []
}

async def autonomous_move():
    """
    Functions ensuring autonomous movement of the entity. Uses random motion generation.
    This is then checked to see if it is valid and if so, it is written down and the function is put to sleep for one second.
    This achieves the desired movement of one patch per second. This function is then created as a background task.
    """

    while True:
        auto_move = random.choice([-1,1])
        axis = random.choice(["x", "y"])

        last_move = {"x": 0, "y": 0, "user_id": "itself"}
        last_move[axis] = auto_move

        if (AUTONOMOUS_ENTITY["coordinates"][axis] + auto_move >= 0):
            AUTONOMOUS_ENTITY["coordinates"][axis] += auto_move
            AUTONOMOUS_ENTITY["last_move"] = last_move

            print(f"{datetime.now().strftime('%H:%M:%S %d/%m/%Y')}: Add to axis({axis}) move({auto_move})")
        else:
            pass
            print(f"{datetime.now().strftime('%H:%M:%S %d/%m/%Y')}: Skiping action due to invalid data or reaching borders.")


        await asyncio.sleep(1)

def update_entity(x: int, y: int, user_id: str) -> None:
    """
    The function changes the parameters for the user entity.
    The last movement performed is saved and also timestamped and stored in the complete movement history of the entity.
    params:
        x - coordinate of movement on the x-axis
        y - coordinate of movement on the y-axis
        user_id - identification of user, who requested motion
    """

    USER_ENTITY["coordinates"]["x"] += x
    USER_ENTITY["coordinates"]["y"] += y
    USER_ENTITY["last_move"] = {"x": x, "y": y, "user_id": user_id}
    info = {"time": datetime.now().strftime("%H:%M:%S %d/%m/%Y"), "x": x, "y": y, "user_id": user_id}
    USER_ENTITY["history_moves"].append(info)

def validate_data_in_entity_request(data: dict) -> None:
    """
    Validation whether we have received all necessary data in the request.
    """

    if not data:
        raise Exception("Missing data in request.")

    if "entity_id" not in data:
        raise Exception("Missing key 'entity_name' in data.")
    
    if data["entity_id"] not in ["user", "autonomous"]:
        raise Exception("Wrong entity_id.")

    return

def validate_data_in_move_request(data: dict) -> None:
    """
    Validation whether we have received all necessary data in the request.
    """

    if not data:
        raise Exception("Missing data in request.")

    if "user_id" not in data:
        raise Exception("Missing key 'user_id' in data.")

    if "coordinates" in data:

        if "x" in data["coordinates"] and "y" in data["coordinates"]:

            #add validation to x an y is number or numeric string

            x = data["coordinates"]["x"]
            y = data["coordinates"]["y"]
            user_id = data["user_id"]

            if (USER_ENTITY["coordinates"]["x"] + x < 0) or (USER_ENTITY["coordinates"]["y"] + y < 0):
                raise Exception("The movement cannot be executed, the destination is beyond the permitted borders.")

            return x, y, user_id

        raise Exception("Missing 'x' or 'y' coordinates in request")

    if "direction" in data and "count" in data:
        x = 0
        y = 0
        user_id = data["user_id"]
        count = data["count"]
        direction = data["direction"]

        if direction in ["top", "down", "left", "right"]:

            if direction == "down" or direction == "left":
                count *= -1
    
            if direction == "right" or direction == "left":
                x = count

            if direction == "top" or direction == "down":
                y = count
            
            if (USER_ENTITY["coordinates"]["x"] + x < 0) or (USER_ENTITY["coordinates"]["y"] + y < 0):
                raise Exception("The movement cannot be executed, the destination is beyond the permitted borders.")

            return x, y, user_id

        raise Exception("Direction in request must be on of top/down/left/right.")

    raise Exception("Missing key 'coordinates' or 'direction' with 'count' in data.")

async def handler(websocket, path):
    """
    Function for receiving requests to the server. 
    Individual requests are divided by path. To make the implementation as close to the REST API as possible.
    """
    connected_clients.add(websocket)
    data = {}

    try:
        while True:
            message = await websocket.recv()
            if message:
                data = json.loads(message)
            
            if path == "/map":
                response = {
                    "status": "success",
                    "server_time": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
                    "autonomous_entity": AUTONOMOUS_ENTITY,
                    "user_entity": USER_ENTITY
                }
            elif path == "/entity":
                try:
                    validate_data_in_entity_request(data)

                    response = {"status": "success", data["entity_id"]: USER_ENTITY if data["entity_id"] == "user" else AUTONOMOUS_ENTITY}
                except Exception as e:
                    response = {"status": "error", "message": str(e)}
            elif path == "/move":
                try:
                    x, y, user_id = validate_data_in_move_request(data)
                    update_entity(x, y, user_id)

                    response = {"status": "success", "message": "the movement has been saved"}
                except Exception as e:
                    response = {"status": "error", "message": str(e)}
            else:
                {"status": "error", "message": "This path is not implemented"}

            await websocket.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosedError:
        connected_clients.remove(websocket)
    
    except websockets.exceptions.ConnectionClosedOK:
        connected_clients.remove(websocket)
        print("Client disconnected")

async def start_server():
    async with websockets.serve(handler, "localhost", 5002):
        await asyncio.Future()


async def main():
    server = asyncio.create_task(start_server())
    auto_move = asyncio.create_task(autonomous_move())
    await asyncio.gather(server, auto_move)

asyncio.run(main())