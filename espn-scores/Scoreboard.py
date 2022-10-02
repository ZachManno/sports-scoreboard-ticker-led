from enum import Enum


class TimeState(Enum):
    PAST = 1
    LIVE = 2
    UPCOMING = 3


class GameClock:
    def __init__(self, time_state: TimeState, start_time: str = None,
                 live_clock_time: str = None, live_period: str = None):
        self.time_state = time_state
        self.start_time = start_time
        self.live_clock_time = live_clock_time
        self.live_period = live_period

    @property
    def time_state(self):
        return self.time_state

    @time_state.setter
    def time_state(self, value):
        self._time_state = value

    @property
    def start_time(self):
        return self.start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def live_clock_time(self):
        return self.live_clock_time

    @live_clock_time.setter
    def live_clock_time(self, value):
        self._live_clock_time = value

    @property
    def live_period(self):
        return self.live_clock_time

    @live_period.setter
    def live_period(self, value):
        self._live_clock_time = value


class Team:
    def __init__(self, city_abbr: str, wins: int, losses: int, ties: int):
        self.city_abbr = city_abbr
        self.wins = wins
        self.losses = losses
        self.ties = ties

    @property
    def city_abbr(self):
        return self.city_abbr

    @city_abbr.setter
    def city_abbr(self, value):
        self._city_abbr = value

    @property
    def wins(self):
        return self.wins

    @wins.setter
    def wins(self, value):
        self._wins = value

    @property
    def losses(self):
        return self.losses

    @losses.setter
    def losses(self, value):
        self._losses = value

    @property
    def ties(self):
        return self.ties

    @ties.setter
    def ties(self, value):
        self._ties = value


class Scoreboard:
    def __init__(self, away_team: str, home_team: str, gameclock: GameClock):
        self.away_team = away_team
        self.home_team = home_team
        self.gameclock = gameclock

    @property
    def away_team(self):
        return self.away_team

    @away_team.setter
    def away_team(self, value):
        self._away_team = value
