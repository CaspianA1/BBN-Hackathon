# the goal of this module is to get a latitude and longitude given a town name.

import requests, json

def lat_long_from_address(key, address):
	base = "https://maps.googleapis.com/maps/api/geocode/json?"
	params = f"address={address.replace(' ', '+')}&key={key}"
	response = requests.get(base + params).text
	return json.loads(response)["results"][0]["geometry"]["bounds"]["northeast"]

if __name__ == "__main__":
	geocode_key = "AIzaSyC6J9AVhQ6oJ7wL9khOUZMSQUgDptc_vGY"
	response = lat_long_from_address(geocode_key, "23 Columbia Street, Watertown MA")
	print(response)