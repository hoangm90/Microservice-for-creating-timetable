from typing import Optional
import color_time

def attach_timeslots_to_lessons(jsons: dict, start_date: Optional[dict] = None):
    lessons = jsons["events"]
    num_color = jsons["number_of_colors"]
    color_to_time = color_time.color_to_time(num_color, start_date)

    for lesson in lessons:
        time_slot = color_to_time[lesson["color"]]
        lesson["startTime"] = time_slot["startTime"]
        lesson["endTime"] = time_slot["endTime"]
        lesson["dateCode"] = time_slot["dateCode"]
        lesson["date"] = time_slot["date"]
        lesson.pop('color', None)
    
    result = {}
    result['events'] = lessons
    result["teachers"] = jsons["teachers"]
    result["groups"] = jsons["groups"]
    result["classrooms"] = jsons["classrooms"]

    return result

def assemble_lessons(jsons1: dict, jsons2: dict, start_date: Optional[dict] = None):
    # assemble the 2 independent results into 1 final result
    if jsons1["order"] == 1:
        lessons1 = jsons1["events"]
        num_color1 = jsons1["number_of_colors"]
        lessons2 = jsons2["events"]
        num_color2 = jsons2["number_of_colors"]
    else:
        lessons1 = jsons2["events"]
        num_color1 = jsons2["number_of_colors"]
        lessons2 = jsons1["events"]
        num_color2 = jsons1["number_of_colors"]
    
    for lesson in lessons2:
        lesson["color"] += num_color1
        lessons1.append(lesson)
    
    jsons1["events"] = lessons1
    jsons1["number_of_colors"] = num_color1 + num_color2
    
    result = attach_timeslots_to_lessons(jsons1, start_date)
    
    print("Number of colors:", num_color1 + num_color2)
    return result
