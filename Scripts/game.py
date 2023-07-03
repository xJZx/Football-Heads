import pygame
from pygame import image
import os
from player import Player
from ball import Ball
from goal import Goal

class Game:

    # Methods

    def __init__(self):
        self.game_path = os.getcwd()
        self.root_dir = os.path.dirname(self.game_path)
        background_image_path = os.path.join(self.root_dir, r'Textures\stadium.jpg')

        # Initialize Pygame
        pygame.init()

        # Set up the display
        WIDTH = 1920
        HEIGHT = 1080
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Load the background image
        self.background = pygame.image.load(background_image_path)

        # Draw the background image
        self.screen.blit(self.background, (0, 0))

        self.lower_bounds = 760

        self.playerOne = Player("left")
        self.playerOne.rect.x = 100  # go to x
        self.playerOne.rect.y = self.lower_bounds - self.playerOne.rect.height  # go to y

        self.playerTwo = Player("right")
        self.playerTwo.rect.x = 1600  # go to x
        self.playerTwo.rect.y = self.lower_bounds - self.playerTwo.rect.height  # go to y

        self.ball = Ball()
        self.ball.rect.x = 960
        self.ball.rect.y = 400

        # self.goalOne = Goal(0, 360)
        # self.goalTwo = Goal(self.screen.get_width() - self.goalOne.rect.width, 360)

        self.ball.draw_ball(self.screen)
        self.playerOne.draw_player(self.screen)
        self.playerTwo.draw_player(self.screen)

        # all_sprites = pygame.sprite.Group([self.playerOne, self.playerTwo])

        # Update the display
        pygame.display.flip()

    def checkLeftBounds(self, sprite):
        if sprite.rect.x > sprite.velocity_player:
            return True

        return False

    def checkRightBounds(self, sprite):
        if sprite.rect.x < self.screen.get_width() - sprite.velocity_player - sprite.rect.width:
            return True

        return False

    def checkCollision(self, sprite_one, sprite_two):
        pass

    def run(self):
        # Add game loop if needed
        while True:
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    # sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if self.checkLeftBounds(self.playerTwo) and not self.playerTwo.rect.collidepoint(self.playerOne.rect.midright):
                    self.playerTwo.move_left()
                else:
                    self.playerTwo.bounce_back("right")

            if keys[pygame.K_RIGHT]:
                if self.checkRightBounds(self.playerTwo) and not self.playerTwo.rect.collidepoint(self.playerOne.rect.midleft):
                    self.playerTwo.move_right()
                else:
                    self.playerTwo.bounce_back("left")

            if keys[pygame.K_a]:
                if self.checkLeftBounds(self.playerOne) and not self.playerOne.rect.collidepoint(self.playerTwo.rect.midright):
                    self.playerOne.move_left()
                else:
                    self.playerOne.bounce_back("right")

            if keys[pygame.K_d]:
                if self.checkRightBounds(self.playerOne) and not self.playerOne.rect.collidepoint(self.playerTwo.rect.midleft):
                    self.playerOne.move_right()
                else:
                    self.playerOne.bounce_back("left")

            if not self.playerTwo.isJumping:
                if keys[pygame.K_UP]:
                    self.playerTwo.isJumping = True

            else:
                self.playerTwo.jump()

            if not self.playerOne.isJumping:
                if keys[pygame.K_w]:
                    self.playerOne.isJumping = True

            else:
                self.playerOne.jump()

            # for i, sprite1 in enumerate(self.all_sprites):
            #     for sprite2 in self.all_sprites[i + 1:]:
            #         Sprite_Physics.checkCollision(sprite1, sprite2)
            self.checkCollision(self.ball, self.playerOne)
            self.checkCollision(self.ball, self.playerTwo)

            self.ball.bounce(self.screen, self.lower_bounds)
            self.ball.move()

            # self.ball.bouncePlayer(self.playerOne, self.playerTwo)

            # Update game logic and draw game objects

            # Update the display
            self.refresh()
            pygame.display.update()

    def refresh(self):
        self.screen.blit(self.background, (0, 0))
        self.playerOne.draw_player(self.screen)
        self.playerTwo.draw_player(self.screen)
        self.ball.draw_ball(self.screen)
        pygame.display.flip()

    @staticmethod
    def clip(val, min_val, max_val):
        return min(max(val, min_val), max_val)
