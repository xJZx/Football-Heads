import pygame
import os


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, goal_side):
        pygame.sprite.Sprite.__init__(self)

        self.game_path = os.getcwd()
        self.root_dir = os.path.dirname(self.game_path)

        self.goal_side = goal_side

        if self.goal_side == "left":
            self.texture_path = os.path.join(self.root_dir, 'Textures\goalOne.png')

        else:
            self.texture_path = os.path.join(self.root_dir, 'Textures\goalTwo.png')

        self.image = pygame.image.load(self.texture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_goal(self, screen):
        screen.blit(self.image, self.rect)

        # drew rect hitbox
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)