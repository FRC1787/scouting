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
    # random singleteammatchentrys because I want .team_num and .auto_points to show up for convinince
    redAllianceInOrderData = [SingleTeamSingleMatchEntrysList[0],SingleTeamSingleMatchEntrysList[1],SingleTeamSingleMatchEntrysList[2]]
    blueAllianceInOrderData = [SingleTeamSingleMatchEntrysList[0],SingleTeamSingleMatchEntrysList[1],SingleTeamSingleMatchEntrysList[2]]
    # print(SingleTeamSingleMatchEntrysList.team_num)
    matchData = tbaQualsMatches[SingleTeamSingleMatchEntrysList[0].qual_match_num - 1]
    for i, teamString in enumerate(matchData["alliances"]["blue"]["team_keys"]):
        teamNumWithoutString = int(teamString.replace("frc", ""))
        blueTeamNumbs.append(teamNumWithoutString)
        # print(teamNumWithoutString)
    for i, teamString in enumerate(matchData["alliances"]["red"]["team_keys"]):
        teamNumWithoutString = int(teamString.replace("frc", ""))
        redTeamNumbs.insert(i,teamNumWithoutString)
        # print(teamNumWithoutString)
    for teamMatchData in SingleTeamSingleMatchEntrysList:
        teamNum = teamMatchData.team_num
        # print(teamNum)
        for i in range(6):
            if i <= 2:
                # print(i)
                if teamNum == redTeamNumbs[i]:
                    # print(i)
                    redAllianceInOrderData[i] = teamMatchData
                    # print(str(teamNum) + " red " + str(i+1))
            else:
                if teamNum == blueTeamNumbs[i-3]:
                    blueAllianceInOrderData[i-3] = teamMatchData
                    # print(str(teamNum) + " blue " + str(i-2))
                # print("smth is happening")
    # Validating the data now

    # each of these % off are weighted and represent how off the data is for each game phase
    # for example if 2/3 of the deep climbs were off I might count that 1 not counted as * 6
    autoPrecentOffRed = 0.0
    telePrecentOffRed = 0.0
    endGamePrecentOffRed = 0.0

    autoPrecentOffBlue = 0.0
    telePrecentOffBlue = 0.0
    endGamePrecentOffBlue = 0.0

    redScoutersQuantitativeInacuracy = [0.0,0.0,0.0]
    blueScoutersQuantitativeInacuracy = [0.0,0.0,0.0]

    # auto
    for i in range (2):
        allianceList = []
        team = ""
        autoOffPercent = 0.0
        if i == 0:
            allianceList = redAllianceInOrderData
            team = "red"
        else:
            allianceList = blueAllianceInOrderData
            team = "blue"
        leavesOff = 0.0
        for i in range(3):
            teamAutoLineStr = matchData["score_breakdown"][team]["autoLineRobot"+str(i+1)]
            teamAutoLineBool = teamAutoLineStr == "Yes"
            if allianceList[i].leave != teamAutoLineBool:
                print(allianceList[i].commenter)
                print(allianceList[i].leave)
                print("real" + str(teamAutoLineBool))
                leavesOff += 1.0
        autoOffPercent += 0.3 * (leavesOff / 3.0) # max if can be is 0.3 or 30%
        # print(autoOffPercent)
        scoutedCoralL2Total = allianceList[0].autoL2 + allianceList[1].autoL2 + allianceList[2].autoL2
        scoutedCoralL3Total = allianceList[0].autoL3 + allianceList[1].autoL3 + allianceList[2].autoL3
        scoutedCoralL4Total = allianceList[0].autoL4 + allianceList[1].autoL4 + allianceList[2].autoL4

        tbaL2Auto =  matchData["score_breakdown"][team]["autoReef"]["tba_botRowCount"]
        tbaL3Auto =  matchData["score_breakdown"][team]["autoReef"]["tba_midRowCount"]
        tbaL4Auto =  matchData["score_breakdown"][team]["autoReef"]["tba_topRowCount"]
        
        autoOffPercent += abs(scoutedCoralL2Total - tbaL2Auto) / tbaL2Auto
        autoOffPercent += abs(scoutedCoralL3Total - tbaL3Auto) / tbaL3Auto
        autoOffPercent += abs(scoutedCoralL4Total - tbaL4Auto) / tbaL4Auto
        print(autoOffPercent)

            
        
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

