import pygame

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # wstawic obrazek dla poprzeki
        self.rect.x = x
        self.rect.y = y

        self.rect.width = 330
        self.rect.height = 10
