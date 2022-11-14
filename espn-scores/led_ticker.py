#!/usr/bin/env python3
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import platform
from espn_runner import call_espn_api_and_load_scoreboard
from Scoreboard import TimeState
from threading import Timer

quarter_map = {1: '1ST', 2: '2ND', 3: '3RD', 4: '4TH'}


class GraphicsRunner(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsRunner, self).__init__(*args, **kwargs)

    def run(self):
        rotation = 0
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        self.matrix.brightness = 50
        # print('brightness: ' + str(self.matrix.brightness))
        #canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("font/5x7.bdf")

        green = graphics.Color(0, 255, 0)
        #graphics.DrawCircle(canvas, 15, 15, 10, green)

        blue = graphics.Color(0, 255, 213)

        yellow = graphics.Color(255, 255, 0)

        while True:
            for scoreboard in call_espn_api_and_load_scoreboard():
                home_score = scoreboard.home_team.score
                home_name = scoreboard.home_team.city_abbr
                if len(home_name) == 2:
                    home_name += ' '
                away_name = scoreboard.away_team.city_abbr
                if len(away_name) == 2:
                    away_name += ' '
                away_score = scoreboard.away_team.score
                #home_score = "PHI 32"
                #away_score = "MIN 22"
                #final = "FINAL"
                if rotation % 2 == 0:
                    graphics.DrawText(offscreen_canvas, font, 2, 9, blue, home_name + ' ' + home_score)
                    graphics.DrawText(offscreen_canvas, font, 2, 20, blue, away_name + ' ' + away_score)
                    if scoreboard.gameclock.time_state and scoreboard.gameclock.time_state == TimeState.FINAL:
                        graphics.DrawText(offscreen_canvas, font, 2, 30, blue, 'FINAL')
                    elif scoreboard.gameclock.time_state and scoreboard.gameclock.time_state == TimeState.LIVE:
                        if scoreboard.gameclock.live_clock == 'HALF':
                            gameclock = 'HALF'
                        else:
                            gameclock = quarter_map[scoreboard.gameclock.live_period] + ' ' + scoreboard.gameclock.live_clock
                        graphics.DrawText(offscreen_canvas, font, 2, 30, blue, gameclock)
                else:
                    #home_score = "HHI 32"
                    #away_score = "NNN 22"
                    #final = "FINAL"
                    graphics.DrawText(offscreen_canvas, font, 2, 9, green, home_name + ' ' + home_score)
                    graphics.DrawText(offscreen_canvas, font, 2, 20, green, away_name + ' ' + away_score)
                    if scoreboard.gameclock.time_state == TimeState.FINAL:
                        graphics.DrawText(offscreen_canvas, font, 2, 30, green, 'FINAL')
                    elif scoreboard.gameclock.time_state == TimeState.LIVE:
                        if scoreboard.gameclock.live_clock == 'HALF':
                            gameclock = 'HALF'
                        graphics.DrawText(offscreen_canvas, font, 2, 30, green, gameclock)

                # graphics.DrawText(offscreen_canvas, weather_font, 40, 6, yellow, self.philly_weather.condition.text)
                # graphics.DrawText(offscreen_canvas, weather_font, 55, 13, yellow, str(self.philly_weather.condition.temperature))
                rotation = rotation + 1
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