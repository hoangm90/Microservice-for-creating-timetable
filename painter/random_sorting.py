import random

def sort_helper(e):
    # sort topics according to their numerical order
    num = 0
    i = 0
    while e[i] >= "0" and e[i] <= "9":
        num = num*10 + int(e[i])
        i+=1
    return num

def random_sorting(subjects):
    # function for randomizing the order of lessons for coloring but still maintain the order according to topics

    # create list that classifies lessons according to subjects
    ls = []
    i = 0
    if len(subjects["no_subject"]) > 0:
        ls.append([])
        ls[0].extend(subjects["no_subject"])
        random.shuffle(ls[0])
        i=1
    for sub in subjects:
        if sub == "no_subject":
            continue
        else:
            ls.append([])
            topic_list = []
            for topic in subjects[sub]:
                topic_list.append(topic)
            topic_list.sort(reverse=True, key=sort_helper)
      
            for tp in topic_list:
                ls1 = []
                ls1.extend(subjects[sub][tp])
                random.shuffle(ls1)
                ls[i].extend(ls1)
            i += 1

    # create the dictionary that contain the order of lessons in each subject according to topics 
    dict_previous = {}
    start_index = 0
    # lessons that don't belong to any subject don't have order
    if len(subjects["no_subject"]) > 0:
        for j in range(len(ls[0])):
            dict_previous[ls[0][j]] = -1
        start_index = 1
    # lessons that belong to subjects need to follow order of topics
    for i in range(start_index, len(ls)):
        for j in range(len(ls[i])-1):
            dict_previous[ls[i][j]] = ls[i][j+1]
        dict_previous[ls[i][len(ls[i])-1]] = -1

    # create the randomized list
    ls2 = []
    for i in range(len(ls)):
        for j in range(len(ls[i])):
            ls2.append(i)
    random.shuffle(ls2)
    
    # using the randomized list to create the random order of lessons
    ls3 = []
    for i in ls2:
        ls3.append(ls[i].pop())
    return ls3, dict_previous