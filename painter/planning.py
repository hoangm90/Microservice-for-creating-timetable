from random_sorting import random_sorting 

def graph_coloring(subjects, lessons, classrooms, adj_dict):
  # function to assign color and classroom to each lesson

  # create the random order of lessons to be colored and
  # the dictionary that contain the order of lessons in each subject according to topics 
  [nodes, dict_previous_lesson] = random_sorting(subjects)

  colors = {}
  chosen_classrooms = {}
  max_color = -1

  classroom_not_available = {}
  for classroom in classrooms:
    classroom_not_available[classroom["id"]] = set()
  
  # loop to each lesson to assign color and classroom
  for node in nodes:
    current_lesson = lessons[node]
    colors_not_avai = {colors[v] for v in adj_dict[node] if v in colors} 
      
    # set the initial color according to the lesson that has to occured before examined lesson
    if dict_previous_lesson[node] == -1:
      color = 0
    else:
      color = colors[dict_previous_lesson[node]] + 1
    
    # find available color
    while True:
      if color not in colors_not_avai:
        if len(current_lesson['classroomIDs']) == 0:
          chosen_classrooms[node] = ""
          break
        else:
          # find available classroom
          can_assign_classroom = False
          for classroom_id in current_lesson['classroomIDs']:
            if color not in classroom_not_available[classroom_id]:
              classroom_not_available[classroom_id].add(color)
              chosen_classrooms[node] = classroom_id
              can_assign_classroom = True
              break

          if can_assign_classroom:
            break
      color += 1
    
    # assign available color to examined lesson
    colors[node] = color

    # determine the highest used color
    if color > max_color:
      max_color = color
  
  # return the result 
  resp = {}
  resp["colors"] = colors
  resp["chosen_classrooms"] = chosen_classrooms
  resp["max_color"] = max_color
  return resp

def coloring(subjects, lessons, groups, teachers, classrooms, adj_dict):
  return graph_coloring(subjects, lessons, classrooms, adj_dict)
      