import pygame
from pygame import image
import os

class Player(pygame.sprite.Sprite):

    def __init__(self, player_side):

        pygame.sprite.Sprite.__init__(self)

        self.__MAX_VELOCITY = 1
        self.__velocity = 0

        self.__x_pos = 0
        self.__y_pos = 0

        self.__MAX_JUMP = 1

        self.__MAX_FOOT_ANGLE = 90
        self.__foot_angle = 0

        self.__game_path = os.getcwd()
        self.__root_dir = os.path.dirname(self.__game_path)

        self.__player_side = player_side

        if self.__player_side == "left":
            self.__default_texture_path = os.path.join(self.__root_dir, 'Textures\player1_default.png')
            self.__lost_texture_path = os.path.join(self.__root_dir, 'Textures\player1_lost.jpg')
            self.__won_texture_path = os.path.join(self.__root_dir, 'Textures\player1_won.jpg')
        else:
            self.__default_texture_path = os.path.join(self.__root_dir, 'Textures\player2_default.png')
            self.__lost_texture_path = os.path.join(self.__root_dir, 'Textures\player2_lost.jpg')
            self.__won_texture_path = os.path.join(self.__root_dir, 'Textures\player2_won.jpg')

        self.image = pygame.image.load(self.__default_texture_path).convert()
        self.rect = self.image.get_rect()

    def move(self, key):
        pass

    def jump(self, press_time):
        pass

    def kick(self, press_time):
        pass

    def change_state(self, target_state):
        pass
