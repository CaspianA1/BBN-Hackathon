def get_types():
	with open("types.txt") as t:
		return t.read().split()

print(get_types())