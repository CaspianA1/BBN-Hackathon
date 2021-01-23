import os, requests

def loc_data(key, name, loc_type, radius = 500):
	API_BASE = f"""https://maps.googleapis.com/maps/api/place/nearbysearch/json?
	location={os.popen('curl ipinfo.io/loc').read()}&radius={radius}&types={loc_type}&name={name}&key={key}
	"""
	print(API_BASE)
	return requests.post(API_BASE).text

my_key = "AIzaSyB2TMvSqQ9or3Q4YqgGdnRHcX6lgPhYiJU"
print(loc_data(my_key, "food", "harbour"))