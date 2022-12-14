from Scoreboard import Scoreboard
from Scoreboard import Sport
from Scoreboard import Team
from Scoreboard import TimeState
from Scoreboard import GameClock
from Scoreboard import GameSituation
import json
import datetime
import calendar


def parse_espn_api_json(sport: str, espn_game_json: dict, espn_sport_json: dict):
    home, away = parse_home_and_away(espn_game_json, espn_sport_json)
    gameclock = parse_gameclock(Sport[sport.upper()], espn_game_json)
    scoreboard = Scoreboard(Sport[sport.upper()], home, away, gameclock)
    # print('scoreboard: ', str(scoreboard))
    return scoreboard


def parse_home_and_away(espn_game_json: dict, espn_sport_json: dict):
    home_json = espn_game_json['competitions'][0]['competitors'][0]
    home_team_name = home_json['team']['abbreviation']
    home_score = home_json.get('score', None)

    away_json = espn_game_json['competitions'][0]['competitors'][1]
    away_team_name = away_json['team']['abbreviation']
    away_score = away_json.get('score', None)

    home_record, away_record = get_record(espn_game_json, espn_sport_json)

    away = Team(away_team_name, away_record, away_score)
    home = Team(home_team_name, home_record, home_score)
    return home, away


def get_record(espn_game_json, espn_sport_json: dict):
    home_record = None
    away_record = None
    season_type = espn_sport_json['leagues'][0]['season']['type']['name']
    if season_type == "Regular Season":
        home_record = espn_game_json['competitions'][0]['competitors'][0]['records'][0]['summary']
        away_record = espn_game_json['competitions'][0]['competitors'][1]['records'][0]['summary']
    elif season_type == "Postseason":
        home_record = get_playoff_record(espn_game_json, is_home=True)
        away_record = get_playoff_record(espn_game_json, is_home=False)
    return home_record, away_record


def get_playoff_record(espn_game_json, is_home: bool):
    try:
        home_playoff_record = str(espn_game_json['competitions'][0]['series']['competitors'][0]['wins'])
        away_playoff_record = str(espn_game_json['competitions'][0]['series']['competitors'][1]['wins'])
        return home_playoff_record + "-" + away_playoff_record if is_home else away_playoff_record + "-" + home_playoff_record
    except:
        return ""


def parse_gameclock(sport, espn_game_json: dict):
    game_situation = parse_game_situation(espn_game_json)
    game_status = espn_game_json.get('status').get('type')
    game_status_desc = game_status.get('name')

    if not game_status_desc:
        return None

    time_state = None
    live_clock = None
    live_period = None
    start_time = None
    if game_status_desc == 'STATUS_IN_PROGRESS' or game_status_desc == 'STATUS_HALFTIME' or game_status_desc == 'STATUS_END_PERIOD':
        time_state = TimeState.LIVE
        live_clock = espn_game_json.get('status').get('displayClock')
        live_period = espn_game_json.get('status').get('period')
        # NFL Halftime
        if sport == Sport.NFL and live_clock == '0:00' and live_period == 2:
            live_clock = 'HALF'
            live_period = ''
    elif game_status_desc == 'STATUS_FINAL':
        time_state = TimeState.FINAL
    elif game_status_desc == 'STATUS_SCHEDULED':
        time_state = TimeState.SCHEDULED
        # Short detail: 11/21 - 8:15 PM EST
        time_in_est = game_status.get('shortDetail').split(' - ', 1)[1][:-3] # 8:15 PM
        month_and_day = game_status.get('shortDetail').split(' - ', 1)[0]
        month = month_and_day.split('/', 1)[0]
        day = month_and_day.split('/', 1)[1]
        current_year = str(datetime.date.today().year)
        date_obj = datetime.datetime.strptime(current_year + '-' + month + '-' + day, "%Y-%m-%d")
        day_name = calendar.day_name[date_obj.weekday()][:3].upper()  # 'SUN'
        start_time = time_in_est + day_name
    else:
        print("Unknown game_status_desc: " + game_status_desc) # New one: STATUS_END_PERIOD
    if time_state:
        return GameClock(time_state, start_time, live_clock, live_period, game_situation=game_situation)
    return None


def parse_game_situation(espn_game_json):
    ball_on_team = None
    down_distance_text = None
    if espn_game_json['competitions'][0].get('situation'):
        down_distance_text = espn_game_json['competitions'][0].get('situation').get('shortDownDistanceText')
        possession_text = espn_game_json['competitions'][0].get('situation').get('possessionText') # possessionText: "ATL 18"
        if possession_text:
            ball_on_team = possession_text.split()[0]
        else:
            return None
        ball_on_yardline = espn_game_json['competitions'][0].get('situation').get('yardLine') # "yardLine": 18, yardline: 72
        if ball_on_yardline > 50:
            ball_on_yardline = 100 - ball_on_yardline
    else:
        return None

    if espn_game_json['competitions'][0]['competitors'][0]['homeAway'] == 'home':
        home_team_id = espn_game_json['competitions'][0]['competitors'][0]['id']
        # away_team_id = espn_game_json['competitions'][0]['competitors'][1]['id']
    else:
        home_team_id = espn_game_json['competitions'][0]['competitors'][1]['id']

    team_id_in_possession = espn_game_json['competitions'][0].get('situation').get('possession')
    if team_id_in_possession == str(home_team_id):
        print("Home team possessing")
        home_team_has_ball = True
        away_team_has_ball = False
    else:
        home_team_has_ball = False
        away_team_has_ball = True
    return GameSituation(down_and_distance=down_distance_text, home_team_has_ball=home_team_has_ball,
                         away_team_has_ball=away_team_has_ball, ball_on_yardline=ball_on_yardline, ball_on_team=ball_on_team)