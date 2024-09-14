import pygame
from settings import *

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.speed = OBSTACLE_SPEED

    def move(self, speed_up):
        self.rect.y += self.speed * (2 if speed_up else 1)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)
