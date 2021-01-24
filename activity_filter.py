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
	def __init__(self, name: str, type_: str, location: list, inside: bool, cost: int):
		self.name = name
		self.type = type_
		self.location = location
		self.inside = inside
		self.cost = cost

	def matches_criteria(self, *criteria):
		for [crit_type, crit_val] in criteria:
			if crit_type == "type" or crit_type == "indoors":
				# crit val is another location type or an indoors status
				return self.type == crit_val
			elif crit_type == "closeness":
				# crit val is a pair of lat and long
				dlat, dlong = abs(loc[0] - self.location[0]), abs(loc[1] - self.location[1])
				return ((dlat + dlong) / 2) < 50
			elif crit_type == "cheap":
				return self.cost <= 25
			elif crit_type == "medium_price":
				return 50 >= self.cost > 25
			elif crit_type == "expensive":
				return self.cost >= 51

def filter_by_criteria(activities, criteria):
	if not activities:
		return activities
	rest = filter_by_criteria(activities[1:], criteria)
	for criterion in criteria:
		activity = activities[0]
		if activity.matches_criteria(criterion):
			return [activity] + filter_by_criteria(activities[1:], criteria)
		return rest

if __name__ == "__main__":
	activities = [
	Activity("jogging", "recreation", [125.6, 350.0], False, 0),
	Activity("hula hoop", "recreation", [345.2, 90.3], True, 10),
	Activity("library", "academic", [200, 200], True, 0),
	Activity("outdoor studying", "academic", [300, 300], False, 0)
	]
	r = filter_by_criteria(activities, [["type", "academic"], ["indoors", False]])
	print(f"{r[0].name}, {r[1].name}")

# next: take in place types, using google apis, return locations