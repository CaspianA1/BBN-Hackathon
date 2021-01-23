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

"""
if __name__ == "__main__":
	a = union_of_params("rental", "travel", "flight")
	print(a)
"""

##############

class Activity:
	def __init__(self, type_: str, location: list, inside: bool, cost: int):
		self.type = type_
		self.location = location
		self.inside = inside
		self.cost = cost

	def matches_criteria(self, *criteria):
		for [crit_type, crit_val] in criteria:
			if crit_type == "type" or crit_type == "indoors":
				# crit val is another location type or an indoors status
				return self.type == crit_val
			elif crit_type == "location":
				# crit cal is a pair of lat and long
				dlat, dlong = abs(loc[0] - self.location[0]), abs(loc[1] - self.location[1])
				return ((dlat + dlong) / 2) < max_dist
			elif crit_type == "cheap":
				return self.cost <= 25
			elif crit_type == "medium_price":
				return 50 >= self.cost > 25
			elif crit_type == "expensive":
				return self.cost >= 51

def filter_by_criteria(activities, criteria):
	if not criteria:
		return activities
	elif matches_criteria(activity := activities[0], criterion := criteria[0]):
		return [activity] + filter_by_criteria(activities[1:], criteria[1:])
	else:
		return filter_by_criteria(activities[1:], criteria[1:])


if __name__ == "__main__":
	pass


# a = Activity("", [], False, 51)

# print(a.price_bracket())

# take in place types, using google apis, return locations