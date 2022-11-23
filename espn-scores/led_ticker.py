#!/usr/bin/env python3
from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image
import time
import platform
from espn_runner import call_espn_api_and_load_scoreboard
from Scoreboard import TimeState
from threading import Timer

QUARTER_MAP = {1: '1ST', 2: '2ND', 3: '3RD', 4: '4TH'}
BEGINNING_COLUMN = 2


class GraphicsRunner(SampleBase):
    def __init__(self, *args, **kwargs):
        self.smallest_font = graphics.Font()
        self.smallest_font.LoadFont("font/4x6.bdf")
        self.medium_font = graphics.Font()
        self.medium_font.LoadFont("font/5x7.bdf")
        self.large_font = graphics.Font()
        self.large_font.LoadFont("font/6x10.bdf")
        self.huge_font = graphics.Font()
        self.huge_font.LoadFont("font/7x13.bdf")
        self.green = graphics.Color(0, 255, 0)
        self.blue = graphics.Color(0, 255, 213)
        self.dark_blue = graphics.Color(0, 0, 204)
        self.yellow = graphics.Color(255, 255, 0)
        self.white = graphics.Color(255, 255, 255)
        super(GraphicsRunner, self).__init__(*args, **kwargs)

    @staticmethod
    def format_team_abbr(team_abbr):
        if len(team_abbr) == 2:
            team_abbr += ' '
        return team_abbr

    def draw_nfl_image(self, offscreen_canvas):
        image = Image.open('images/nfl-2.png').convert('RGB')
        image.thumbnail((16, 16), Image.ANTIALIAS)
        offscreen_canvas.SetImage(image, 50)

    def draw_nfl_image_if_space(self, offscreen_canvas, scoreboard):
        if len(scoreboard.home_team.record) < 5 and len(scoreboard.away_team.record) < 5:
            self.draw_nfl_image(offscreen_canvas)

    def draw_team_image(self, offscreen_canvas, image_location, x_axis_position):
        image = Image.open(image_location).convert('RGB')
        image.thumbnail((24, 24), Image.ANTIALIAS)
        offscreen_canvas.SetImage(image, x_axis_position)

    def write_team_and_record(self, offscreen_canvas, color, team_abbr_and_possible_score, record_column, record_row, record):
        graphics.DrawText(offscreen_canvas, self.medium_font, BEGINNING_COLUMN, record_row, color, team_abbr_and_possible_score)
        graphics.DrawText(offscreen_canvas, self.smallest_font, record_column, record_row, self.white, record)

    def write_scheduled_scoreboard(self, offscreen_canvas, color, scoreboard):
        record_location = 20
        # Write away team and record
        graphics.DrawText(offscreen_canvas, self.medium_font, 2, 9, color,
                          self.format_team_abbr(scoreboard.away_team.city_abbr))
        graphics.DrawText(offscreen_canvas, self.smallest_font, record_location, 9, self.white,
                          scoreboard.away_team.record)
        self.write_team_and_record(offscreen_canvas, color,
                                   self.format_team_abbr(scoreboard.away_team.city_abbr),
                                   record_location, 9, scoreboard.away_team.record)

        # Write home team and record
        self.write_team_and_record(offscreen_canvas, color,
                                   self.format_team_abbr(scoreboard.home_team.city_abbr),
                                   record_location, 20, scoreboard.home_team.record)

        # Write start time
        graphics.DrawText(offscreen_canvas, self.medium_font, 2, 30, color, scoreboard.gameclock.start_time)

        # Write home and away logos
        # self.draw_team_image(offscreen_canvas, f'images/nfl/{scoreboard.away_team.city_abbr.upper()}.png', 66)
        # graphics.DrawText(offscreen_canvas, self.huge_font, 94, 16, self.yellow, '@')
        # self.draw_team_image(offscreen_canvas, f'images/nfl/{scoreboard.home_team.city_abbr.upper()}.png', 104)

        # Test drawing field goal posts and green
        graphics.DrawLine(offscreen_canvas, 70, 30, 121, 30, self.green)  # Green line at bottom of screen
        graphics.DrawLine(offscreen_canvas, 70, 31, 121, 31, self.green) # Green line at bottom of screen
        graphics.DrawLine(offscreen_canvas, 69, 31, 69, 30, self.white)  # two dots of white for endzone
        graphics.DrawLine(offscreen_canvas, 68, 31, 68, 30, self.dark_blue)  # blue endzone
        graphics.DrawLine(offscreen_canvas, 67, 31, 67, 30, self.dark_blue)  # blue endzone
        graphics.DrawLine(offscreen_canvas, 66, 31, 66, 28, self.yellow)  # goal post
        graphics.DrawLine(offscreen_canvas, 64, 28, 64, 24, self.yellow)  # goal post
        graphics.DrawLine(offscreen_canvas, 68, 28, 68, 25, self.yellow)  # goal post

        # Write NFL logo in top right
        self.draw_nfl_image(offscreen_canvas)

    def write_live_scoreboard(self, offscreen_canvas, color, scoreboard):
        record_location = 33
        # Write away team, score and record
        self.write_team_and_record(offscreen_canvas, color,
                                   self.format_team_abbr(
                                       scoreboard.away_team.city_abbr) + ' ' + scoreboard.away_team.score,
                                   record_location, 9, scoreboard.away_team.record)

        # Write home team, score and record
        self.write_team_and_record(offscreen_canvas, color,
                                   self.format_team_abbr(
                                       scoreboard.home_team.city_abbr) + ' ' + scoreboard.home_team.score,
                                   record_location, 20, scoreboard.home_team.record)

        # Write live score and clock
        gameclock = QUARTER_MAP.get(scoreboard.gameclock.live_period, '') + ' ' + scoreboard.gameclock.live_clock
        graphics.DrawText(offscreen_canvas, self.medium_font, 2, 30, color, gameclock)

        self.draw_nfl_image_if_space(offscreen_canvas, scoreboard)

        # Write down and distance if applicable
        if scoreboard.gameclock.down_and_distance:
            graphics.DrawText(offscreen_canvas, self.large_font, 72, 16, self.yellow, scoreboard.gameclock.down_and_distance)

    def write_final_scoreboard(self, offscreen_canvas, color, scoreboard):
        record_location = 33
        # Write away team, score and record
        self.write_team_and_record(offscreen_canvas, color,
                                   self.format_team_abbr(scoreboard.away_team.city_abbr) + ' ' + scoreboard.away_team.score,
                                   record_location, 9, scoreboard.away_team.record)

        # Write home team, score and record
        self.write_team_and_record(offscreen_canvas, color,
                                   self.format_team_abbr(scoreboard.home_team.city_abbr) + ' ' + scoreboard.home_team.score,
                                   record_location, 20, scoreboard.home_team.record)

        # Write FINAL
        graphics.DrawText(offscreen_canvas, self.medium_font, 2, 30, color, 'FINAL')

        self.draw_nfl_image_if_space(offscreen_canvas, scoreboard)

    def write_scoreboard(self, offscreen_canvas, color, scoreboard):
        if scoreboard.gameclock.time_state == TimeState.SCHEDULED:
            self.write_scheduled_scoreboard(offscreen_canvas, color, scoreboard)
        elif scoreboard.gameclock.time_state == TimeState.LIVE:
            self.write_live_scoreboard(offscreen_canvas, color, scoreboard)
        else:
            self.write_final_scoreboard(offscreen_canvas, color, scoreboard)

    def run(self):
        rotation = 0
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.matrix.brightness = 50
        # print('brightness: ' + str(self.matrix.brightness))

        while True:
            print()
            for scoreboard in call_espn_api_and_load_scoreboard():
                if rotation % 2 == 0:
                    self.write_scoreboard(offscreen_canvas, self.blue, scoreboard)
                else:
                    self.write_scoreboard(offscreen_canvas, self.green, scoreboard)

                # Rotates the colors between blue and green to  give some pizazz
                rotation = rotation + 1
                # Don't let rotation count get too high!
                if rotation == 90000:
                    rotation = 0
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                offscreen_canvas = self.matrix.CreateFrameCanvas()
                time.sleep(5)


# Main function
if __name__ == "__main__":
    graphics_runner = GraphicsRunner()
    # My "just get it working" solution after digging through python in-program cron scheduling forums:
    # weather_update_interval = 900.0 #every 15 mins = 900.0
    # for i in range(16): # 16 weather updates = assumes program runs for at max 4 hours. Also creates 16 threads
    #     Timer(weather_update_interval * i, graphics_runner.refresh_weather).start()
    if (not graphics_runner.process()):
        graphics_runner.print_help()