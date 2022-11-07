import requests
import time
from espn_json_helper import *
from Scoreboard import parse_espn_api_json

# Set API URLs from https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b
MLB = "http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
NFL = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
NBA = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
NHL = "http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"
NCAAM = "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"
NCAAF = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"

# Set Base Sports Matrix[URL,dispayName,hasRank]
sports = [[MLB, "MLB", False], [NFL, "NFL", False], [NBA, "NBA", False]]


# sports = [[MLB,"MLB",False], [NFL,"NFL",False], [NBA,"NBA",False], [NHL,"NHL",False], [NCAAF,"NCAAF",True], [NCAAM,
# "NCAAM",True]]


# Start Iterating the JSON
def scrollResults():
    for sport in sports:
        # Query API
        r = requests.get(sport[0])
        data = r.json()
        # Determine if InSeason and Display
        if inSeason(data) is True:
            print("")
            print("++++" + sport[1] + "***")
            # Get Teams and Score
            for game in data['events']:
                parsed_games = parse_espn_api_json(sport[1], game)
                displayHomeTeam = getHomeTeam(game)
                displayHomeScore = getHomeScore(game)
                displayAwayTeam = getAwayTeam(game)
                displayAwayScore = getAwayScore(game)
                displayGameStatus = getGameDisplayStatus(game)
                # Get Ranking Data if Needed
                if sport[2] is True:
                    displayHomeTeamRank = getHomeRank(game)
                    displayAwayTeamRank = getAwayRank(game)
                    if (int(displayHomeTeamRank)) < 99:
                        displayHomeTeam = displayHomeTeamRank + "-" + displayHomeTeam
                    elif (int(displayAwayTeamRank)) < 99:
                        displayAwayTeam = displayAwayTeamRank + "-" + displayAwayTeam
                # Determin Winner and Note
                if getGameFinal(game) is True:
                    if getAwayWinner(game) is True:
                        displayAwayTeam = "*" + displayAwayTeam + "*"
                    elif getHomeWinner(game) is True:
                        displayHomeTeam = "*" + displayHomeTeam + "*"
                # Determine if Regular Season to display record
                if getSeasonType(data) == "Regular Season":
                    displayHomeRecord = getHomeRecord(game)
                    displayAwayRecord = getAwayRecord(game)
                    print(
                        displayAwayRecord + " " + displayAwayTeam + " (" + displayAwayScore + ") @ " + displayHomeRecord + " " + displayHomeTeam + " (" + displayHomeScore + ") - " + displayGameStatus,
                        end=" ")
                # Determine if Postseason to display recoed
                elif getSeasonType(data) == "Postseason":
                    displayHomePlayoffRecord = getHomePlayoffRecord(game)
                    displayAwayPlayoffRecord = getAwayPlayoffRecord(game)
                    print(
                        "[" + displayAwayPlayoffRecord + "] " + displayAwayTeam + " (" + displayAwayScore + ") @ " + "[" + displayHomePlayoffRecord + "] " + displayHomeTeam + " (" + displayHomeScore + ") - " + displayGameStatus,
                        end=" ")
                else:
                    # Print Results
                    print(
                        displayAwayTeam + " (" + displayAwayScore + ") @ " + displayHomeTeam + " (" + displayHomeScore + ") - " + displayGameStatus,
                        end=" ")

                # If Game is final show stats
                if sport[1] == "NBA" or sport[1] == "NHL":
                    print("")
                else:
                    if getGameFinal(game) is True:
                        for leader in game['competitions'][0]['leaders']:
                            # displayStatName = getStatName(leader)
                            for subLeader in leader['leaders']:
                                displayStatAthlete = getStatAthlete(subLeader)
                                displayStat = getStat(subLeader)
                                print(": " + displayStatAthlete + " - " + displayStat, end=" ")
                        print("")
                    else:
                        print("")


while 1 == 1:
    scrollResults()
    print("---------------------------------------------------------------")
    time.sleep(5)
