import requests
import json
import re
import sys

# Function that accepts a URL from the API and uses regex to isolate and return the ID
# The API URLs all contain the ID at the end, preceded by "/", which the regex searches for.
def extract_id(url):
	id = re.search("([0-9]+)(?=[^/]*$)", url).group(0)
	return id 

# Examines the JSON file, adding each location and their respective characters to a list
# Checks if the current file has a reference to a next page; if so performs a GET request
# on that page's URL and updates the current JSON. When no next page reference is found
# the loop breaks and the list containing the locations and their characters is returned
def get_all_pages():
	locs = []
	location_info = response.json()
	while True:
		for i in location_info["results"]:
			locs.append(((i["name"]), i["residents"]))
		if location_info["info"]["next"] != None:
			next_page_url = (location_info["info"]["next"])
		else:
			break
		r = requests.get(next_page_url)
		location_info = r.json()
	return locs

# Iterates through the list of locations and characters, printing just the locations
# Enumerates from 1 in order to align with the API's ID numbers for each location
def print_locations(location_char_list):
	for i, pair in enumerate(location_char_list, 1):
		print(i, pair[0], sep=": ")

# Prompts the user to enter the ID number of the location where they wish to see the character.
# Handles ValueError exception in the event that the user selects an invalid index, and also
# prevents the user from entering a negative number of one greater than the total number of locations
def get_user_input(total_locations):
	while True:
		try:
			requested_location = int(input("\nEnter location number to retrieve characters: "))
		except ValueError:
			print("You must enter a valid ID between 1 -", total_locations)
			continue
		if requested_location < 1 or requested_location > total_locations:
			print("You must enter a valid ID between 1 -", total_locations)
			continue	
		return requested_location

# Function to print the characters from the requested location if it has characters
def print_characters(loc_id, location_char_list):
	location_index = loc_id - 1 # The API's IDs are not zero indexed, so substract 1 to prevent incorrent selection
	character_ids = []
	print("\nCharacters at", location_char_list[location_index][0], "\n") # location_chars contains tuples; element 0 contains the location
	for character in location_char_list[location_index][1]: # Element 1 contains the names
		character_ids.append(extract_id(character)) 
	if not character_ids: 
		print("No characters at location")
	else: 
		string = ','.join([str(item) for item in character_ids])
		response = requests.get("https://rickandmortyapi.com/api/character/" + string) # Accesses the API, selecting mutiple characters shown by https://rickandmortyapi.com/documentation/#get-multiple-locations 
		character_info = response.json()
	
		# JSON format is different is there is only 1 character
		if len(character_ids) == 1:
			# Prints the name of the 1 character
			print(character_info["name"])
		else:
			# Prints the name of each each character
			for i in character_info:
				print(i["name"])

# Function to prompt the user for if they want to return to the location list
# or exit the program - returns True or False respectively
def user_continue():
	while True:
		option = input("\nEnter 1 to return to location menu\nEnter 2 to exit\n")
		if option == "2":
			return False
		if option == "1":
			return True	


if __name__ == "__main__":
	# Makes inital GET request to the Rick and Morty API location section 
	response = requests.get("https://rickandmortyapi.com/api/location/")
	
	# get_all_pages() returns a list of tuples, the first element being the location and the second element a list of characters as URLs
	locations_chars = get_all_pages()

	# Continues running until the user specifies that they want to exit
	while True:
		print_locations(locations_chars)
		requested_location = get_user_input(len(locations_chars))
		print_characters(requested_location, locations_chars)
		if not user_continue():
			sys.exit() 
		
