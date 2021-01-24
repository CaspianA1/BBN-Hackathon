from difflib import SequenceMatcher as sm
from functools import reduce
import os, requests, json, multiprocessing as mp

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
			if crit_type == "type":
				return self.type == crit_val
			elif crit_type == "inside":
				return self.inside == crit_val
			elif crit_type == "closeness":
				# crit val is a pair of lat and long
				dlat, dlong = abs(loc[0] - self.location[0]), abs(loc[1] - self.location[1])
				return ((dlat + dlong) / 2) < 50
			elif crit_type == "cheap_cost": # hardcoded at the moment
				return self.cost <= 50
			elif crit_type == "medium_cost":
				return 75 > self.cost > 50
			elif crit_type == "expensive_cost":
				return self.cost >= 75

def filter_by_criteria(activities, criteria):
	if not activities:
		return activities
	for criterion in criteria:
		activity = activities[0]
		if not activity.matches_criteria(criterion):
			return filter_by_criteria(activities[1:], criteria)
	return [activity] + filter_by_criteria(activities[1:], criteria)

"""
if __name__ == "__main__":
	activities = [Activity("jogging", "recreation", [125.6, 350.0], False, 3),
		Activity("hula hoop", "recreation", [345.2, 90.3], True, 10),
		Activity("library", "academic", [200, 200], True, 60),
		Activity("outdoor studying", "academic", [300, 300], False, 5)]
	r = filter_by_criteria(activities, [["inside", True], ["medium_cost", None]])
	print(r[0].name)
"""

def single_type_google_api(payload):
	base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
	param_list = [f"type={payload['type']}", 'fields=photos,name,rating,business_status,price_level']
	for key in payload.keys():
		if key != 'type':
			param_list.append(f"{key}={payload[key]}")
	params = '&'.join(param_list)
	g = json.loads(requests.get(base + params).text)
	if g['status'] == 'OK':
		return g['results']
	return []

def nearby_locs_from_type(d):
	
	base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
	results = []
	if 'type' in d.keys():
		placetype = d['type']
		del d['type']
		all_data = []
		for place in placetype:
			new_d = d.copy()
			new_d['type'] = place
			all_data.append(new_d)
		
		with mp.Pool(5) as p:
			raw_results = p.map(single_type_google_api, all_data)
		for r in raw_results:
			results.extend(r)
		# for place_type in d['type']:
		# 	param_list = [f"location={os.popen('curl ipinfo.io/loc').read()}", f"type={place_type}", 'fields=photos,name,rating,business_status,price_level']
		# 	for key in d.keys():
		# 		if key != 'type':
		# 			param_list.append(f"{key}={d[key]}")
		# 	params = '&'.join(param_list)
		# 	g = json.loads(requests.get(base + params).text)
		# 	if g['status'] == 'OK':
		# 		results.extend(g['results'])
		return sorted(results, key=lambda x:x['rating'] if 'rating' in x.keys() else 3, reverse=True)
	else:
		param_list = ['fields=photos,name,rating,business_status,price_level']
		for key in d.keys():
			if key != 'type':
				param_list.append(f"{key}={d[key]}")
		params = '&'.join(param_list)

		return sorted(json.loads(requests.get(base + params).text)['results'], key=lambda x:x['rating'], reverse=True)