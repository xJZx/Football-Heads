import math
import pygame
import os

from pygame import Vector2

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
        self.original_image = self.image
        self.rect = self.image.get_rect()

        self.MAX_FOOT_ANGLE = 90
        self.FOOT_ANGLE_VELOCITY = 7
        self.foot_angle = 0
        self.pos = Vector2()
        self.offset = Vector2(50, 50)

        self.mass = 1

    def rotate_foot(self):
        # rotate image
        self.image = pygame.transform.rotozoom(self.original_image, -self.foot_angle, 1)
        # rotate offset vector
        # offset_rotated = self.offset.rotate(self.foot_angle)
        # create new rect
        self.rect = self.image.get_rect()
    #     center=self.pos+offset_rotated ^^^

    def kick_right_foot(self):
        if self.foot_angle < self.MAX_FOOT_ANGLE:
            self.foot_angle += self.FOOT_ANGLE_VELOCITY
            self.rotate_foot()

    def kick_left_foot(self):
        if self.foot_angle > -self.MAX_FOOT_ANGLE:
            self.foot_angle -= self.FOOT_ANGLE_VELOCITY
            self.rotate_foot()

    def draw_foot(self, screen):
        screen.blit(self.image, self.rect)
        # draw rect hitbox
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
