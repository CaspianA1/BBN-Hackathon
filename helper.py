from db_construction import Activity, Placetype, Comment, Action, Mood
import math


"""
Args: vec1 (list), vec2 (list)
Takes in 2 vectors of equal shape to find the vector cosine similarity between them
Return: similarity score
"""
def vector_cosine_similarity(vec1,vec2): 
    dot_product = 0
    vec1_sum = 0
    vec2_sum = 0
    for i, v_1 in enumerate(vec1):
        dot_product += v_1 * vec2[i]
        vec1_sum += v_1**2
        vec2_sum += vec2[i]**2

    return dot_product/(math.sqrt(vec1_sum)*math.sqrt(vec2_sum))

"""
input: checkList --> a list of the items checked
output: a list of the associated Placetype Ids
"""
def getPlaces(checkList):
    finalString = ""
    listOfPlaces = set()
    for i in range(len(checkList)):
        activityList = Activity.query.filter_by(activity_name = checkList[i]).first()
        finalString = finalString + activityList
        listOfPlaces.union(set(activityList.split(' ')))
    return listOfPlaces