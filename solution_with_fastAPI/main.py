from datetime import datetime
import random

import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

AUTONOMOUS_ENTITY = {
    "name": "Autonomous Entity",
    "coordinates": {"x": 0, "y": 0},
    "last_move": {"x": 0, "y": 0, "user_id": "itself"},
    "history_moves": []
}
USER_ENTITY = {
    "name": "User Entity",
    "coordinates": {"x": 0, "y": 0},
    "last_move": {"x": 0, "y": 0, "user_id": "user1"},
    "history_moves": []
}

class MoveDirection(BaseModel):
    direction: str
    count: int
    user_id: str

class Coordinates(BaseModel):
    x: int
    y: int
    
class Move(Coordinates):
    user_id: str

class Entity(BaseModel):
    name: str
    coordinates: Coordinates
    last_move: Move

class EntityWithHistory(Entity):
    history_moves: list

class MapResponse(BaseModel):
    server_time: str
    autonomous_entity: Entity
    user_entity: Entity

async def do_random_move():
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
            info = {"time": datetime.now().strftime("%H:%M:%S %d/%m/%Y")}
            info.update(last_move)
            AUTONOMOUS_ENTITY["history_moves"].append(info)

            print(f"Add to axis({axis}) move({auto_move})")
        else:
            print("Skiping action due to invalid data or reaching borders.")

        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(do_random_move())

@app.get("/")
async def home():
    return {
        "message": "Vitejte na hlavni strance zadani ukolu,",
        "endopointy": {
            "/docs": "Najdete dokumentaci, pro mozne vyzkouseni API",
            "/map": "Najdete data o entitach na mape",
            "/entity/user": "Najde data o uzivatelske entite",
            "/entity/autonomous": "Najdete data o autonomni entite",
            "/entity/user/history": "Najde data o uzivatelske entite vcetne kompletni historie pohybu",
            "/entity/autonomous/history": "Najdete data o autonomni vcetne kompletni historie pohybu",
            "/move": "Je POST metoda, ktera vam umozni ve formatu dictu: x:int, y: int, user_id: str odeslat pohyb/",
            "/move_with_direction": "Je POST metoda, ktera vam umozni poslat ve formatu top/down/right/left, x: int, user_id: str odeslat pohyb"

        }
    }

@app.get("/map", response_model=MapResponse)
async def map() -> MapResponse:
    return {
        "server_time": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
        "autonomous_entity": AUTONOMOUS_ENTITY,
        "user_entity": USER_ENTITY
    }

@app.get("/entity/{entity_name}", response_model=Entity)
async def entity(entity_name: str) -> Entity:
    if entity_name == "user":
        return USER_ENTITY
    elif entity_name == "autonomous":
        return AUTONOMOUS_ENTITY
    else:
        raise HTTPException(status_code=404, detail="Entity not found")

@app.get("/entity/{entity_name}/history", response_model=EntityWithHistory)
async def entity(entity_name: str) -> EntityWithHistory:
    if entity_name == "user":
        return USER_ENTITY
    elif entity_name == "autonomous":
        return AUTONOMOUS_ENTITY
    else:
        raise HTTPException(status_code=404, detail="Entity not found")

@app.post("/move_with_direction")
async def move_with_direction(move_param: MoveDirection):

    if move_param.direction not in ["top", "down", "left", "right"]:
        raise HTTPException(status_code=422, detail="Direction must be top/down/left/right")
    
    if move_param.direction == "down" or move_param.direction == "left":
        move_param.count *= -1
    
    last_move = {"x": 0, "y": 0, "user_id": move_param.user_id}

    if move_param.direction == "right" or move_param.direction == "left":
        last_move["x"] = move_param.count

    if move_param.direction == "top" or move_param.direction == "down":
        last_move["y"] = move_param.count

    if (USER_ENTITY["coordinates"]["x"] + last_move["x"] < 0) or (USER_ENTITY["coordinates"]["y"] + last_move["y"] < 0):
        raise HTTPException(status_code=409, detail="The movement cannot be executed, the destination is beyond the permitted borders.")
    
    USER_ENTITY["coordinates"]["x"] += last_move["x"]
    USER_ENTITY["coordinates"]["y"] += last_move["y"]
    USER_ENTITY["last_move"] = last_move
    info = {"time": datetime.now().strftime("%H:%M:%S %d/%m/%Y")}
    info.update(last_move)
    USER_ENTITY["history_moves"].append(info)

    return {"OK - the movement has been saved"}

@app.post("/move")
async def move(move_param: Move):
    if (USER_ENTITY["coordinates"]["x"] + move_param.x < 0) or (USER_ENTITY["coordinates"]["y"] + move_param.y < 0):
        raise HTTPException(status_code=409, detail="The movement cannot be executed, the destination is beyond the permitted borders.")
    
    USER_ENTITY["coordinates"]["x"] += move_param.x
    USER_ENTITY["coordinates"]["y"] += move_param.y
    USER_ENTITY["last_move"] = move_param
    info = {"time": datetime.now().strftime("%H:%M:%S %d/%m/%Y")}
    info.update(move_param)
    USER_ENTITY["history_moves"].append(info)

    return {"OK - the movement has been saved"}