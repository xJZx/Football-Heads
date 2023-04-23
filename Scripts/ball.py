import math
import random
import pygame
from pygame import image
import os


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.velocity_ball = 10
        self.gravity = (math.pi, 0.2)
        self.drag = 0.999
        self.elasticity = 0.75

        self.game_path = os.getcwd()
        self.root_dir = os.path.dirname(self.game_path)

        self.angle_ball = random.uniform(0, math.pi*2)

        # self.ball_state

        self.default_texture_path = os.path.join(self.root_dir, r'Textures\ball_faf.png')
        self.image = pygame.image.load(self.default_texture_path).convert_alpha()
        self.rect = self.image.get_rect()

    def move(self):
        move_vector = (self.angle_ball, self.velocity_ball)
        (self.angle_ball, self.velocity_ball) = self.add_vectors(move_vector, self.gravity)
        self.velocity_ball *= self.drag

        self.rect.x += math.sin(self.angle_ball) * self.velocity_ball
        self.rect.y -= math.cos(self.angle_ball) * self.velocity_ball

    @staticmethod
    def add_vectors(vector1, vector2):
        x = math.sin(vector1[0]) * vector1[1] + math.sin(vector2[0]) * vector1[1]
        y = math.cos(vector1[0]) * vector1[1] + math.cos(vector2[0]) * vector2[1]

        length = math.hypot(x, y)
        angle = 0.5 * math.pi - math.atan2(y, x)
        return_vector = (angle, length)

        return return_vector

    def bounce(self, screen, lower_bounds):
        if self.rect.x > screen.get_width() - self.rect.width:
            self.rect.x = 2 * (screen.get_width() - self.rect.width) - self.rect.x
            self.angle_ball = - self.angle_ball
            self.velocity_ball *= self.elasticity
        elif self.rect.x < self.velocity_ball:
            self.rect.x = 2 * self.velocity_ball - self.rect.x
            self.angle_ball = - self.angle_ball
            self.velocity_ball *= self.elasticity

        if self.rect.y > lower_bounds - self.rect.height:
            self.rect.y = 2 * (lower_bounds - self.rect.height) - self.rect.y
            self.angle_ball = math.pi - self.angle_ball
            self.velocity_ball *= self.elasticity
        elif self.rect.y < self.velocity_ball:
            self.rect.y = 2 * self.velocity_ball - self.rect.y
            self.angle_ball = math.pi - self.angle_ball
            self.velocity_ball *= self.elasticity

    def draw_ball(self, screen):
        screen.blit(self.image, self.rect)
