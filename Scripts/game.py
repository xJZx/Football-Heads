import json
import math
import pygame
import os
import time
import socket

from Scripts.foot import Foot
from Scripts.goal import Goal
from sprite_physics import Sprite_Physics
from player import Player
from ball import Ball
from post import Post


class Game:

    # Methods

    def __init__(self):
        self.game_path = os.getcwd()
        self.root_dir = os.path.dirname(self.game_path)
        background_image_path = os.path.join(self.root_dir, r'Textures\stadium_snow.jpg')

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

        self.left_foot_offset_X = 60
        self.left_foot_offset_Y = 130
        self.right_foot_offset_X = 60
        self.right_foot_offset_Y = 130

        self.playerOne = Player("left")
        self.player_one_startPos = (100, self.lower_bounds - self.playerOne.rect.height)
        self.playerOne.rect.x = self.player_one_startPos[0]
        self.playerOne.rect.y = self.player_one_startPos[1]

        self.footOne = Foot("left")
        self.footOne.rect.x = self.playerOne.rect.x + self.left_foot_offset_X
        self.footOne.rect.y = self.playerOne.rect.y + self.left_foot_offset_Y

        self.playerTwo = Player("right")
        self.player_two_startPos = (1600, self.lower_bounds - self.playerTwo.rect.height)
        self.playerTwo.rect.x = self.player_two_startPos[0]
        self.playerTwo.rect.y = self.player_two_startPos[1]

        self.footTwo = Foot("right")
        self.footTwo.rect.x = self.playerTwo.rect.x - self.left_foot_offset_X
        self.footTwo.rect.y = self.playerTwo.rect.y + self.left_foot_offset_Y

        self.ball = Ball()
        self.ball_start_pos = (960, 400)
        self.ball.rect.x = self.ball_start_pos[0]
        self.ball.rect.y = self.ball_start_pos[1]
        self.collisionTolerance = 10

        self.postOne = Post(0, 340)
        self.postTwo = Post(self.screen.get_width() - self.postOne.rect.width, 340)

        self.goalOne = Goal(0, 360, 'left')
        self.goalTwo = Goal(self.screen.get_width() - self.goalOne.rect.width, 360, 'right')

        self.ball.draw_ball(self.screen)
        self.playerOne.draw_player(self.screen)
        self.footOne.draw_foot(self.screen)
        self.playerTwo.draw_player(self.screen)
        self.footTwo.draw_foot(self.screen)
        self.postOne.draw_post(self.screen)
        self.postTwo.draw_post(self.screen)
        self.goalOne.draw_goal(self.screen)
        self.goalTwo.draw_goal(self.screen)

        self.scored = False
        self.control = True
        self.goal_time = None

        # controlls for client side (player two)
        self.left_down = False
        self.right_down = False
        self.kick_right = False
        self.player_two_jump_pressed = False

        self.score = [0, 0]
        self.my_font = pygame.font.SysFont("monospace", 82)

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
        # dodalem predkosc pilki do badanego dystansu
        if distance < (player.rect.width / 2 + ball.rect.width / 2) + ball.velocity:  # ball.rect.width +
            tangent = math.atan2(dy, dx)

            angle = 0.5 * math.pi + tangent

            total_mass = ball.mass + player.mass

            # ball gets the angle calculated from tangent and the current velocity of the player as zderzenie sprezyste
            (ball.angle, ball.velocity) = (angle, 2 * abs(player.velocity + player.jump_force) * player.mass / total_mass + ball.velocity)
            # lower the speed of ball by elasticity,
            # otherwise would start getting constantly faster with every other bounce
            ball.velocity *= Sprite_Physics.elasticity

            ball.rect.x += math.sin(angle)
            ball.rect.y -= math.cos(angle)

    def checkCollisionFoot(self, ball, foot, player):
        dx = ball.rect.centerx - foot.rect.centerx
        dy = ball.rect.centery - foot.rect.centery

        distance = math.hypot(dx, dy)

        if distance < (foot.rect.width / 2 + ball.rect.width / 2) + ball.velocity:
            if 0 < foot.foot_angle < 80:
                tangent = math.atan2(dy, dx)

                angle = 0.5 * math.pi + tangent

                total_mass = ball.mass + foot.mass

                (ball.angle, ball.velocity) = (angle, 2 * abs(player.velocity + player.jump_force) * foot.mass / total_mass + ball.velocity + foot.FOOT_ANGLE_VELOCITY)

                ball.velocity *= Sprite_Physics.elasticity

                ball.rect.x += math.sin(angle)
                ball.rect.y -= math.cos(angle)

            else:
                tangent = math.atan2(dy, dx)

                angle = 0.5 * math.pi + tangent

                total_mass = ball.mass + foot.mass

                (ball.angle, ball.velocity) = (angle, 2 * abs(player.velocity + player.jump_force) * foot.mass / total_mass + ball.velocity)

                ball.velocity *= Sprite_Physics.elasticity

                ball.rect.x += math.sin(angle)
                ball.rect.y -= math.cos(angle)

    def checkCollisionPostOne(self):
        if self.ball.rect.colliderect(self.postOne):

            if abs(self.postOne.rect.top - self.ball.rect.bottom) < self.ball.velocity + self.collisionTolerance and (math.pi / 2) < self.ball.angle < (math.pi * 1.5): # hit from top
                self.ball.angle = math.pi - self.ball.angle
                self.ball.velocity *= Sprite_Physics.elasticity
                if 0 <= self.ball.velocity < 0.5:
                    self.ball.velocity += 1

            elif abs(self.postOne.rect.bottom - self.ball.rect.top) < self.ball.velocity + self.collisionTolerance and 0 < abs(self.ball.angle) < (math.pi / 2): # hit from bottom
                self.ball.angle = math.pi - self.ball.angle
                self.ball.velocity *= Sprite_Physics.elasticity

            elif abs(self.postOne.rect.right - self.ball.rect.left) < self.ball.velocity + self.collisionTolerance and (self.ball.angle <= 0 or math.pi <= self.ball.angle <= (math.pi * 1.5)): # hit from right
                if self.ball.angle < 0:
                    self.ball.angle = math.pi - self.ball.angle

                else:
                    self.ball.angle = -self.ball.angle


            # self.ball.velocity *= Sprite_Physics.elasticity

    def checkCollisionPostTwo(self):
        if self.ball.rect.colliderect(self.postTwo):

            if abs(self.postTwo.rect.top - self.ball.rect.bottom) < self.ball.velocity + self.collisionTolerance and (math.pi / 2) < self.ball.angle < (math.pi * 1.5): # hit from top
                self.ball.angle = math.pi - self.ball.angle
                self.ball.velocity *= Sprite_Physics.elasticity
                if 0 <= self.ball.velocity < 0.5:
                    self.ball.velocity += 1

            elif abs(self.postTwo.rect.bottom - self.ball.rect.top) < self.ball.velocity + self.collisionTolerance and 0 < abs(self.ball.angle) < (math.pi / 2): # hit from bottom
                self.ball.angle = math.pi - self.ball.angle
                self.ball.velocity *= Sprite_Physics.elasticity

            elif abs(self.postTwo.rect.left - self.ball.rect.right) < self.ball.velocity + self.collisionTolerance and 0 < self.ball.angle < math.pi: # hit from left
                if 0 < self.ball.angle < math.pi:
                    self.ball.angle = -self.ball.angle
                else:
                    self.ball.angle = math.pi + self.ball.angle

            # self.ball.velocity *= Sprite_Physics.elasticity

    def checkGoalLeft(self):
        if self.ball.rect.colliderect(self.goalOne) and abs(self.ball.rect.right - self.goalOne.rect.right) < self.ball.velocity:
            if not self.scored:
                self.scored = True
                self.score[1] += 1
                self.control = False
                self.playerOne.change_state("lost")
                self.playerTwo.change_state("won")
                self.goal_time = time.perf_counter()

    def checkGoalRight(self):
        if self.ball.rect.colliderect(self.goalTwo) and abs(self.ball.rect.left - self.goalTwo.rect.left) < self.ball.velocity:
            if not self.scored:
                self.scored = True
                self.score[0] += 1
                self.control = False
                self.playerOne.change_state("won")
                self.playerTwo.change_state("lost")
                self.goal_time = time.perf_counter()

    def checkLeftBounds(self, sprite):
        if sprite.rect.x > sprite.velocity:
            return True

        return False

    def checkRightBounds(self, sprite):
        if sprite.rect.x < self.screen.get_width() - sprite.velocity - sprite.rect.width:
            return True

        return False

    def goal_animation(self):
        if not self.scored:
            return

        if time.perf_counter() - self.goal_time >= 5:
            self.scored = False
            self.control = True
            self.playerOne.change_state("default")
            self.playerTwo.change_state("default")
            self.goal_time = None
            self.ball.rect.x = self.ball_start_pos[0]
            self.ball.rect.y = self.ball_start_pos[1]
            self.ball.init_ball()

            self.playerOne.rect.x = self.player_one_startPos[0]
            self.playerOne.rect.y = self.player_one_startPos[1]

            self.playerTwo.rect.x = self.player_two_startPos[0]
            self.playerTwo.rect.y = self.player_two_startPos[1]

    def display_score(self):
        self.score_text = self.my_font.render(f"{self.score[0]} : {self.score[1]}", True, (0, 0, 255))
        self.screen.blit(self.score_text, (845, 20))

    def update_foot(self, player, foot):
        if player.player_side == "left":
            foot.rect.x = player.rect.x + self.left_foot_offset_X
            foot.rect.y = player.rect.y + self.left_foot_offset_Y

        else:
            foot.rect.x = player.rect.x - self.right_foot_offset_X
            foot.rect.y = player.rect.y + self.right_foot_offset_Y


        # if self.kick_left is True:
        #     self.footOne.rect.x += 50
        #     self.footOne.rect.y += 50
        # else:
        #     self.footOne.rect.x -= 50
        #     self.footOne.rect.y -= 50
        #
        # if self.kick_right is True:
        #     self.footTwo.rect.x -= 50
        #     self.footTwo.rect.y += 50
        # else:
        #     self.footTwo.rect.x += 50
        #     self.footTwo.rect.y -= 50

    def check_ball_speed(self):
        if self.ball.velocity > self.ball.speed_threshold:
            self.ball.make_angry()
        else:
            self.ball.make_happy()

    def run_offline(self):
        # Add game loop if needed

        # player one
        a_down = False
        d_down = False
        kick_left = False

        # player two
        left_down = False
        right_down = False
        kick_right = False

        while True:
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()
                elif event.type == pygame.KEYDOWN and self.control:
                    if event.key == pygame.K_LEFT:
                        left_down = True

                    elif event.key == pygame.K_RIGHT:
                        right_down = True

                    elif event.key == pygame.K_p:
                        kick_right = True

                    elif event.key == pygame.K_a:
                        a_down = True

                    elif event.key == pygame.K_d:
                        d_down = True

                    elif event.key == pygame.K_SPACE:
                        kick_left = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left_down = False

                    elif event.key == pygame.K_RIGHT:
                        right_down = False

                    elif event.key == pygame.K_p:
                        kick_right = False

                    elif event.key == pygame.K_a:
                        a_down = False

                    elif event.key == pygame.K_d:
                        d_down = False

                    elif event.key == pygame.K_SPACE:
                        kick_left = False

            if True:
                if left_down and not right_down:
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

                if right_down and not left_down:
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

                if a_down and not d_down:
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

                if d_down and not a_down:
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

                if kick_right and self.footTwo.foot_angle < self.footTwo.MAX_FOOT_ANGLE:
                    self.right_foot_offset_Y -= 10 # 4 domyślnie
                    self.right_foot_offset_X += 0.5
                    self.footTwo.kick_right_foot()
                else:
                    if self.footTwo.foot_angle > 0:
                        self.footTwo.foot_angle -= self.footTwo.FOOT_ANGLE_VELOCITY
                        self.right_foot_offset_Y += 10 # 4 domyślnie
                        self.right_foot_offset_X -= 0.5
                        self.footTwo.rotate_foot()

                if kick_left and self.footOne.foot_angle > -self.footOne.MAX_FOOT_ANGLE:
                    self.left_foot_offset_Y -= 10 # 4 domyślnie
                    self.left_foot_offset_X += 7.5
                    self.footOne.kick_left_foot()
                else:
                    if self.footOne.foot_angle < 0:
                        self.footOne.foot_angle += self.footOne.FOOT_ANGLE_VELOCITY
                        self.left_foot_offset_Y += 10 # 4 domyślnie
                        self.left_foot_offset_X -= 7.5
                        self.footOne.rotate_foot()

            #print(self.footOne.foot_angle)

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

            self.checkCollisionPlayer(self.ball, self.playerOne)
            self.checkCollisionPlayer(self.ball, self.playerTwo)
            self.checkCollisionPostTwo()
            self.checkCollisionPostOne()
            self.checkGoalLeft()
            self.checkGoalRight()
            self.update_foot(self.playerOne, self.footOne)
            self.update_foot(self.playerTwo, self.footTwo)
            self.checkCollisionFoot(self.ball, self.footOne, self.playerOne)
            self.checkCollisionFoot(self.ball, self.footTwo, self.playerTwo)
            self.check_ball_speed()
            self.goal_animation()

            self.ball.bounce(self.screen, self.lower_bounds)
            self.ball.move()
            self.display_score()

            # Update the display
            self.refresh()
            pygame.display.update()

    def run_online_host(self):
        # Add game loop if needed

        a_down = False
        d_down = False
        kick_left = False

        # startujemy tu server
        # dodajemy klientów, którzy są threadami, na każdym threadzie są while, które słuchają event.keyów
        # te event keye są w pętli głównej servera nasłuchiwane
        # jak zrobić w tym wypadku wyświetlanie całej gry u klientów???

        while True:
            pygame.time.delay(20)

            # even handling for server-client side (player one)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()
                elif event.type == pygame.KEYDOWN and self.control:

                    if event.key == pygame.K_a:
                        a_down = True

                    elif event.key == pygame.K_d:
                        d_down = True

                    elif event.key == pygame.K_SPACE:
                        kick_left = True

                elif event.type == pygame.KEYUP:

                    if event.key == pygame.K_a:
                        a_down = False

                    elif event.key == pygame.K_d:
                        d_down = False

                    elif event.key == pygame.K_SPACE:
                        kick_left = False

            if True:
                if self.left_down and not self.right_down:
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

                if self.right_down and not self.left_down:
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

                if a_down and not d_down:
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

                if d_down and not a_down:
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

                if self.kick_right and self.footTwo.foot_angle < self.footTwo.MAX_FOOT_ANGLE:
                    self.right_foot_offset_Y -= 10  # 4 domyślnie
                    self.right_foot_offset_X += 0.5
                    self.footTwo.kick_right_foot()
                else:
                    if self.footTwo.foot_angle > 0:
                        self.footTwo.foot_angle -= self.footTwo.FOOT_ANGLE_VELOCITY
                        self.right_foot_offset_Y += 10  # 4 domyślnie
                        self.right_foot_offset_X -= 0.5
                        self.footTwo.rotate_foot()

                if kick_left and self.footOne.foot_angle > -self.footOne.MAX_FOOT_ANGLE:
                    self.left_foot_offset_Y -= 10  # 4 domyślnie
                    self.left_foot_offset_X += 7.5
                    self.footOne.kick_left_foot()
                else:
                    if self.footOne.foot_angle < 0:
                        self.footOne.foot_angle += self.footOne.FOOT_ANGLE_VELOCITY
                        self.left_foot_offset_Y += 10  # 4 domyślnie
                        self.left_foot_offset_X -= 7.5
                        self.footOne.rotate_foot()

            # print(self.footOne.foot_angle)

            # print(self.playerOne.velocity)
            # print(self.playerTwo.velocity)

            keys = pygame.key.get_pressed()

            if not self.playerTwo.isJumping:
                if self.player_two_jump_pressed:
                    self.playerTwo.isJumping = True

            else:
                self.playerTwo.jump()

            if not self.playerOne.isJumping:
                if keys[pygame.K_w]:
                    self.playerOne.isJumping = True

            else:
                self.playerOne.jump()

            self.checkCollisionPlayer(self.ball, self.playerOne)
            self.checkCollisionPlayer(self.ball, self.playerTwo)
            self.checkCollisionPostTwo()
            self.checkCollisionPostOne()
            self.checkGoalLeft()
            self.checkGoalRight()
            self.update_foot(self.playerOne, self.footOne)
            self.update_foot(self.playerTwo, self.footTwo)
            self.checkCollisionFoot(self.ball, self.footOne, self.playerOne)
            self.checkCollisionFoot(self.ball, self.footTwo, self.playerTwo)
            self.check_ball_speed()
            self.goal_animation()

            self.ball.bounce(self.screen, self.lower_bounds)
            self.ball.move()
            self.display_score()

            # Update the display
            self.refresh()
            pygame.display.update()

    def run_online_client(self):

        self.left_down = False
        self.right_down = False
        self.kick_right = False
        self.player_two_jump_pressed = False

        while True:
            pygame.time.delay(20)

            # even handling for server-client side (player one)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()
                elif event.type == pygame.KEYDOWN and self.control:

                    if event.key == pygame.K_LEFT:
                        self.left_down = True

                    elif event.key == pygame.K_RIGHT:
                        self.right_down = True

                    elif event.key == pygame.K_UP:
                        self.player_two_jump_pressed = True

                    elif event.key == pygame.K_p:
                        self.kick_right = True

                elif event.type == pygame.KEYUP:

                    if event.key == pygame.K_LEFT:
                        self.left_down = False

                    elif event.key == pygame.K_RIGHT:
                        self.right_down = False

                    elif event.key == pygame.K_UP:
                        self.player_two_jump_pressed = False

                    elif event.key == pygame.K_p:
                        self.kick_right = False

            self.display_score()
            self.refresh()

    def refresh(self):
        self.screen.blit(self.background, (0, 0))
        self.ball.draw_ball(self.screen)
        self.playerOne.draw_player(self.screen)
        self.footOne.draw_foot(self.screen)
        self.playerTwo.draw_player(self.screen)
        self.footTwo.draw_foot(self.screen)
        self.postOne.draw_post(self.screen)
        self.postTwo.draw_post(self.screen)
        self.goalOne.draw_goal(self.screen)
        self.goalTwo.draw_goal(self.screen)
        self.display_score()
        pygame.display.flip()

    def run_client_thread(self):
        server_addr = '127.0.0.1'
        port = 5555

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((server_addr, port))
        except socket.error as e:
            str(e)

        while True:
            # left pressed, right pressed, up_pressed, kick_pressed
            data_to_send = {'left_pressed': self.left_down,
                            'right_pressed': self.right_down,
                            'up_pressed': self.player_two_jump_pressed,
                            'kick_pressed': self.kick_right}

            json_data = json.dumps(data_to_send).encode('utf-8')

            client_socket.send(json_data)

            data_from_server = client_socket.recv(2048)
            json_objects = data_from_server.split(b'\n')
            for json_object in json_objects:
                try:
                    server_data = json.loads(json_object.decode('utf-8'))

                    # left pressed, right pressed, up_pressed, kick_pressed
                    self.ball.rect.x = server_data['ball_x']
                    self.ball.rect.y = server_data['ball_y']
                    self.playerOne.rect.x = server_data['player_one_x']
                    self.playerOne.rect.y = server_data['player_one_y']
                    self.footOne.rect.x = server_data['foot_one_x']
                    self.footOne.rect.y = server_data['foot_one_y']
                    self.playerTwo.rect.x = server_data['player_two_x']
                    self.playerTwo.rect.y = server_data['player_two_y']
                    self.footTwo.rect.x = server_data['foot_two_x']
                    self.footTwo.rect.y = server_data['foot_two_y']
                    self.score = server_data['score']
                except json.decoder.JSONDecodeError:
                    pass

        client_socket.close()

    def run_server_thread(self):
        server = '127.0.0.1'
        port = 5555

        print("run_server_thread STARTED!!!!")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.bind((server, port))
        except socket.error as e:
            str(e)

        server_socket.listen(1)
        print("Waiting for a connection, Server Started")

        # connection is an object representing what is connected
        connection, address = server_socket.accept()
        print("Connected to: ", address)

        while True:
            # ball_x, ball_y, p1_x, p1_y, f1_x, f1_y, p2_x, p2_y, f2_x, f2_y, score_left, score_right
            data_to_send = {'ball_x': self.ball.rect.x,
                            'ball_y': self.ball.rect.y,
                            'player_one_x': self.playerOne.rect.x,
                            'player_one_y': self.playerOne.rect.y,
                            'foot_one_x': self.footOne.rect.x,
                            'foot_one_y': self.footOne.rect.y,
                            'player_two_x': self.playerTwo.rect.x,
                            'player_two_y': self.playerTwo.rect.y,
                            'foot_two_x': self.footTwo.rect.x,
                            'foot_two_y': self.footTwo.rect.y,
                            'score': self.score}

            json_data = json.dumps(data_to_send).encode('utf-8')

            connection.send(json_data)

            data_from_client = connection.recv(2048)
            json_objects = data_from_client.split(b'\n')
            for json_object in json_objects:

                try:
                    client_data = json.loads(json_object.decode('utf-8'))

                    # left pressed, right pressed, up_pressed, kick_pressed
                    self.left_down = client_data['left_pressed']
                    self.right_down = client_data['right_pressed']
                    self.kick_right = client_data['kick_pressed']
                    self.player_two_jump_pressed = client_data['up_pressed']

                except json.decoder.JSONDecodeError:
                    pass


        server_socket.close()
