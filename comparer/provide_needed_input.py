import networkx as nx
#####################################################################################
def create_subjects_dictionary(lesson_raw):
    # create the dictionary that classifies lessons according to topics in each subject
    subjects = {}
    subjects["no_subject"] = []
  
    for lesson in lesson_raw:
        if lesson.get("subjectName") == None:
            subjects["no_subject"].append(lesson["id"])
        else:
            if subjects.get(lesson["subjectName"]) == None:
                subjects[lesson["subjectName"]] = {}

            current_subject = subjects[lesson["subjectName"]]
            if lesson.get("topic") == None:
                if current_subject.get("no_topic") == None:
                    current_subject["no_topic"] = []
                current_subject["no_topic"].append(lesson["id"])
            else:
                topic = lesson["topic"]
                if topic[0] < "0" or topic[0] > "9":
                    topic = "0" + topic
                if current_subject.get(topic) == None:
                    current_subject[topic] = []
                current_subject[topic].append(lesson["id"])
    return subjects
##########################################################################
def create_lessons_dictionary(lessons_raw):
    # create the dictionary that the keys are lesson IDs
    lessons = {}

    # create teacher and group dictionaries that have each key is ID of 1 teacher (group) 
    # and value is list of lectures belong to that teacher (group),
    # those dictionaries help to create graph faster
    teachers = {}
    groups = {}

    for lesson_raw in lessons_raw:
        lesson_id = lesson_raw.get('id')
        current_lesson = {}
        lessons[lesson_id] = current_lesson
        current_lesson['teacherIDs'] = []
        current_lesson['groupIDs'] = []
        current_lesson['classroomIDs'] = []
        
        # save the information about the teachers that must present to the dictionary
        for teacher_id in lesson_raw.get("teachersIds"):
            current_lesson['teacherIDs'].append(teacher_id)
            if teachers.get(teacher_id) == None:
                teachers[teacher_id] = []
            teachers[teacher_id].append(lesson_id)
        # save the information about the groups of students that must present to the dictionary  
        for group_id in lesson_raw.get('groupsIds'):
            current_lesson['groupIDs'].append(group_id)
            if groups.get(group_id) == None:
                groups[group_id] = []
            groups[group_id].append(lesson_id)
        # save the classrooms for this lesson to the dictionary
        for classroom_id in lesson_raw.get('classroomsIds'):
            current_lesson['classroomIDs'].append(classroom_id)     
    return lessons, teachers, groups
######################################################################
def create_graph(lessons, teachers, groups):
    # create the adjacent graph representing the relationship between lessons
    G = nx.Graph()

    for lesson_id in lessons:
        G.add_node(lesson_id)

    # add edge between lessons that have the same teacher
    for teacher_id in teachers:
        lesson_list = teachers[teacher_id]
        for i in range(len(lesson_list)-1):
            for j in range(i+1, len(lesson_list)):
                G.add_edge(lesson_list[i], lesson_list[j])

    # add edge between lessons that have the same group
    for group_id in groups:
        lesson_list = groups[group_id]
        for i in range(len(lesson_list)-1):
            for j in range(i+1, len(lesson_list)):
                G.add_edge(lesson_list[i], lesson_list[j])
                
    return G
################################################################################################
def create_adjacent_dictionary(G):
    # create the dictionary that contains the relationships between lessons
    adj_dict = {}
    for u in G.nodes():
        adj_dict[u] = {}
        for v in G[u]:
            adj_dict[u][v] = {}
    return adj_dict

################################################################################################
def return_needed_input(data):
    # create needed input for Painter
    lessons_raw = data["events"]
    lessons, teachers, groups = create_lessons_dictionary(lessons_raw)
    
    result = {}
    result["subjects"] = create_subjects_dictionary(lessons_raw)
    result["lessons"] = lessons
    result["groups"] = data["groups"]
    result["teachers"] = data["teachers"]
    result["classrooms"] = data["classrooms"]

    G = create_graph(lessons, teachers, groups)
    result["graph"] = create_adjacent_dictionary(G)

    return result