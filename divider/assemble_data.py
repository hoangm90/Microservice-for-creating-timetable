import color_time

def assemble_lessons(result1, result2):
    # assemble the 2 independent results into 1 final result
    if result1["order"] == 1:
        lessons1 = result1["events"]
        max1 = result1["number_of_colors"]
        lessons2 = result2["events"]
        max2 = result2["number_of_colors"]
    else:
        lessons1 = result2["events"]
        max1 = result2["number_of_colors"]
        lessons2 = result1["events"]
        max2 = result1["number_of_colors"]
    
    result = {}
    for lesson in lessons2:
        lesson["color"] += max1
        lessons1.append(lesson)
    
    color_to_time = color_time.color_to_time(max1 + max2)
    
    for lesson in lessons1:
        lesson["occurringTime"] = color_to_time[lesson["color"]]
    result['events'] = lessons1
    result["teachers"] = result1["teachers"]
    result["groups"] = result1["groups"]
    result["classrooms"] = result1["classrooms"]
    
    return result