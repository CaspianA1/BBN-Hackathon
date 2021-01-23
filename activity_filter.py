from difflib import SequenceMatcher as sm

def get_types():
	with open("types.txt") as t:
		return t.read().split()

def top_3_matches(user_idea):
	similarities = [[t, sm(None, user_idea, t).ratio()] for t in get_types()]
	print(similarities)

print(top_3_matches("bike"))