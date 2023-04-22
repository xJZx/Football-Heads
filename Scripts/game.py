import pygame
from pygame import image
import os
from player import Player


class Game:

    # Methods

    def __init__(self):
        self.game_path = os.getcwd()
        self.root_dir = os.path.dirname(self.game_path)
        background_image_path = os.path.join(self.root_dir, 'Textures\stadium.jpg')

        # Initialize Pygame
        pygame.init()

        # Set up the display
        WIDTH = 1920
        HEIGHT = 1080
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Load the background image
        self.__background = pygame.image.load(background_image_path)

        # Draw the background image
        self.__screen.blit(self.__background, (0, 0))

        self.__playerOne = Player("left")
        self.__playerOne.rect.x = 100  # go to x
        self.__playerOne.rect.y = 580  # go to y

        self.__playerTwo = Player("right")
        self.__playerTwo.rect.x = 1600  # go to x
        self.__playerTwo.rect.y = 580  # go to y

        self.__playerOne.draw(self.__screen)
        self.__playerTwo.draw(self.__screen)

        # Update the display
        pygame.display.flip()

    def checkLeftBounds(self, sprite):
        if sprite.rect.x > sprite.velocity:
            return True

        return False

    def checkRightBounds(self, sprite):
        if sprite.rect.x < self.__screen.get_width() - sprite.velocity - sprite.rect.width:
            return True

        return False

    def run(self):
        # Add game loop if needed
        while True:
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    # sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.checkLeftBounds(self.__playerTwo):
                self.__playerTwo.moveLeft()
            if keys[pygame.K_RIGHT] and self.checkRightBounds(self.__playerTwo):
                self.__playerTwo.moveRight()

            if keys[pygame.K_a] and self.checkLeftBounds(self.__playerOne):
                self.__playerOne.moveLeft()
            if keys[pygame.K_d] and self.checkRightBounds(self.__playerOne):
                self.__playerOne.moveRight()

            if not self.__playerTwo.isJumping:
                if keys[pygame.K_UP]:
                    self.__playerTwo.isJumping = True

            else:
                self.__playerTwo.jump()

            if not self.__playerOne.isJumping:
                if keys[pygame.K_w]:
                    self.__playerOne.isJumping = True

            else:
                self.__playerOne.jump()

            # Update game logic and draw game objects

            # Update the display
            self.refresh()
            pygame.display.update()

    def refresh(self):
        self.__screen.blit(self.__background, (0, 0))
        self.__playerOne.draw(self.__screen)
        self.__playerTwo.draw(self.__screen)
        pygame.display.flip()

    @staticmethod
    def clip(val, min_val, max_val):
        return min(max(val, min_val), max_val)
