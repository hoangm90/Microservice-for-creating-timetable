import datetime

def test_input(input: dict):
    # check if the start date is in the right format, if it is included
    try:
        if input.get("startDate") != None:
            start_date = input["startDate"]
            try: 
                date = datetime.date(start_date.get("year"), start_date.get("month"), start_date.get("day"))
            except Exception as e:
                print(e)
                return False, "Wrong date format!"
    except Exception as e:
        print(e)
        return False, "Input is not a dictionary!"

    # check the list of all teachers
    try:
        teachers = input["teachers"]
        if type(teachers) is not list:
            return False, "Teacher list is not of the list type!"

        teachers_dict = {}

        for i in range(len(teachers)):
            error_string = "Item " + str(i) + " of teacher list is not in the right format!"
            try:
                # check each item of the teacher list
                teacher = teachers[i]
                id = teacher["id"]
                name = teacher["name"]
                if type(id) is not str and type(id) is not int:
                    return False, error_string
                if type(name) is not str and type(name) is not int:
                    return False, error_string
                
                teachers_dict[id] = name.lower() if type(name) is str else name             
            except Exception as e:
                print(e)
                return False, error_string
    except Exception as e:
        print(e)
        return False, "The input does not have teacher list!"
    
    # check the list of all classrooms
    try:
        classrooms = input["classrooms"]
        if type(classrooms) is not list:
            return False, "Classroom list is not of the list type!"

        classrooms_dict = {}

        for i in range(len(classrooms)):
            error_string = "Item " + str(i) + " of classroom list is not in the right format!"
            try:
                # check each item of the classroom list
                classroom = classrooms[i]
                id = classroom["id"]
                name = classroom["name"]
                if type(id) is not str and type(id) is not int:
                    return False, error_string
                if type(name) is not str and type(name) is not int:
                    return False, error_string
                
                classrooms_dict[id] = name.lower() if type(name) is str else name
            except Exception as e:
                print(e)
                return False, error_string
    except Exception as e:
        print(e)
        return False, "The input does not have classroom list!"
    
    # check the list of all study groups
    try:
        groups = input["groups"]
        if type(groups) is not list:
            return False, "Group list is not of the list type!"

        groups_dict = {}

        for i in range(len(groups)):
            error_string = "Item " + str(i) + " of group list is not in the right format!"
            try:
                # check each item of the group list
                group = groups[i]
                id = group["id"]
                name = group["name"]
                if type(id) is not str and type(id) is not int:
                    return False, error_string
                if type(name) is not str and type(name) is not int:
                    return False, error_string
                
                groups_dict[id] = name.lower() if type(name) is str else name
            except Exception as e:
                print(e)
                return False, error_string
    except Exception as e:
        print(e)
        return False, "The input does not have group list!"

    # check the event list
    try:
        events = input["events"]
        if type(events) is not list:
            return False, "Event list is not of the list type!"
        
        # check each lesson
        for i in range(len(events)):
            error_string = "Item " + str(i) + " of event list is not in the right format!"
            try:
                lesson = events[i]
                # check the id of the lesson
                id = lesson["id"]
                if type(id) is not str and type(id) is not int:
                    return False, error_string

                # check the list of teachers, classrooms and study groups in each lesson
                groups_id = lesson["groupsIds"]
                teachers_id = lesson["teachersIds"]
                classrooms_id = lesson["classroomsIds"]

                groups_name = lesson["groupsNames"]
                teachers_name = lesson["teachersNames"]
                classrooms_name = lesson["classroomsNames"]

                if len(groups_id) != len(groups_name) or len(teachers_id) != len(teachers_name) or len(classrooms_id) != len(classrooms_name):
                    return False, error_string
                
                for j in range(len(groups_id)):
                    name = groups_name[j].lower() if type(groups_name[j]) is str else groups_name[j]
                    if groups_dict[groups_id[j]] != name:
                        return False, error_string

                for j in range(len(teachers_id)):
                    name = teachers_name[j].lower() if type(teachers_name[j]) is str else teachers_name[j]
                    if teachers_dict[teachers_id[j]] != name:
                        return False, error_string

                for j in range(len(classrooms_id)):
                    name = classrooms_name[j].lower() if type(classrooms_name[j]) is str else classrooms_name[j]
                    if classrooms_dict[classrooms_id[j]] != name:
                        return False, error_string
                
                # check for valid subject and topic, if those fields are included
                if lesson.get("subjectId") != None:
                    if type(lesson["subjectId"]) is not int and type(lesson["subjectId"]) is not str:
                        print("ttttt")
                        return False, error_string
                if lesson.get("subjectName") != None:
                    if type(lesson["subjectName"]) is not int and type(lesson["subjectName"]) is not str:
                        print("tttta")
                        return False, error_string
                
                if lesson.get("topicId") != None:
                    if type(lesson["topicId"]) is not int and type(lesson["topicId"]) is not str:
                        print("ssss")
                        return False, error_string
                if lesson.get("topic") != None:
                    if type(lesson["topic"]) is not int and type(lesson["topic"]) is not str:
                        print("sssa")
                        return False, error_string
            except Exception as e:
                print(e)
                return False, error_string

    except Exception as e:
        print(e)
        return False, "The input does not have event list!"
    
    # return true if the input passes all the tests
    return True, "OK"