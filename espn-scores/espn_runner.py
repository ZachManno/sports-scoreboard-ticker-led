import requests
from requests.adapters import HTTPAdapter, Retry
import time
from espn_json_helper import inSeason
from espn_data_parser import parse_espn_api_json


def get_espn_api_configs():
    # Set API URLs from https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b
    base_url = "http://site.api.espn.com/apis/site/v2/sports/"

    sport_config_dict = {"MLB": {"url": base_url + "baseball/mlb/scoreboard", "level": "PRO"},
                         "NFL": {"url": base_url + "football/nfl/scoreboard", "level": "PRO"},
                         "NBA": {"url": base_url + "basketball/nba/scoreboard", "level": "PRO"},
                         "NHL": {"url": base_url + "hockey/nhl/scoreboard", "level": "PRO"},
                         "NCAAM": {"url": base_url + "basketball/mens-college-basketball/scoreboard", "level": "COLLEGE"},
                         "NCAAF": {"url": base_url + "football/college-football/scoreboard", "level": "COLLEGE"}}
    return sport_config_dict


def call_espn_api_and_load_scoreboard():
    sport_config_dict = get_espn_api_configs()
    current_scoreboards_list = []

    # Only do NFL for now
    for sport_config in [sport_config_dict['NFL']]:
        # Query API
        espn_response = call_api(sport_config['url'])
        espn_data = espn_response.json()
        # Determine if InSeason and Display
        if inSeason(espn_data) is True:
            # Get Teams and Score
            for game in espn_data['events']:
                current_scoreboards_list.append(parse_espn_api_json('NFL', game, espn_data))
        for scoreboard in current_scoreboards_list:
            print(str(scoreboard))
    return current_scoreboards_list


def call_api(url):
    sess = requests.Session()

    retries = Retry(total=7,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    sess.mount('http://', HTTPAdapter(max_retries=retries))

    return sess.get(url)


if __name__ == "__main__":
    call_espn_api_and_load_scoreboard()
