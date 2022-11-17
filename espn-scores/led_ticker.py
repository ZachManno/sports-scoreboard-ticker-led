#!/usr/bin/env python3
from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image
import time
import platform
from espn_runner import call_espn_api_and_load_scoreboard
from Scoreboard import TimeState
from threading import Timer

quarter_map = {1: '1ST', 2: '2ND', 3: '3RD', 4: '4TH'}


class GraphicsRunner(SampleBase):
    def __init__(self, *args, **kwargs):
        self.smallest_font = graphics.Font()
        self.smallest_font.LoadFont("font/4x6.bdf")
        self.medium_font = graphics.Font()
        self.medium_font.LoadFont("font/5x7.bdf")
        self.green = graphics.Color(0, 255, 0)
        self.blue = graphics.Color(0, 255, 213)
        self.yellow = graphics.Color(255, 255, 0)
        self.white = graphics.Color(255, 255, 255)
        super(GraphicsRunner, self).__init__(*args, **kwargs)

    @staticmethod
    def format_team_abbr(team_abbr):
        if len(team_abbr) == 2:
            team_abbr += ' '
        return team_abbr

    def draw_image(self, offscreen_canvas):
        image = Image.open('images/nfl-2.png').convert('RGB')
        image.thumbnail((16, 16), Image.ANTIALIAS)
        offscreen_canvas.SetImage(image, 50)
        print()

    def write_scoreboard(self, offscreen_canvas, color, scoreboard):
        # Home
        if scoreboard.gameclock.time_state != TimeState.SCHEDULED:
            graphics.DrawText(offscreen_canvas, self.medium_font, 2, 9, color,
                          self.format_team_abbr(scoreboard.home_team.city_abbr) + ' ' + scoreboard.home_team.score)
        graphics.DrawText(offscreen_canvas, self.smallest_font, 33, 9, self.white, scoreboard.home_team.record)
        # graphics.DrawText(offscreen_canvas, self.medium_font, 70, 9, self.yellow, '1st and 10')

        # Away
        if scoreboard.gameclock.time_state != TimeState.SCHEDULED:
            graphics.DrawText(offscreen_canvas, self.medium_font, 2, 20, color,
                          self.format_team_abbr(scoreboard.away_team.city_abbr) + ' ' + scoreboard.away_team.score)
        graphics.DrawText(offscreen_canvas, self.smallest_font, 33, 20, self.white, scoreboard.away_team.record)
        if scoreboard.gameclock.time_state:
            if scoreboard.gameclock.time_state == TimeState.FINAL:
                graphics.DrawText(offscreen_canvas, self.medium_font, 2, 30, color, 'FINAL')
            elif scoreboard.gameclock.time_state == TimeState.LIVE:
                gameclock = quarter_map[scoreboard.gameclock.live_period] + ' ' + scoreboard.gameclock.live_clock
                graphics.DrawText(offscreen_canvas, self.medium_font, 2, 30, color, gameclock)
            elif scoreboard.gameclock.time_state == TimeState.SCHEDULED:
                graphics.DrawText(offscreen_canvas, self.medium_font, 2, 30, color, scoreboard.gameclock.start_time)
        if len(scoreboard.home_team.record) < 5 and len(scoreboard.away_team.record) < 5:
            self.draw_image(offscreen_canvas)

    def run(self):
        rotation = 0
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.matrix.brightness = 50
        # print('brightness: ' + str(self.matrix.brightness))

        while True:
            for scoreboard in call_espn_api_and_load_scoreboard():
                if rotation % 2 == 0:
                    self.write_scoreboard(offscreen_canvas, self.blue, scoreboard)
                else:
                    self.write_scoreboard(offscreen_canvas, self.green, scoreboard)

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