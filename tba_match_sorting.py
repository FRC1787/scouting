import os
import json

tbaFileName = 'TBAMatches.json'

global tbaMatchesWithPlayoffs
global tbaQualsMatches
tbaQualsMatches = []


try:
    with open(tbaFileName, 'r') as file:
        tbaMatchesWithPlayoffs = json.load(file)
    #print(tbaMatches)
except FileNotFoundError:
    print("Error: The file was not found.")
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from the file.")

for i, match in enumerate(tbaMatchesWithPlayoffs):
    if match["comp_level"] == "qm":
        tbaQualsMatches.insert(match["match_number"], match)
    #print(match["comp_level"])

#print(tbaQualsMatches[11]["match_number"])
