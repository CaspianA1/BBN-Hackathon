import os, requests

def loc_data(key, name, loc_type, radius = 500):
	API_BASE = f"""https://maps.googleapis.com/maps/api/place/nearbysearch/json?
	location={os.popen('curl ipinfo.io/loc').read()}&radius={radius}&types={loc_type}&name={name}&key={key}
	"""
	print(API_BASE)
	return requests.post(API_BASE).text

my_key = "AIzaSyB2TMvSqQ9or3Q4YqgGdnRHcX6lgPhYiJU"
print(loc_data(my_key, "food", "harbour"))

# This is old:

# next: take in place types, using google apis, return locations
# types -> instantiations of type

def locations_from_place_desc(api_key, radius, type_desc):
	"""
	The only service I found available that matched our functionality was one
	that gave locations based on a description
	"""
	base_url = "https://maps.googleapis.com/maps/api/place/queryautocomplete/json?"
	params = "key={}&input={}&radius={}&location={}".format(
		api_key, 
		type_desc.replace(" ", "+"),
		radius,
		os.popen("curl ipinfo.io/loc").read())

	response = requests.get(base_url + params)
	print(response.text)

if __name__ == "__main__":
	key = "AIzaSyB2TMvSqQ9or3Q4YqgGdnRHcX6lgPhYiJU"
	locations_from_place_desc(key, 500, "pizza outside")