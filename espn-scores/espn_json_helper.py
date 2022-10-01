from datetime import datetime
import re


def inSeason(myJSON=True):
    # Determine if Sport is in Season
    now = datetime.now()
    data = myJSON
    seasonStartDate = data['leagues'][0]['season']['startDate']
    seasonEndDate = data['leagues'][0]['season']['endDate']
    seasonStartDate = re.sub('T.*$', '', seasonStartDate)
    seasonEndDate = re.sub('T.*$', '', seasonEndDate)
    seasonStartDate = datetime.strptime(seasonStartDate, '%Y-%m-%d')
    seasonEndDate = datetime.strptime(seasonEndDate, '%Y-%m-%d')
    if seasonStartDate <= now <= seasonEndDate:
        isInSeason = True
    else:
        isInSeason = False
    return isInSeason


def getSeasonType(myJSON):
    return str(myJSON['leagues'][0]['season']['type']['name'])


def getHomeTeam(myJSON):
    return str(myJSON['competitions'][0]['competitors'][0]['team']['abbreviation'])


def getHomeScore(myJSON):
    return str(myJSON['competitions'][0]['competitors'][0]['score'])


def getHomeRecord(myJSON):
    try:
        homeRecord = "[" + str(myJSON['competitions'][0]['competitors'][0]['records'][0]['summary']) + "]"
        return homeRecord
    except:
        return ""


def getAwayTeam(myJSON):
    return str(myJSON['competitions'][0]['competitors'][1]['team']['abbreviation'])


def getAwayScore(myJSON):
    return str(myJSON['competitions'][0]['competitors'][1]['score'])


def getAwayRecord(myJSON):
    try:
        awayRecord = "[" + str(myJSON['competitions'][0]['competitors'][1]['records'][0]['summary']) + "]"
        return awayRecord
    except:
        return ""


def getHomeWinner(myJSON):
    return myJSON['competitions'][0]['competitors'][0]['winner']


def getAwayWinner(myJSON):
    return myJSON['competitions'][0]['competitors'][1]['winner']


def getHomeRank(myJSON):
    try:
        homeRank = str(myJSON['competitions'][0]['competitors'][0]['curatedRank']['current'])
        return homeRank
    except:
        return ""


def getAwayRank(myJSON):
    try:
        awayRecord = str(myJSON['competitions'][0]['competitors'][1]['curatedRank']['current'])
        return awayRecord
    except:
        return ""


def getGameStatus(myJSON):
    return str(myJSON['status']['type']['name'])


def getGameDisplayStatus(myJSON):
    return str(myJSON['status']['type']['shortDetail'])


def getGameFinal(myJSON):
    if myJSON['status']['type']['completed'] is True:
        return True
    else:
        return False


def getStatName(myJSON):
    return str(myJSON['shortDisplayName'])


def getStatAthlete(myJSON):
    # return str(myJSON['leaders'][0]['athlete']['shortName'])
    return str(myJSON['athlete']['shortName'])


def getStat(myJSON):
    return str(myJSON['displayValue'])


def getHomePlayoffRecord(myJSON):
    try:
        homePlayoffRecord = str(myJSON['competitions'][0]['series']['competitors'][0]['wins'])
        awayPlayoffRecord = str(myJSON['competitions'][0]['series']['competitors'][1]['wins'])
        playoffRecord = homePlayoffRecord + "-" + awayPlayoffRecord
        return playoffRecord
    except:
        return ""


def getAwayPlayoffRecord(myJSON):
    try:
        homePlayoffRecord = str(myJSON['competitions'][0]['series']['competitors'][0]['wins'])
        awayPlayoffRecord = str(myJSON['competitions'][0]['series']['competitors'][1]['wins'])
        playoffRecord = awayPlayoffRecord + "-" + homePlayoffRecord
        return playoffRecord
    except:
        return ""
