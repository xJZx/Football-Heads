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
        self.__playerOne.rect.x = 0  # go to x
        self.__playerOne.rect.y = 600  # go to y

        self.__playerTwo = Player("right")
        self.__playerTwo.rect.x = 1500  # go to x
        self.__playerTwo.rect.y = 600  # go to y


        self.__player_list = pygame.sprite.Group()
        self.__player_list.add(self.__playerOne)
        self.__player_list.add(self.__playerTwo)

        self.__player_list.draw(screen)

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                    # sys.exit()

            # Update game logic and draw game objects


            # Update the display
            pygame.display.update()

