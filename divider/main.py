import aiohttp
import asyncio
import json
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import divide_data, assemble_data
import time

serverUrl = 'comparer'

app = FastAPI()

@app.post('/api/makeplan')
# use POST method to send data in JSON format to the microservice
async def compute(request: Request = None):
    
    # this retrieve JSON structure from request body
    input = await request.json()
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
    result = assemble_data.assemble_lessons(jsons[0], jsons[1])
    # return results
    return result

@app.websocket('/api/ws')
# use WebSocket to send data in JSON format to the microservice
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            input = await websocket.receive_json()

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
            result = assemble_data.assemble_lessons(jsons[0], jsons[1])
            
            # return results
            await websocket.send_json(result)
        except Exception as e:
            print(e)
            break
