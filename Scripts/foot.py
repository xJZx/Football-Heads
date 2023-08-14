import math
import pygame
import os

from sprite_physics import Sprite_Physics


class Foot(Sprite_Physics):
    def __init__(self, foot_side):

        Sprite_Physics.__init__(self)



        self.game_path = os.getcwd()
        self.root_dir = os.path.dirname(self.game_path)

        self.foot_side = foot_side

        if self.foot_side == "left":
            self.default_texture_path = os.path.join(self.root_dir, 'Textures\\shoe_left.png')

        else:
            self.default_texture_path = os.path.join(self.root_dir, 'Textures\\shoe_right.png')

        self.image = pygame.image.load(self.default_texture_path).convert_alpha()
        self.rect = self.image.get_rect()

        self.MAX_FOOT_ANGLE = 90
        self.foot_angle = 0

    def kick(self, press_time):

        pass

    def draw_foot(self, screen):
        screen.blit(self.image, self.rect)
        # draw rect hitbox
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
