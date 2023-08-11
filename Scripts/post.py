import pygame
import os


class Post(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.game_path = os.getcwd()
        self.root_dir = os.path.dirname(self.game_path)

        self.texture_path = os.path.join(self.root_dir, 'Textures\crossbar.png')

        self.image = pygame.image.load(self.texture_path).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.mass = 5

    def draw_post(self, screen):
        screen.blit(self.image, self.rect)

        # drew rect hitbox
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
