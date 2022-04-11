import aiohttp
import asyncio

from fastapi import FastAPI, Request

import planning
           

app = FastAPI()

@app.get('/api/makeplan')
async def compute(request: Request):
    # retrieve input from request body
    input = await request.json()

    adj_dict = input["graph"]
    subjects = input["subjects"]
    lessons = input["lessons"]
    groups = input["groups"]
    teachers = input["teachers"]
    classrooms = input["classrooms"]
    
    # compute one result
    result = planning.coloring(subjects, lessons, groups, teachers, classrooms, adj_dict)
    
    # return the result
    return result
