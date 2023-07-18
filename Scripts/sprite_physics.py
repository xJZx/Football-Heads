import math
import pygame


class Sprite_Physics(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        Sprite_Physics.gravity = (math.pi, 0.2)
        Sprite_Physics.drag = 0.999
        Sprite_Physics.elasticity = 0.75
