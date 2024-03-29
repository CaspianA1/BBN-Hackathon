from db_construction import Activity, Placetype, Comment, Action, Mood, Placetype_and_Activity, Mood_and_Activity, Action_and_Activity
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
    n = (math.sqrt(vec1_sum)*math.sqrt(vec2_sum))
    
    return (dot_product/n) if n > 0 else 0

"""
input: checkList --> a list of the items checked
output: a list of the associated Placetype Ids
"""
def getPlaces(checkList):
    listOfPlaces = set()
    for i in range(len(checkList)):
        curr_activity = Activity.query.filter_by(activity_name = checkList[i]).first()

        placetypes_with_this_activity = Placetype_and_Activity.query.filter_by(activity_id=curr_activity.activity_id).all()
        for pk in [i.placetype_id for i in placetypes_with_this_activity]:
            listOfPlaces.add(Placetype.query.filter_by(type_id=pk).first().type_name)
    return listOfPlaces

"""
Args: list of bad big businesses (list), all businesses from google api (list)
Filters any in bad list from the google results
Returns: list of not bad businesses from google api
"""
def filter_bad_businesses_and_get_top_5(bad_businesses, all_businesses):
    bad_set = set(bad_businesses)
    good_businesses = []
    for b in all_businesses:
        bad = False
        for bad_name in bad_set:
            if b['name'] in bad_name:
                bad = True
                break
        if (not bad) and ('OPERATIONAL' == b['business_status']):
            good_businesses.append(b)
    
    return good_businesses[:5] if len(good_businesses) > 5 else good_businesses
        
