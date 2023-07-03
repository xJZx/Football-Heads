import math
import pygame

class Sprite_Physics(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        Sprite_Physics.gravity = (math.pi, 0.2)
        Sprite_Physics.drag = 0.999
        Sprite_Physics.elasticity = 0.75

    # @staticmethod
    # def checkCollision(sprite_one, sprite_two):
    #     dx = sprite_one.rect.x - sprite_two.rect.x
    #     dy = sprite_one.rect.y - sprite_two.rect.y
    #
    #     distance = math.hypot(dx, dy)
    #     if distance < sprite_one.rect.width + sprite_two.rect.width:
    #         tangent = math.atan2(dy, dx)
    #         # sprite_one.angle = 2 * tangent - sprite_one.angle
    #         # sprite_two.angle = 2 * tangent - sprite_two.angle
    #         (sprite_one.velocity, sprite_two.velocity) = (sprite_two.velocity, sprite_one.velocity)
    #         # sprite_one.velocity *= Sprite_Physics.elasticity
    #         # sprite_two.velocity *= Sprite_Physics.elasticity
    #
    #         angle = 0.5 * math.pi + tangent
    #         sprite_one.rect.x += math.sin(angle)
    #         sprite_one.rect.y -= math.cos(angle)
    #         sprite_two.rect.x -= math.sin(angle)
    #         sprite_two.rect.y += math.cos(angle)
