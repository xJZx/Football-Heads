import pygame
from pygame import image
import os


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.velocity_ball = 10

        self.__game_path = os.getcwd()
        self.__root_dir = os.path.dirname(self.__game_path)

        # self.__ball_state

        self.__default_texture_path = os.path.join(self.__root_dir, 'Textures\ball_faf.png')
