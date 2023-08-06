import math
import pygame
import os

from sprite_physics import Sprite_Physics
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
        self.collisionTolerance = 10

        self.goalOne = Goal(0, 360)
        self.goalTwo = Goal(self.screen.get_width() - self.goalOne.rect.width, 360)

        self.ball.draw_ball(self.screen)
        self.playerOne.draw_player(self.screen)
        self.playerTwo.draw_player(self.screen)
        self.goalOne.draw_goal(self.screen)
        self.goalTwo.draw_goal(self.screen)

        self.all_sprites = [self.playerOne, self.playerTwo, self.ball]
        # all_sprites = pygame.sprite.Group()

        # Update the display
        pygame.display.flip()

    @staticmethod
    def add_vectors(vector1, vector2):
        x = math.sin(vector1[0]) * vector1[1] + math.sin(vector2[0]) * vector1[1]
        y = math.cos(vector1[0]) * vector1[1] + math.cos(vector2[0]) * vector2[1]

        length = math.hypot(x, y)
        angle = 0.5 * math.pi - math.atan2(y, x)
        return_vector = (angle, length)

        return return_vector

    def checkCollisionPlayer(self, ball, player):
        dx = ball.rect.centerx - player.rect.centerx
        dy = ball.rect.centery - player.rect.centery
        # print('dx=', dx)
        # print('dy=', dy)

        distance = math.hypot(dx, dy)
        # print('distance=', distance)
        if distance < player.rect.width / 2 + ball.rect.width / 2:  # ball.rect.width +
            tangent = math.atan2(dy, dx)

            angle = 0.5 * math.pi + tangent

            total_mass = ball.mass + player.mass

            # ball gets the angle calculated from tangent and the current velocity of the player as zderzenie sprezyste
            (ball.angle, ball.velocity) = (angle, 2 * abs(player.velocity + player.lift_force) * player.mass / total_mass + ball.velocity)
            # lower the speed of ball by elasticity,
            # otherwise would start getting constantly faster with every other bounce
            ball.velocity *= Sprite_Physics.elasticity

            ball.rect.x += math.sin(angle)
            ball.rect.y -= math.cos(angle)

    def checkCollisionGoalOne(self):
        if self.ball.rect.colliderect(self.goalOne):

            if abs(self.goalOne.rect.top - self.ball.rect.bottom) < self.ball.velocity + self.collisionTolerance and (math.pi / 2) < self.ball.angle < (math.pi * 1.5): # hit from top
                self.ball.angle = math.pi - self.ball.angle
                self.ball.velocity *= Sprite_Physics.elasticity

            elif abs(self.goalOne.rect.bottom - self.ball.rect.top) < self.ball.velocity + self.collisionTolerance and 0 < abs(self.ball.angle) < (math.pi / 2): # hit from bottom
                self.ball.angle = math.pi - self.ball.angle
                self.ball.velocity *= Sprite_Physics.elasticity

            elif abs(self.goalOne.rect.right - self.ball.rect.left) < self.ball.velocity + self.collisionTolerance and (self.ball.angle < 0 or math.pi < self.ball.angle < (math.pi * 1.5)): # hit from right
                if self.ball.angle < 0:
                    self.ball.angle = -self.ball.angle

                else:
                    self.ball.angle = math.pi - self.ball.angle

                self.ball.velocity *= Sprite_Physics.elasticity

    def checkCollisionGoalTwo(self):
        if self.ball.rect.colliderect(self.goalTwo):

            if abs(self.goalTwo.rect.top - self.ball.rect.bottom) < self.ball.velocity + self.collisionTolerance and (math.pi / 2) < self.ball.angle < (math.pi * 1.5): # hit from top
                self.ball.angle = math.pi - self.ball.angle
                self.ball.velocity *= Sprite_Physics.elasticity

            elif abs(self.goalTwo.rect.bottom - self.ball.rect.top) < self.ball.velocity + self.collisionTolerance and 0 < abs(self.ball.angle) < (math.pi / 2): # hit from bottom
                self.ball.angle = math.pi - self.ball.angle
                self.ball.velocity *= Sprite_Physics.elasticity

            elif abs(self.goalTwo.rect.left - self.ball.rect.right) < self.ball.velocity + self.collisionTolerance and 0 < self.ball.angle < math.pi: # hit from left
                if 0 < self.ball.angle < math.pi:
                    self.ball.angle = -self.ball.angle

                else:
                    self.ball.angle = math.pi + self.ball.angle

                self.ball.velocity *= Sprite_Physics.elasticity



    def checkLeftBounds(self, sprite):
        if sprite.rect.x > sprite.velocity:
            return True

        return False

    def checkRightBounds(self, sprite):
        if sprite.rect.x < self.screen.get_width() - sprite.velocity - sprite.rect.width:
            return True

        return False

    def run(self):
        # Add game loop if needed
        left_down = False
        right_down = False
        a_down = False
        d_down = False
        while True:
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left_down = True

                    elif event.key == pygame.K_RIGHT:
                        right_down = True

                    elif event.key == pygame.K_a:
                        a_down = True

                    elif event.key == pygame.K_d:
                        d_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left_down = False

                    elif event.key == pygame.K_RIGHT:
                        right_down = False

                    elif event.key == pygame.K_a:
                        a_down = False

                    elif event.key == pygame.K_d:
                        d_down = False

            if left_down:
                if self.checkLeftBounds(self.playerTwo) and not self.playerTwo.rect.collidepoint(
                        self.playerOne.rect.midright):
                    if self.playerTwo.velocity >= -self.playerTwo.MAX_VELOCITY:
                        self.playerTwo.velocity -= self.playerTwo.acceleration
                    self.playerTwo.move()
            else:
                if self.checkLeftBounds(self.playerTwo) and not self.playerTwo.rect.collidepoint(
                        self.playerOne.rect.midright):
                    if self.playerTwo.velocity < 0:
                        self.playerTwo.velocity += self.playerTwo.acceleration
                        self.playerTwo.move()

            if right_down:
                if self.checkRightBounds(self.playerTwo) and not self.playerTwo.rect.collidepoint(
                        self.playerOne.rect.midleft):
                    if self.playerTwo.velocity <= self.playerTwo.MAX_VELOCITY:
                        self.playerTwo.velocity += self.playerTwo.acceleration
                    self.playerTwo.move()
            else:
                if self.checkRightBounds(self.playerTwo) and not self.playerTwo.rect.collidepoint(
                        self.playerOne.rect.midleft):
                    if self.playerTwo.velocity > 0:
                        self.playerTwo.velocity -= self.playerTwo.acceleration
                        self.playerTwo.move()

            if a_down:
                if self.checkLeftBounds(self.playerOne) and not self.playerOne.rect.collidepoint(
                        self.playerTwo.rect.midright):
                    if self.playerOne.velocity >= -self.playerOne.MAX_VELOCITY:
                        self.playerOne.velocity -= self.playerOne.acceleration
                    self.playerOne.move()
            else:
                if self.checkLeftBounds(self.playerOne) and not self.playerOne.rect.collidepoint(
                        self.playerTwo.rect.midright):
                    if self.playerOne.velocity < 0:
                        self.playerOne.velocity += self.playerOne.acceleration
                        self.playerOne.move()

            if d_down:
                if self.checkRightBounds(self.playerOne) and not self.playerOne.rect.collidepoint(
                        self.playerTwo.rect.midleft):
                    if self.playerOne.velocity <= self.playerOne.MAX_VELOCITY:
                        self.playerOne.velocity += self.playerOne.acceleration
                    self.playerOne.move()
            else:
                if self.checkRightBounds(self.playerOne) and not self.playerOne.rect.collidepoint(
                        self.playerTwo.rect.midleft):
                    if self.playerOne.velocity > 0:
                        self.playerOne.velocity -= self.playerOne.acceleration
                        self.playerOne.move()

            #print(self.playerOne.velocity)
            #print(self.playerTwo.velocity)

            keys = pygame.key.get_pressed()

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
            self.checkCollisionPlayer(self.ball, self.playerOne)
            self.checkCollisionPlayer(self.ball, self.playerTwo)
            self.checkCollisionGoalTwo()
            self.checkCollisionGoalOne()

            self.ball.bounce(self.screen, self.lower_bounds)
            self.ball.move()
            # print(self.ball.velocity)
            # print(self.playerTwo.velocity)
            # print(self.playerOne.velocity)

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
        self.goalOne.draw_goal(self.screen)
        self.goalTwo.draw_goal(self.screen)
        pygame.display.flip()
