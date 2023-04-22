import pygame
from pygame import image
import os

class Player(pygame.sprite.Sprite):

    def __init__(self, player_side):

        pygame.sprite.Sprite.__init__(self)

        self.__MAX_VELOCITY = 12
        self.velocity = 10

        self.isJumping = False
        self.jumpCount = 8
        self.__currentJumpCount = self.jumpCount

        self.__MAX_JUMP = 300
        self.__GROUND_LEVEL = 400

        self.__MAX_FOOT_ANGLE = 90
        self.__foot_angle = 0

        self.__game_path = os.getcwd()
        self.__root_dir = os.path.dirname(self.__game_path)

        self.__player_side = player_side

        if self.__player_side == "left":
            self.__default_texture_path = os.path.join(self.__root_dir, 'Textures\player1_default_merged.png')
            self.__lost_texture_path = os.path.join(self.__root_dir, 'Textures\player1_lost.jpg')
            self.__won_texture_path = os.path.join(self.__root_dir, 'Textures\player1_won.jpg')
        else:
            self.__default_texture_path = os.path.join(self.__root_dir, 'Textures\player2_default_merged.png')
            self.__lost_texture_path = os.path.join(self.__root_dir, 'Textures\player2_lost.jpg')
            self.__won_texture_path = os.path.join(self.__root_dir, 'Textures\player2_won.jpg')

        self.image = pygame.image.load(self.__default_texture_path).convert_alpha()
        self.rect = self.image.get_rect()

    def moveLeft(self):
        self.rect.x -= self.velocity

    def moveRight(self):
        self.rect.x += self.velocity

    def jump(self):
        if self.__currentJumpCount >= -self.jumpCount:
            neg = 1
            if self.__currentJumpCount < 0:
                neg = -1

            self.rect.y -= (abs(self.__currentJumpCount) ** 2) * neg
            self.__currentJumpCount -= 1
        else:
            self.__currentJumpCount = self.jumpCount
            self.isJumping = False


    def kick(self, press_time):
        pass

    def change_state(self, target_state):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
