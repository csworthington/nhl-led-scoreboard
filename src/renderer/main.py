
from PIL import Image
from time import sleep
from datetime import datetime
import debug
from boards.boards import Boards
from boards.clock import Clock
from data.scoreboard import Scoreboard
from renderer.scoreboard import ScoreboardRenderer
from utils import get_file
import random
import glob



class MainRenderer:
    def __init__(self, matrix, data, sleepEvent):
        self.matrix = matrix
        self.data = data
        self.status = self.data.status
        self.refresh_rate = self.data.config.live_game_refresh_rate
        self.boards = Boards()
        self.sleepEvent = sleepEvent
        self.sog_display_frequency = data.config.sog_display_frequency
        self.alternate_data_counter = 1

    def render(self):
        while self.data.network_issues:
            Clock(self.data, self.matrix, self.sleepEvent, duration=60)
            self.data.refresh_data()

        while True:
            try:
                debug.info('Rendering...')
                self.data.refresh_data()
                if self.status.is_offseason(self.data.date()):
                    # Offseason (Show offseason related stuff)
                    debug.info("It's offseason")
                    self.__render_offday()
                else:
                    # Season.
                    if not self.data.config.live_mode:
                        debug.info("Live mode is off. Going through the boards")
                        self.__render_offday()
                    elif self.data.is_pref_team_offday():
                        debug.info("Your preferred teams are Off today")
                        self.__render_offday()
                    elif self.data.is_nhl_offday():
                        debug.info("There is no game in the NHL today")
                        self.__render_offday()
                    else:
                        debug.info("Game Day Wooooo")
                        self.__render_game_day()

            except AttributeError as e:
                debug.log(f"ERROR WHILE RENDERING: {e}")
                debug.log("Refreshing data in a minute")
                self.boards.fallback(self.data, self.matrix, self.sleepEvent)
                self.data.refresh_data()


    def __render_offday(self):
        while True:
            debug.log('PING !!! Render off day')
            if self.data._is_new_day():
                debug.info('This is a new day')
                return
            self.data.refresh_data()
            self.boards._off_day(self.data, self.matrix, self.sleepEvent)

    def __render_game_day(self):
        debug.info("Showing Game")
        # Initialize the scoreboard. get the current status at startup
        self.data.refresh_overview()
        self.scoreboard = Scoreboard(self.data.overview, self.data)
        self.away_score = self.scoreboard.away_team.goals
        self.home_score = self.scoreboard.home_team.goals
        self.sleepEvent.clear()

        while not self.sleepEvent.is_set():

            if self.data._is_new_day():
                debug.log('This is a new day')
                return

            # Display the pushbutton board
            if self.data.pb_trigger:
                debug.info('PushButton triggered in game day loop....will display ' + self.data.config.pushbutton_state_triggered1 + ' board')
                self.data.pb_trigger = False
                #Display the board from the config
                self.boards._pb_board(self.data, self.matrix, self.sleepEvent)

            if self.status.is_live(self.data.overview.status):
                """ Live Game state """
                debug.info("Game is Live")
                self.scoreboard = Scoreboard(self.data.overview, self.data)
                self.check_new_goals()
                self.__render_live(self.scoreboard)
                if self.scoreboard.intermission:
                    debug.info("Main event is in Intermission")
                    # Show Boards for Intermission
                    self.draw_end_period_indicator()
                    #sleep(self.refresh_rate)
                    self.sleepEvent.wait(self.refresh_rate)
                    self.boards._intermission(self.data, self.matrix,self.sleepEvent)
                else:
                    self.sleepEvent.wait(self.refresh_rate)

            elif self.status.is_game_over(self.data.overview.status):
                debug.info("Game Over")
                self.scoreboard = Scoreboard(self.data.overview, self.data)
                self.__render_postgame(self.scoreboard)
                # sleep(self.refresh_rate)
                self.sleepEvent.wait(self.refresh_rate)

            elif self.status.is_final(self.data.overview.status):
                """ Post Game state """
                debug.info("FINAL")
                self.scoreboard = Scoreboard(self.data.overview, self.data)
                self.__render_postgame(self.scoreboard)
                #sleep(self.refresh_rate)
                self.sleepEvent.wait(self.refresh_rate)
                if self.data._next_game():
                    debug.info("moving to the next preferred game")
                    return
                self.boards._post_game(self.data, self.matrix,self.sleepEvent)

            elif self.status.is_scheduled(self.data.overview.status):
                """ Pre-game state """
                debug.info("Game is Scheduled")
                self.scoreboard = Scoreboard(self.data.overview, self.data)
                self.__render_pregame(self.scoreboard)
                #sleep(self.refresh_rate)
                self.sleepEvent.wait(self.refresh_rate)
                self.boards._scheduled(self.data, self.matrix,self.sleepEvent)

            elif self.status.is_irregular(self.data.overview.status):
                """ Pre-game state """
                debug.info("Game is irregular")
                self.scoreboard = Scoreboard(self.data.overview, self.data)
                self.__render_irregular(self.scoreboard)
                #sleep(self.refresh_rate)
                self.sleepEvent.wait(self.refresh_rate)
                self.boards._scheduled(self.data, self.matrix,self.sleepEvent)

            sleep(5)
            self.data.refresh_data()
            self.data.refresh_overview()
            if self.data.network_issues:
                self.matrix.network_issue_indicator()



    def __render_pregame(self, scoreboard):
        debug.info("Showing Pre-Game")
        self.matrix.clear()
        ScoreboardRenderer(self.data, self.matrix, scoreboard).render()



    def __render_postgame(self, scoreboard):
        debug.info("Showing Post-Game")
        self.matrix.clear()
        ScoreboardRenderer(self.data, self.matrix, scoreboard).render()
        self.draw_end_of_game_indicator()


    def __render_live(self, scoreboard):
        debug.info("Showing Main Event")
        self.matrix.clear()
        show_SOG = False
        if self.alternate_data_counter % self.sog_display_frequency == 0:
            show_SOG = True
        ScoreboardRenderer(self.data, self.matrix, scoreboard, show_SOG).render()
        self.alternate_data_counter += 1

    def __render_irregular(self, scoreboard):
        debug.info("Showing Irregular")
        self.matrix.clear()
        ScoreboardRenderer(self.data, self.matrix, scoreboard).render()



    def check_new_goals(self):
        debug.log("Check new goal")
        pref_team_only = self.data.config.goal_anim_pref_team_only
        away_id = self.scoreboard.away_team.id
        away_name = self.scoreboard.away_team.name
        away_goals = self.scoreboard.away_team.goals
        away_score = self.away_score
        home_id = self.scoreboard.home_team.id
        home_name = self.scoreboard.home_team.name
        home_goals = self.scoreboard.home_team.goals
        home_score = self.home_score

        if away_score < away_goals:
            self.away_score = away_goals
            if away_id not in self.data.pref_teams and pref_team_only:
                return
            self._draw_goal(away_id, away_name)
        if home_score < home_goals:
            self.home_score = home_goals
            if home_id not in self.data.pref_teams and pref_team_only:
                return
            self._draw_goal(home_id, home_name)

    def _draw_goal(self, id, name):
        debug.info('Score by team: ' + name)

        # Get the list of gif's under the preferred and opposing directory
        preferred_gifs = glob.glob("assets/animations/preferred/*.gif")
        opposing_gifs = glob.glob("assets/animations/opposing/*.gif")

        # Set opposing team goal animation here
        filename = random.choice(opposing_gifs)
        debug.info("Opposing animation is: " + filename)
        if id in self.data.pref_teams:
            # Set your preferred team goal animation here
            filename = random.choice(preferred_gifs)
            debug.info("Preferred animation is: " + filename)


        im = Image.open(get_file(filename))

        # Set the frame index to 0
        frame_nub = 0

        self.matrix.clear()

        # play sound here

        # Go through the frames
        x = 0
        while x is not 5:
            try:
                im.seek(frame_nub)
            except EOFError:
                x += 1
                frame_nub = 0
                im.seek(frame_nub)

            self.matrix.draw_image((0, 0), im,"center")
            self.matrix.render()

            frame_nub += 1
            sleep(0.1)

    def draw_end_period_indicator(self):
        """TODO: change the width depending how much time is left to the intermission"""
        # color = self.matrix.graphics.Color(0, 255, 0)
        color = (0, 255, 0)
        # self.matrix.graphics.DrawLine(self.matrix.matrix, 24, self.matrix.height - 2, 40, self.matrix.height - 2, color)
        self.matrix.draw_line(
            start_coords=(24, self.matrix.height - 2),
            end_coords=(40, self.matrix.height - 2),
            colour=color
        )
        # self.matrix.graphics.DrawLine(self.matrix.matrix, 23, self.matrix.height - 1, 41, self.matrix.height - 1, color)
        self.matrix.draw_line(
            start_coords=(23, self.matrix.height - 1),
            end_coords=(41, self.matrix.height - 1),
            colour=color
        )

    def draw_end_of_game_indicator(self):
        """TODO: change the width depending how much time is left to the intermission"""
        # color = self.matrix.graphics.Color(255, 0, 0)
        color = (255, 0, 0)
        # self.matrix.graphics.DrawLine(self.matrix.matrix, 24, self.matrix.height - 2, 40, self.matrix.height - 2, color)
        self.matrix.draw_line(
            start_coords=(24, self.matrix.height - 2),
            end_coords=(40, self.matrix.height - 2),
            colour=color
        )
        # self.matrix.graphics.DrawLine(self.matrix.matrix, 23, self.matrix.height - 1, 41, self.matrix.height - 1, color)
        self.matrix.draw_line(
            start_coords=(23, self.matrix.height - 1),
            end_coords=(41, self.matrix.height - 1),
            colour=color
        )
