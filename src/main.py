import pygame
import os
from settings import *
from player import Player
from obstacle import Obstacle
import random

pygame.init()
pygame.mixer.init()  

def create_obstacle(obstacles):
    x_pos = random.randint(0, WIDTH - OBSTACLE_WIDTH)
    obstacles.append(Obstacle(x_pos, -OBSTACLE_HEIGHT))

def show_game_over_screen(screen, restart_func):
    font = pygame.font.SysFont(None, 55)
    text = font.render("Game Over! Press R to Restart or Q to Quit", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_func()
                    waiting_for_input = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def game_loop():
    player = Player()
    obstacles = []
    obstacle_timer = 0
    sound_played = False 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        player.move(keys)

        if keys[pygame.K_UP]:
            player.speed_up = True
            if not sound_played:  
                accelerate_sound.play(-1) 
                sound_played = True
        else:
            player.speed_up = False
            accelerate_sound.stop()
            sound_played = False

        if obstacle_timer > OBSTACLE_FREQUENCY:
            create_obstacle(obstacles) 
            obstacle_timer = 0
        obstacle_timer += 1

        screen.fill(WHITE)
        player.draw(screen)

        collision_detected = False 
        for obstacle in obstacles:
            obstacle.move(player.speed_up)
            obstacle.draw(screen)
            if obstacle.check_collision(player.rect):
                if not collision_detected: 
                    crash_sound.play()
                    accelerate_sound.stop()  
                    collision_detected = True
                show_game_over_screen(screen, game_loop) 
                return  

        pygame.display.flip()
        clock.tick(60)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Racing Game")
clock = pygame.time.Clock()


crash_sound_path = os.path.join('src', 'crash.wav')
accelerate_sound_path = os.path.join('src', 'accelerate.wav')
crash_sound = pygame.mixer.Sound(crash_sound_path)
accelerate_sound = pygame.mixer.Sound(accelerate_sound_path)

game_loop()
