from enum import Enum
import typing


def parse_espn_api_json(sport: str, espn_json: dict):
    # print('here: ' + sport + ' ,' + str(espn_json))
    home, away = parse_home_and_away(espn_json)
    gameclock = parse_gameclock(Sport[sport.upper()], espn_json)
    scoreboard = Scoreboard(Sport[sport.upper()], home, away, gameclock)
    print('scoreboard: ', str(scoreboard))


def parse_home_and_away(espn_json: dict):
    home_json = espn_json['competitions'][0]['competitors'][0]
    home_team_name = home_json['team']['abbreviation']
    home_score = home_json.get('score', None)
    home_record = home_json['records'][0]['summary']
    home = Team(home_team_name, home_record, home_score)

    away_json = espn_json['competitions'][0]['competitors'][1]
    away_team_name = away_json['team']['abbreviation']
    away_score = away_json.get('score', None)
    away_record = away_json['records'][0]['summary']
    away = Team(away_team_name, away_record, away_score)
    return home, away


def parse_gameclock(sport, espn_json: dict):
    game_status = espn_json.get('status').get('type')
    game_status_desc = game_status.get('name')

    if not game_status_desc:
        return None

    time_state = None
    live_clock = None
    live_period = None
    start_time = None
    if game_status_desc == 'STATUS_IN_PROGRESS' or game_status_desc == 'STATUS_HALFTIME':
        time_state = TimeState.LIVE
        live_clock = espn_json.get('status').get('displayClock')
        live_period = espn_json.get('status').get('period')
        # NFL Halftime
        if sport == Sport.NFL and live_clock == '0:00' and live_period == 2:
            live_clock = 'HALF'
    elif game_status_desc == 'STATUS_FINAL':
        time_state = TimeState.FINAL
    elif game_status_desc == 'STATUS_SCHEDULED':
        time_state = TimeState.SCHEDULED
        start_time = game_status.get('shortDetail')
    else:
        print("Unknown game_status_desc: " + game_status_desc)
    if time_state:
        return GameClock(time_state, start_time, live_clock, live_period)
    return None


class SeasonType(Enum):
    REGULAR = 1
    POSTSEASON = 2


class Sport(Enum):
    MLB = 1
    NBA = 2
    NFL = 3


class TimeState(Enum):
    FINAL = 1
    LIVE = 2
    SCHEDULED = 3


class GameClock:
    def __init__(self, time_state: TimeState, start_time: str = None,
                 live_clock: str = None, live_period: str = None):
        self.time_state = time_state
        self.start_time = start_time
        self.live_clock = live_clock
        self.live_period = live_period

    @property
    def time_state(self):
        return self._time_state

    @time_state.setter
    def time_state(self, value):
        self._time_state = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def live_clock(self):
        return self._live_clock

    @live_clock.setter
    def live_clock(self, value):
        self._live_clock = value

    @property
    def live_period(self):
        return self._live_clock_time

    @live_period.setter
    def live_period(self, value):
        self._live_clock_time = value

    def __str__(self):
        return str({'time_state': self.time_state, 'start_time': self.start_time,
                    'live_clock': self.live_clock, 'live_period': self.live_period})


class Team:
    def __init__(self, city_abbr: str, record: str, score: typing.Optional[int] = None):
        self.city_abbr = city_abbr
        self.record = record
        self.score = score

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def city_abbr(self):
        return self._city_abbr

    @city_abbr.setter
    def city_abbr(self, value):
        self._city_abbr = value

    @property
    def record(self):
        return self._record

    @record.setter
    def record(self, value):
        self._record = value

    def __str__(self):
        return str({'city_abbr': self.city_abbr, 'record': self.record, 'score': self.score})


class Scoreboard:
    def __init__(self, sport: Sport, home_team: Team, away_team: Team, gameclock: GameClock):
        self.sport = sport
        self.home_team = home_team
        self.away_team = away_team
        self.gameclock = gameclock

    @property
    def sport(self):
        return self._sport

    @sport.setter
    def sport(self, value):
        self._sport = value

    @property
    def away_team(self):
        return self._away_team

    @away_team.setter
    def away_team(self, value):
        self._away_team = value

    @property
    def home_team(self):
        return self._home_team

    @home_team.setter
    def home_team(self, value):
        self._home_team = value

    def __str__(self):
        return str({'sport': self.sport, 'home_team': str(self.home_team),
                    'away_team': str(self.away_team), 'gameclock': str(self.gameclock)})
