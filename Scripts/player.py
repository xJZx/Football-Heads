import pygame
from pygame import image
import os


class Player(pygame.sprite.Sprite):

    def __init__(self, player_side):

        pygame.sprite.Sprite.__init__(self)

        self.MAX_VELOCITY = 12
        self.velocity_player = 10

        self.isJumping = False
        self.jumpCount = 8
        self.currentJumpCount = self.jumpCount

        self.MAX_JUMP = 300
        self.GROUND_LEVEL = 400

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

    def move_left(self):
        self.rect.x -= self.velocity_player

    def move_right(self):
        self.rect.x += self.velocity_player

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
