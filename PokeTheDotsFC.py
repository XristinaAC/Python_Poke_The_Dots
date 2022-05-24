from uagame import Window
from pygame.event import get as get_events
from pygame import QUIT, Color, MOUSEBUTTONUP, KEYDOWN, K_r, display
from pygame.time import Clock, get_ticks
from pygame.draw import circle as draw_circle
from random import randint
import math

class Dot:
    def __init__(self, radius, velocity, color):
        self.center    = ''
        self.radius   = radius
        self.velocity = velocity
        self.color    = color

    def get_dot_color(self):
        return self.color

    def randomize_dot(self, window = None):
        center_x = randint(self.radius, window.get_width()- self.radius)
        center_y = randint(self.radius, window.get_height() - self.radius) 

        self.center = [center_x, center_y]

    def draw_dot(self, window = None):
        surface = window.get_surface()

        draw_circle(surface, self.color, self.center, self.radius)

    def move_dot(self, window = None):
        width = window.get_width
        size = [window.get_width(), window.get_height()]

        for index in range(0,2):
            self.center[index] = self.center[index] + self.velocity[index]

            if self.center[index] + self.radius >= size[index] or self.center[index] <= self.radius:
                self.velocity[index] = - self.velocity[index]



class Game:
    def __init__(self):
        self._window         = Window('Poke the Dots', 1080, 700)
        self._frame_rate     = 90
        self._close_selected = False
        self._clock          = Clock()
        self._dots           = []
        self._score          = 0
        self.old_score       = 0
        self.old_score_v     = 0
        self._game_lost      = False
        self._timer          = 0

        self._adjust_window()
        for index in range(0,2):
            self.create_dot()

    def create_dot(self):
            r_color  = (randint(0,255),randint(0,255),randint(0,255))
            r_radius = randint(25,60)
            r_velocity_x = randint(1,2)
            r_velocity_y = randint(2,3)
            dot = Dot(r_radius, [r_velocity_x ,r_velocity_y], r_color)
            dot.randomize_dot(self._window)
            self._dots.append(dot)

    def _adjust_window(self):
        self._window.set_font_size(65)
        self._window.set_font_color('orange')
        self._window.set_bg_color('black')

    def draw_score(self):
        self._score = str(int(get_ticks() / 1000) - self._timer)
        self._window.draw_string('Score: '+self._score, 0, 0)

    def draw_replay_string(self):
        replay_string = 'To replay press R'
        r_s_x = (self._window.get_width() - self._window.get_string_width(replay_string))//2
        r_s_y = (self._window.get_height() - self._window.get_font_height())//2

        self._window.draw_string(replay_string, r_s_x,r_s_y)
        self._window.set_font_color('red')
        self._window.set_bg_color('orange')

    def draw_game_over_string(self):
        g_o_s_y = self._window.get_height() - self._window.get_font_height()
        self._window.draw_string('GAME OVER', 0, g_o_s_y)

    def draw_game_over(self):
        self.draw_game_over_string()
        self.draw_replay_string()

    def increase_dots_velocity(self):
       if int(self._score) > self.old_score_v + 5:
           for index in range(0,len(self._dots)):
               self._dots[index].velocity[0] =  self._dots[index].velocity[0] + randint(3,4)
               self._dots[index].velocity[1] =  self._dots[index].velocity[1] + randint(1,2)
           
           self.old_score_v = int(self._score)

    def create_in_game_dot(self):
        if int(self._score) >=  self.old_score + 10:
            self.create_dot()
            self.old_score = int(self._score)

    def draw_game(self):
        if(self._game_lost == False):
            self._window.clear()
            self.draw_score()
            self.create_in_game_dot()
            self.increase_dots_velocity()

            for index in range(0,len(self._dots)):
                self._dots[index].draw_dot(self._window)
        else:
            self.draw_game_over()

        self._window.update()

    def reload_game(self):
         self._dots = []
         for index in range(0,2):
             self.create_dot()

         self.old_score = 0
         self._v_increment = 0
         self._adjust_window()
         self._game_lost = False

    def handle_close_window_event(self, event):
        if event.type == QUIT:
            self._close_selected = True

    def handle_rnadomize_dots_event(self, event):
        if event.type == MOUSEBUTTONUP:
            for index in range(0,len(self._dots)):
                self._dots[index].randomize_dot(self._window)

    def handle_reload_game_event(self, event):
        if self._game_lost == True and event.type == KEYDOWN:
            if event.key == K_r:
                self.reload_game()

    def handle_events(self):
        event_list = get_events()
        for event in event_list:
            self.handle_close_window_event(event)
            self.handle_rnadomize_dots_event(event)
            self.handle_reload_game_event(event)
       
    def update_game(self):
        #Calculate dot distance using the distance formula for Euclidean distance.
        distance = math.sqrt((self._dots[0].center[0]-self._dots[1].center[0])**2 + (self._dots[0].center[1]-self._dots[1].center[1])**2)

        if(distance <= self._dots[0].radius + self._dots[1].radius):
            self._game_lost = True
            self._timer = int(get_ticks() / 1000)
        else:
            for index in range(0,len(self._dots)):
                self._dots[index].move_dot(self._window)

            self._clock.tick(self._frame_rate)

    def play(self):
        while not self._close_selected:
            self.handle_events()
            self.draw_game()
            self.update_game()

        self._window.close()

def main():
    game = Game()
    game.play()

main()