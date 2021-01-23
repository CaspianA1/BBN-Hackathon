from difflib import SequenceMatcher as sm

def top_matches(user_idea):
	with open("types.txt", "r") as types:
		similarities = [[t, sm(None, t, user_idea).ratio()] for t in types.read().split()]
		return sorted(similarities, key = lambda t: t[1])[::-1]

if __name__ == "__main__":
	print(top_matches("taxi"))