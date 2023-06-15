import asyncio
import websockets
import json

async def send_request(endpoint, data=None):
    """
    A function that sends the request to the specific websocket URL.
    params:
        endpoint - part of URL with slash
        data - Optional, contains data for request

    return:
        JSON like response from server
    """

    async with websockets.connect(f"ws://localhost:5002{endpoint}") as websocket:
        if data:
            await websocket.send(json.dumps(data))
        else:
            await websocket.send("")
        response = await websocket.recv()
        return json.loads(response)

async def test_plain():
    data = {"name": "Entity1"}
    response = await send_request("/", data)
    print(response)

async def test_map():
    response = await send_request("/map")
    print(response)

async def test_entity_user():
    data = {"entity_id": "user"}
    response = await send_request("/entity", data)
    print(response)

async def test_entity_wrong_user():
    data = {"entity_id": "user1"}
    response = await send_request("/entity", data)
    print(response)

async def test_entity_wrong_param():
    data = {"entity_name": "user"}
    response = await send_request("/entity", data)
    print(response)

async def test_entity_missing_data():
    response = await send_request("/entity")
    print(response)

async def test_entity_auto():
    data = {"entity_id": "autonomous"}
    response = await send_request("/entity", data)
    print(response)

async def test_move_missing_data():
    response = await send_request("/move")
    print(response)

async def test_move_missing_user_id():
    data = {"coordinates": {"x": 0, "y": 0}}
    response = await send_request("/move", data)
    print(response)

async def test_move_missing_coordinates():
    data = {"user_id": "test"}
    response = await send_request("/move", data)
    print(response)

async def test_move_missing_direction():
    data = {"user_id": "test", "count": -1}
    response = await send_request("/move", data)
    print(response)

async def test_move_missing_count():
    data = {"user_id": "test", "direction": "top"}
    response = await send_request("/move", data)
    print(response)

async def test_move_missing_coordinate_x():
    data = {"user_id": "test", "coordinates": {"y": 0}}
    response = await send_request("/move", data)
    print(response)

async def test_move_missing_coordinate_y():
    data = {"user_id": "test", "coordinates": {"x": 0}}
    response = await send_request("/move", data)
    print(response)

async def test_move_out_of_border():
    data = {"user_id": "test", "coordinates": {"x": -1, "y": 0}}
    response = await send_request("/move", data)
    print(response)

async def test_move_with_coordinates():
    data = {"user_id": "test", "coordinates": {"x": 1, "y": 0}}
    response = await send_request("/move", data)
    print(response)

async def test_move_with_direction():
    data = {"user_id": "test", "direction": "top", "count": 1}
    response = await send_request("/move", data)
    print(response)

async def test_entity_user():
    data = {"entity_id": "user"}
    response = await send_request("/entity", data)
    print(response)

async def tests_with_bad_request():
    """
    A function triggers functions with uncomplete, wrong or bad format request to server
    """

    await test_plain()
    await test_entity_wrong_user()
    await test_entity_wrong_param()
    await test_entity_missing_data()
    await test_move_missing_data()
    await test_entity_missing_user_id()
    await test_entity_missing_coordinates()
    await test_entity_missing_direction()
    await test_entity_missing_count()
    await test_entity_missing_coordinate_x()
    await test_entity_missing_coordinate_y()
    await test_move_out_of_border()


async def main():
    await test_map()

    await test_entity_user()
    await test_entity_auto()

    await test_move_with_coordinates()
    await test_entity_user()

    await test_move_with_direction()
    await test_entity_user()

    # tests_with_bad_request()

asyncio.run(main())