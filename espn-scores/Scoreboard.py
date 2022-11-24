from enum import Enum
import typing


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


class GameSituation:
    def __init__(self, down_and_distance: str = None,
                 home_team_has_ball: bool = None, away_team_has_ball: bool = None,
                 ball_on_yardline: int = None, ball_on_team: str = None):
        self.down_and_distance = down_and_distance
        self.home_team_has_ball = home_team_has_ball
        self.away_team_has_ball = away_team_has_ball
        self.ball_on_yardline = ball_on_yardline
        self.ball_on_team = ball_on_team

    @property
    def down_and_distance(self):
        return self._down_and_distance

    @down_and_distance.setter
    def down_and_distance(self, value):
        self._down_and_distance = value

    @property
    def home_team_has_ball(self):
        return self._home_team_has_ball

    @home_team_has_ball.setter
    def home_team_has_ball(self, value):
        self._home_team_has_ball = value

    @property
    def away_team_has_ball(self):
        return self._away_team_has_ball

    @away_team_has_ball.setter
    def away_team_has_ball(self, value):
        self._away_team_has_ball = value

    @property
    def ball_on_yardline(self):
        return self._ball_on_yardline

    @ball_on_yardline.setter
    def ball_on_yardline(self, value):
        self._ball_on_yardline = value

    @property
    def ball_on_team(self):
        return self._ball_on_team

    @ball_on_team.setter
    def ball_on_team(self, value):
        self._ball_on_team = value

    def __str__(self):
        return str({'down_and_distance': self.down_and_distance, 'home_team_has_ball': self.home_team_has_ball,
                    'away_team_has_ball': self.away_team_has_ball, 'ball_on_yardline': self.ball_on_yardline,
                    'ball_on_team': self.ball_on_team})


class GameClock:
    def __init__(self, time_state: TimeState, start_time: str = None,
                 live_clock: str = None, live_period: str = None, game_situation: GameSituation = None):
        self.time_state = time_state
        self.start_time = start_time
        self.live_clock = live_clock
        self.live_period = live_period
        self.game_situation = game_situation

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

    @property
    def game_situation(self):
        return self._game_situation

    @game_situation.setter
    def game_situation(self, value):
        self._game_situation = value

    def __str__(self):
        return str({'time_state': self.time_state, 'start_time': self.start_time,
                    'live_clock': self.live_clock, 'live_period': self.live_period,
                    'game_situation': str(self.game_situation)})


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
