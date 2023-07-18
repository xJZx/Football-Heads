import math
import random
import pygame
import os

from sprite_physics import Sprite_Physics


class Player(Sprite_Physics):

    def __init__(self, player_side):

        Sprite_Physics.__init__(self)

        self.MAX_VELOCITY = 10
        self.velocity = 0

        self.acceleration = 0.5

        self.mass = 5

        self.angle = math.pi / 2

        self.isJumping = False
        self.jumpCount = 8
        self.currentJumpCount = self.jumpCount

        self.MAX_FOOT_ANGLE = 90
        self.foot_angle = 0

        self.game_path = os.getcwd()
        self.root_dir = os.path.dirname(self.game_path)

        self.player_side = player_side

        if self.player_side == "left":
            self.default_texture_path = os.path.join(self.root_dir, 'Textures\player1_default_merged.png')
            self.lost_texture_path = os.path.join(self.root_dir, 'Textures\player1_lost.jpg')
            self.won_texture_path = os.path.join(self.root_dir, 'Textures\player1_won.jpg')
        else:
            self.default_texture_path = os.path.join(self.root_dir, 'Textures\player2_default_merged.png')
            self.lost_texture_path = os.path.join(self.root_dir, 'Textures\player2_lost.jpg')
            self.won_texture_path = os.path.join(self.root_dir, 'Textures\player2_won.jpg')

        self.image = pygame.image.load(self.default_texture_path).convert_alpha()
        self.rect = self.image.get_rect()

    @staticmethod
    def add_vectors(vector1, vector2):
        x = math.sin(vector1[0]) * vector1[1] + math.sin(vector2[0]) * vector1[1]
        y = math.cos(vector1[0]) * vector1[1] + math.cos(vector2[0]) * vector2[1]

        length = math.hypot(x, y)
        angle = 0.5 * math.pi - math.atan2(y, x)
        return_vector = (angle, length)

        return return_vector

    def move(self):
        self.rect.x += self.velocity

    def bounce_back(self, bouncing_side):
        if bouncing_side == 'left':
            self.rect.x -= 15

        else:
            self.rect.x += 15

    def jump(self):
        if self.currentJumpCount >= -self.jumpCount:
            neg = 1
            if self.currentJumpCount < 0:
                neg = -1

            self.rect.y -= (abs(self.currentJumpCount) ** 2) * neg
            self.currentJumpCount -= 1
        else:
            self.currentJumpCount = self.jumpCount
            self.isJumping = False

    def kick(self, press_time):
        pass

    def change_state(self, target_state):
        pass

    def draw_player(self, screen):
        screen.blit(self.image, self.rect)
