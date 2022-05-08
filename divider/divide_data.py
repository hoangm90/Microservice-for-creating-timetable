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
##########################################################################################################
def sort_helper(e):
    # sort topics according to the numerical order
    num = 0
    i = 0
    while e[i] >= "0" and e[i] <= "9":
        num = num*10 + int(e[i])
        i+=1
    return num
###########################################################################################################
def divide_data(data):
    # divide the data received from user into 2 independent sets
    lessons_raw = data["events"]

    # create the dictionary that classifies lessons according to topics in each subject
    subjects = create_subjects_dictionary(lessons_raw)

    # create the list that classifies lessons according to subjects
    ls = []
    i = 0
    if len(subjects["no_subject"]) > 0:
        ls.append([])
        ls[0].extend(subjects["no_subject"])
        i=1
    
    for sub in subjects:
        if sub == "no_subject":
            continue
        else:
            ls.append([])
            topic_list = []
            for topic in subjects[sub]:
                topic_list.append(topic)
            topic_list.sort(key=sort_helper)
      
            for tp in topic_list:
                ls[i].extend(subjects[sub][tp])
            i += 1
    
    # divide the lessons into 2 sets
    lesson_ID_1 = set()
    for i in range(len(ls)):
        n = len(ls[i])//2
        for j in range(n):
            lesson_ID_1.add(ls[i][j])
    
    lessons_1 = []
    lessons_2 = []
    for lesson in lessons_raw:
        if lesson["id"] in lesson_ID_1:
            lessons_1.append(lesson)
        else:
            lessons_2.append(lesson)

    # first independent set
    input1 = {}
    input1["events"] = lessons_1
    input1["groups"] = data["groups"]
    input1["teachers"] = data["teachers"]
    input1["classrooms"] = data["classrooms"]
    input1["order"] = 1

    # second independent set
    input2 = {}
    input2["events"] = lessons_2
    input2["groups"] = data["groups"]
    input2["teachers"] = data["teachers"]
    input2["classrooms"] = data["classrooms"]
    input2["order"] = 2

    if len(input1["events"]) == 0:
        return [input2] 
    
    return [input1, input2]