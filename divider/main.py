import aiohttp
import asyncio
from fastapi import FastAPI, Request, WebSocket
import divide_data, assemble_data

import test_input

serverUrl = 'comparer'

app = FastAPI()

@app.post('/api/makeplan')
# use POST method to send data in JSON format to the microservice
async def compute(request: Request = None):
    
    # this retrieve JSON structure from request body
    input = await request.json()
    
    # call to planning function
    result = await timetable_planning(input)

    # return results
    return result

@app.websocket('/api/ws')
# use WebSocket to send data in JSON format to the microservice
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # this receive JSON input from user
            input = await websocket.receive_json()

            # call to planning function
            result = await timetable_planning(input)

            # return results
            await websocket.send_json(result)
        except Exception as e:
            print(e)
            break

async def timetable_planning(input): 
    # check whether the input is in right format
    is_right, error_string = test_input.test_input(input)
    if is_right:
        # calculating the timetable if the input is valid
        # now divide the input into parts (two in this case)
        inputs = divide_data.divide_data(input)
        async def fetch(input):
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{serverUrl}:8000/api/makeplan/', json=input) as resp:
                    return await resp.json() 
        # ask services for a solution
        queries = [fetch(input) for input in inputs]

        # jsons is list which contains a subsolutions
        jsons = await asyncio.gather(*queries)
        # join the subsolutions
        start_date = input.get("startDate")  # the first date in the timetable
        if len(jsons) == 2:
            result = assemble_data.assemble_lessons(jsons[0], jsons[1], start_date)
        else:
            result = assemble_data.attach_timeslots_to_lessons(jsons[0], start_date)
    else:
        # return error that the input is invalid
        result = {"error": error_string}

    # return results
    return result