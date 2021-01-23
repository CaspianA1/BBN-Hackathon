from difflib import SequenceMatcher as sm
from functools import reduce

############ this is based on string comparisons
def sort_by_similarity(similarities):
	return sorted(similarities, key = lambda t: t[1])[::-1]

def match_locations_by_name(user_idea):
	with open("types.txt", "r") as types:
		similarities = [[t, sm(None, t, user_idea).ratio()] for t in types.read().split()]
		return sort_by_similarity(similarities)

def union_of_params(*user_activities):
	matched_activities = reduce(lambda i1, i2: i1 + i2,
		[match_locations_by_name(i) for i in user_activities])
	idea_set = []
	for idea in matched_activities:
		if idea[0] not in [i[0] for i in idea_set]:
			idea_set.append(idea)
	return [i for i in sort_by_similarity(idea_set) if i[1] != 0]

if __name__ == "__main__":
	a = union_of_params("rental", "travel", "flight")
	print(a)

##############

class Activity:
	def __init__(self, type_: str, location: str, radius: int, indoor_or_outdoor: bool, cost: int):
		pass