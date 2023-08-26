import math
import random
import pygame
import os
from sprite_physics import Sprite_Physics


class Ball(Sprite_Physics):
    def __init__(self):

        Sprite_Physics.__init__(self)

        self.velocity = 10

        self.mass = 0.1

        self.game_path = os.getcwd()
        self.root_dir = os.path.dirname(self.game_path)

        self.angle = random.uniform(0, math.pi*2)

        # self.ball_state

        self.default_texture_path = os.path.join(self.root_dir, r'Textures\ball_faf.png')
        self.image = pygame.image.load(self.default_texture_path).convert_alpha()
        self.rect = self.image.get_rect()

    def move(self):
        move_vector = (self.angle, self.velocity)
        (self.angle, self.velocity) = self.add_vectors(move_vector, Sprite_Physics.gravity)
        self.velocity *= Sprite_Physics.drag

        self.rect.x += math.sin(self.angle) * self.velocity
        self.rect.y -= math.cos(self.angle) * self.velocity

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
            self.angle = - self.angle
            self.velocity *= Sprite_Physics.elasticity
        elif self.rect.x < self.velocity:
            self.rect.x = 2 * self.velocity - self.rect.x
            self.angle = - self.angle
            self.velocity *= Sprite_Physics.elasticity

        if self.rect.y > lower_bounds - self.rect.height:
            self.rect.y = 2 * (lower_bounds - self.rect.height) - self.rect.y
            self.angle = math.pi - self.angle
            self.velocity *= Sprite_Physics.elasticity
        elif self.rect.y < self.velocity:
            self.rect.y = 2 * self.velocity - self.rect.y
            self.angle = math.pi - self.angle
            self.velocity *= Sprite_Physics.elasticity

    def rotate_image(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle * -90)
        new_rect = rotated_image.get_rect()
        return rotated_image

    def draw_ball(self, screen):
        rotated_image = pygame.transform.rotate(self.image, (self.angle * -180) / math.pi)
        new_rect = rotated_image.get_rect()
        new_rect.centerx = new_rect.centerx - rotated_image.get_width() / 2
        new_rect.centery = new_rect.centery - rotated_image.get_height() / 2
        # (self.rect.x - new_rect.center[0], self.rect.y - new_rect.center[1])  V down
        # screen.blit(rotated_image, self.rect)
        screen.blit(rotated_image, (self.rect.x - new_rect.center[0], self.rect.y - new_rect.center[1]))

        # draw rect hitbox
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

        # draw vectors
        # pygame.draw.line(screen, (0, 255, 0), self.rect.center, )

        # print(self.angle * 180 / math.pi)
