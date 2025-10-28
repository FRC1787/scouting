from dataclasses import dataclass
import os
import json
import shared_classes
from typing import List

tbaFileName = 'TBAMatches.json'

global tbaMatchesWithPlayoffs
global tbaQualsMatches
global scoutedQualsMatchesRed
global scoutedQualsMatchesBlue
tbaQualsMatches = []
scoutedQualsMatchesRed = []
scoutedQualsMatchesBlue = []

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

def makeBothAllianceMatchClass(SingleTeamSingleMatchEntrysList: List[shared_classes.SingleTeamSingleMatchEntry]):
    redTeamNumbs = []
    blueTeamNumbs = []
    redAllianceInOrder = [0,0,0]
    blueAllianceInOrder = [0,0,0]
    # print(SingleTeamSingleMatchEntrysList.team_num)
    matchData = tbaQualsMatches[SingleTeamSingleMatchEntrysList[0].qual_match_num - 1]
    for teamString in matchData["alliances"]["blue"]["team_keys"]:
        teamNumWithoutString = int(teamString.replace("frc", ""))
        blueTeamNumbs.append(teamNumWithoutString)
        print(teamNumWithoutString)
    for i, teamString in enumerate(matchData)["alliances"]["red"]["team_keys"]:
        teamNumWithoutString = int(teamString.replace("frc", ""))
        redTeamNumbs.insert(i,teamNumWithoutString)
        print(teamNumWithoutString)
    for teamMatchData in SingleTeamSingleMatchEntrysList:
        teamNum = teamMatchData.team_num
        for i in range(6):
            if i <= 3:
                if teamNum == redTeamNumbs[i]:
                    # print(i)
                    redAllianceInOrder[i] = teamNum
                    print(str(teamNum) + " " + str(i))
            else:
                if teamNum == blueTeamNumbs[i-3]:
                    redAllianceInOrder[i-3] = teamNum
                    print(str(teamNum) + "   " + str(i))
                print("smth is happening")

    
    
        
def initializeTBAData():
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
        # print(match["comp_level"])

#print(tbaQualsMatches[11]["match_number"])

