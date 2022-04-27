def return_planned_timetables(data, colors, chosen_classrooms, max_color):
    # add the chosen set of colors and chosen classrooms to lessons
    dict_classrooms = {}
    for cl in data["classrooms"]:
        dict_classrooms[cl["id"]] = cl["name"]

    for l in data["events"]:
        id = l["id"]
        l["color"] = colors[id]
        if dict_classrooms.get(chosen_classrooms[id]) != None:
            l["classroomsIds"] = [chosen_classrooms[id]]
            l["classroomsNames"] = [dict_classrooms[chosen_classrooms[id]]]
        else:
            l["classroomsIds"] = []
            l["classroomsNames"] = []
    
    result = data
    result["number_of_colors"] = max_color + 1
    return result