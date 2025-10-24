from dataclasses import dataclass
import os
import json
import data_process

tbaFileName = 'TBAMatches.json'

global tbaMatchesWithPlayoffs
global tbaQualsMatches
tbaQualsMatches = []

@dataclass
class singleAllianceMatch:
    matchNum: int = 0
    isRedAlliance: bool = False
    firstBotTeamNumber: int = 0
    secondBotTeamNumber: int = 0
    thirdBotTeamNumber: int = 0

    autol4Count: int = 0
    autol3Count: int = 0
    autol2Count: int = 0
    autol1Count: int = 0
    autoMove: bool = False

    l4Count: int = 0
    l3Count: int = 0
    l2Count: int = 0
    l1Count: int = 0
    proccesorCount: int = 0
    netCount: int = 0

    # end game can be None, Parked, ShallowCage, DeepCage
    firstBotEndgame: str = "None"
    secondBotEndgame: str = "None"
    thirdBotEndgame: str = "None"

def makeBothAllianceMatchClass(SingleTeamSingleMatchEntry):
    print(SingleTeamSingleMatchEntry)
        
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

