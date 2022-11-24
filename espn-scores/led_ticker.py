#!/usr/bin/env python3
from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image
import time
import math
import platform
from espn_runner import call_espn_api_and_load_scoreboard
from Scoreboard import TimeState
from Scoreboard import GameSituation
from threading import Timer

QUARTER_MAP = {1: '1ST', 2: '2ND', 3: '3RD', 4: '4TH'}
YARDLINE_TO_X_AXIS_MAP = {5: 70, 10: 15, 35: 80, 40: 85, 45: 90, 50: 95}
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
        self.dark_blue = graphics.Color(0, 0, 255)
        self.red = graphics.Color(255, 51, 0)
        self.purple = graphics.Color(153, 51, 255)
        self.yellow = graphics.Color(255, 255, 0)
        self.white = graphics.Color(255, 255, 255)
        self.brown = graphics.Color(204, 102, 0)
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

    def draw_team_image(self, offscreen_canvas, image_location, x_axis_position, size, y_axis_position=None):
        image = Image.open(image_location).convert('RGB')
        image.thumbnail((size, size), Image.ANTIALIAS)
        if y_axis_position:
            offscreen_canvas.SetImage(image, x_axis_position, y_axis_position)
        else:
            offscreen_canvas.SetImage(image, x_axis_position)

    def write_team_and_record(self, offscreen_canvas, color, team_abbr_and_possible_score, record_column, record_row,
                              record):
        graphics.DrawText(offscreen_canvas, self.medium_font, BEGINNING_COLUMN, record_row, color,
                          team_abbr_and_possible_score)
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
        # self.draw_team_image(offscreen_canvas, f'images/nfl/{scoreboard.away_team.city_abbr.upper()}.png', 66, 24)
        # graphics.DrawText(offscreen_canvas, self.huge_font, 94, 16, self.yellow, '@')
        # self.draw_team_image(offscreen_canvas, f'images/nfl/{scoreboard.home_team.city_abbr.upper()}.png', 104, 24)

        # Test drawing field goal posts and green
        scoreboard.gameclock.game_situation = GameSituation(down_and_distance="3rd and 7", home_team_has_ball=True,
                                                            away_team_has_ball=False, ball_on_yardline=10,
                                                            ball_on_team='BUF')
        self.draw_football_field(offscreen_canvas, scoreboard)

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
            graphics.DrawText(offscreen_canvas, self.large_font, 72, 16, self.yellow,
                              scoreboard.gameclock.down_and_distance)

    def write_final_scoreboard(self, offscreen_canvas, color, scoreboard):
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

    def draw_football_field(self, offscreen_canvas, scoreboard):
        graphics.DrawLine(offscreen_canvas, 70, 30, 121, 30, self.green)  # Green line at bottom of screen
        graphics.DrawLine(offscreen_canvas, 70, 31, 121, 31, self.green)  # Green line at bottom of screen
        graphics.DrawLine(offscreen_canvas, 69, 31, 69, 30, self.white)  # two dots of white for endzone
        graphics.DrawLine(offscreen_canvas, 68, 31, 68, 30, self.red)  # red endzone
        graphics.DrawLine(offscreen_canvas, 67, 31, 67, 30, self.red)  # red endzone
        graphics.DrawLine(offscreen_canvas, 66, 31, 66, 28, self.yellow)  # goal post left
        graphics.DrawLine(offscreen_canvas, 64, 28, 64, 24, self.yellow)  # goal post left
        graphics.DrawLine(offscreen_canvas, 68, 28, 68, 25, self.yellow)  # goal post left
        graphics.DrawLine(offscreen_canvas, 65, 28, 65, 28, self.yellow)  # goal post left
        graphics.DrawLine(offscreen_canvas, 67, 28, 67, 28, self.yellow)  # goal post left

        graphics.DrawLine(offscreen_canvas, 95, 31, 95, 30, self.white)  # white midfield
        graphics.DrawLine(offscreen_canvas, 96, 31, 96, 30, self.white)  # white midfield

        right_shift_goalpost = 59
        right_shift_endzone_white = 53
        right_shift_endzone_blue = 56
        graphics.DrawLine(offscreen_canvas, 69 + right_shift_endzone_white, 31, 69 + right_shift_endzone_white, 30,
                          self.white)  # two dots of white for endzone
        graphics.DrawLine(offscreen_canvas, 68 + right_shift_endzone_blue, 31, 68 + right_shift_endzone_blue, 30,
                          self.purple)  # purple endzone
        graphics.DrawLine(offscreen_canvas, 68 + right_shift_endzone_blue - 1, 31, 68 + right_shift_endzone_blue - 1,
                          30, self.purple)  # purple endzone
        graphics.DrawLine(offscreen_canvas, 66 + right_shift_goalpost, 31, 66 + right_shift_goalpost, 28,
                          self.yellow)  # goal post right
        graphics.DrawLine(offscreen_canvas, 64 + right_shift_goalpost, 28, 64 + right_shift_goalpost, 24 + 1,
                          self.yellow)  # goal post right, invert post
        graphics.DrawLine(offscreen_canvas, 68 + right_shift_goalpost, 28, 68 + right_shift_goalpost, 25 - 1,
                          self.yellow)  # goal post right, invert post
        graphics.DrawLine(offscreen_canvas, 65 + right_shift_goalpost, 28, 65 + right_shift_goalpost, 28,
                          self.yellow)  # goal post right
        graphics.DrawLine(offscreen_canvas, 67 + right_shift_goalpost, 28, 67 + right_shift_goalpost, 28,
                          self.yellow)  # goal post right

        self.draw_possession(offscreen_canvas, scoreboard)  # 96 is fifty yardline
        # self.draw_possession(offscreen_canvas, 18, 'RIGHT')  # 96 is fifty yardline

    def draw_possession(self, offscreen_canvas, scoreboard):
        if not scoreboard.gameclock.game_situation:
            return

        yardline = scoreboard.gameclock.game_situation.ball_on_yardline

        field_direction = 'LEFT_TO_RIGHT'
        if scoreboard.gameclock.game_situation.ball_on_team == scoreboard.away_team.city_abbr:
            field_direction = 'LEFT_TO_RIGHT'
        else:
            field_direction = 'RIGHT_TO_LEFT'

        starting_position = scoreboard.gameclock.game_situation.ball_on_yardline / 2.05
        if field_direction == 'LEFT_TO_RIGHT':
            starting_position = math.floor(starting_position + 70)
        else:
            starting_position = math.floor(122 - starting_position)

        if len(str(yardline)) == 1:
            yardline_is_one_char = True
        else:
            yardline_is_one_char = False
        self.draw_possession_arrow(offscreen_canvas, scoreboard, yardline_is_one_char, starting_position)
        # Draw football
        graphics.DrawLine(offscreen_canvas, starting_position - 1, 29, starting_position + 1, 29, self.brown)
        graphics.DrawLine(offscreen_canvas, starting_position - 1, 27, starting_position + 1, 27, self.brown)
        graphics.DrawLine(offscreen_canvas, starting_position - 2, 28, starting_position - 1, 28, self.brown)
        graphics.DrawLine(offscreen_canvas, starting_position + 1, 28, starting_position + 2, 28, self.brown)

        # Draw yardline
        if yardline_is_one_char:
            starting_position_of_yardline = starting_position - 1
        else:
            starting_position_of_yardline = starting_position - 2
        graphics.DrawText(offscreen_canvas, self.smallest_font, starting_position_of_yardline, 26, self.blue,
                          str(yardline))

        # Team Logos
        self.draw_team_image(offscreen_canvas, f'images/nfl/{scoreboard.away_team.city_abbr.upper()}.png', 64, 11, 10)
        self.draw_team_image(offscreen_canvas, f'images/nfl/{scoreboard.home_team.city_abbr.upper()}.png', 116, 11, 10)

    def draw_possession_arrow(self, offscreen_canvas, scoreboard, yardline_is_one_char, starting_position):
        direction = 'LEFT_TO_THE_LEFT' # TODO: remove
        print('home_team_has_ball: ', scoreboard.gameclock.game_situation.home_team_has_ball)
        print('ball_on_team: ', scoreboard.gameclock.game_situation.ball_on_team)
        print('home_team_city_abbr: ', scoreboard.home_team.city_abbr)
        # Away team has ball on their own side of the field
        if scoreboard.gameclock.game_situation.away_team_has_ball and \
                scoreboard.gameclock.game_situation.ball_on_team == scoreboard.away_team.city_abbr:
            direction = "RIGHT_TO_THE_RIGHT"
        # Away team has ball on the opposing team's side of the field
        if scoreboard.gameclock.game_situation.away_team_has_ball and \
                scoreboard.gameclock.game_situation.ball_on_team != scoreboard.away_team.city_abbr:
            direction = "RIGHT_TO_THE_RIGHT"
            if yardline_is_one_char:  # Home team about to score, flip the arrow on the other side so it doesn't overwrite goalpost
                direction = "RIGHT_TO_THE_LEFT"
        # Home team has ball on their own side
        if scoreboard.gameclock.game_situation.home_team_has_ball and \
                scoreboard.gameclock.game_situation.ball_on_team == scoreboard.home_team.city_abbr:
            direction = "LEFT_TO_THE_LEFT"
        # Home team has ball on opposing team's side of field
        if scoreboard.gameclock.game_situation.home_team_has_ball and \
                scoreboard.gameclock.game_situation.ball_on_team != scoreboard.home_team.city_abbr:
            direction = "LEFT_TO_THE_LEFT"
            print("HERE7, yardline0nechar: ", yardline_is_one_char)
            if yardline_is_one_char:  # Home team about to score, flip the arrow on the other side so it doesn't overwrite goalpost
                direction = "LEFT_TO_THE_RIGHT"

        if direction == 'LEFT_TO_THE_LEFT':
            print('LEFT_TO_THE_LEFT')
            self.draw_left_arrow(offscreen_canvas, starting_position - 4)
        elif direction == 'LEFT_TO_THE_RIGHT':
            self.draw_left_arrow(offscreen_canvas, starting_position + 4)
        elif direction == 'RIGHT_TO_THE_RIGHT':
            self.draw_right_arrow(offscreen_canvas, starting_position + 4)
        elif direction == 'RIGHT_TO_THE_LEFT':
            self.draw_right_arrow(offscreen_canvas, starting_position - 4)

    def draw_left_arrow(self, offscreen_canvas, arrow_starting_position):
        graphics.DrawLine(offscreen_canvas, arrow_starting_position, 27, arrow_starting_position, 23, self.white)
        graphics.DrawLine(offscreen_canvas, arrow_starting_position - 1, 26, arrow_starting_position - 1, 24,
                          self.white)
        graphics.DrawLine(offscreen_canvas, arrow_starting_position - 2, 25, arrow_starting_position - 2, 25,
                          self.white)

    def draw_right_arrow(self, offscreen_canvas, arrow_starting_position):
        graphics.DrawLine(offscreen_canvas, arrow_starting_position, 27, arrow_starting_position, 23, self.white)
        graphics.DrawLine(offscreen_canvas, arrow_starting_position + 1, 26, arrow_starting_position + 1, 24,
                          self.white)
        graphics.DrawLine(offscreen_canvas, arrow_starting_position + 2, 25, arrow_starting_position + 2, 25,
                          self.white)


# Main function
if __name__ == "__main__":
    graphics_runner = GraphicsRunner()
    # My "just get it working" solution after digging through python in-program cron scheduling forums:
    # weather_update_interval = 900.0 #every 15 mins = 900.0
    # for i in range(16): # 16 weather updates = assumes program runs for at max 4 hours. Also creates 16 threads
    #     Timer(weather_update_interval * i, graphics_runner.refresh_weather).start()
    if (not graphics_runner.process()):
        graphics_runner.print_help()
