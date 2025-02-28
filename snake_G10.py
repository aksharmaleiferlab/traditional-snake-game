#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 23:16:38 2025

@author: aksharma
"""

import pygame
import time
import random

pygame.init()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
GRAY = (100, 100, 100)

# Display settings
DIS_WIDTH = 800
DIS_HEIGHT = 600
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game - 10 Stages')

# Game constants
SNAKE_BLOCK = 10
INITIAL_SPEED = 10

# Font
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

clock = pygame.time.Clock()

def our_snake(snake_block, snake_list):
    """Draw the snake on the screen"""
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], snake_block, snake_block])

def message(msg, color, x, y):
    """Display message at specified position"""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [x, y])

def show_score(score, stage):
    """Display current score and stage"""
    score_text = score_font.render(f"Score: {score}", True, YELLOW)
    stage_text = score_font.render(f"Stage: {stage}", True, WHITE)
    dis.blit(score_text, [0, 0])
    dis.blit(stage_text, [DIS_WIDTH - 100, 0])

def create_obstacles(stage):
    """Create obstacles based on stage number"""
    obstacles = []
    num_obstacles = stage * 2  # More obstacles with higher stages
    for _ in range(min(num_obstacles, 20)):  # Cap at 20 obstacles
        while True:
            x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            if [x, y] not in obstacles and x != DIS_WIDTH/2 and y != DIS_HEIGHT/2:
                obstacles.append([x, y])
                break
    return obstacles

def draw_obstacles(obstacles):
    """Draw obstacles on screen"""
    for obs in obstacles:
        pygame.draw.rect(dis, GRAY, [obs[0], obs[1], SNAKE_BLOCK, SNAKE_BLOCK])

def gameLoop():
    game_over = False
    game_close = False
    current_stage = 1
    max_stage = 10
    
    # Initial snake position
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    snake_speed = INITIAL_SPEED
    food_eaten = 0
    food_needed = 3  # Initial food needed to advance stage

    # Initial food position
    foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
    
    obstacles = create_obstacles(current_stage)

    while not game_over:
        while game_close:
            dis.fill(BLUE)
            if current_stage > max_stage:
                message("You Won! All Stages Complete!", GREEN, DIS_WIDTH/6, DIS_HEIGHT/3)
            else:
                message("You Lost! Q-Quit or C-Play Again", RED, DIS_WIDTH/6, DIS_HEIGHT/3)
            show_score(length_of_snake - 1, current_stage)
            our_snake(SNAKE_BLOCK, snake_list)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        # Reset game variables
                        x1 = DIS_WIDTH / 2
                        y1 = DIS_HEIGHT / 2
                        x1_change = 0
                        y1_change = 0
                        snake_list = []
                        length_of_snake = 1
                        snake_speed = INITIAL_SPEED
                        food_eaten = 0
                        food_needed = 3
                        current_stage = 1
                        foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                        foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                        obstacles = create_obstacles(current_stage)
                        game_close = False
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != SNAKE_BLOCK:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -SNAKE_BLOCK:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != SNAKE_BLOCK:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -SNAKE_BLOCK:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Check boundaries and obstacles
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0 or [x1, y1] in obstacles:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(BLUE)
        
        # Draw elements
        draw_obstacles(obstacles)
        pygame.draw.rect(dis, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        
        # Update snake
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check self-collision
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(SNAKE_BLOCK, snake_list)
        show_score(length_of_snake - 1, current_stage)
        pygame.display.update()

        # Check food collision
        if x1 == foodx and y1 == foody:
            while True:
                foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                if [foodx, foody] not in obstacles and [foodx, foody] not in snake_list:
                    break
            length_of_snake += 1
            food_eaten += 1
            
            # Stage progression
            if food_eaten >= food_needed and current_stage <= max_stage:
                current_stage += 1
                food_eaten = 0
                food_needed += 1  # Need more food for next stage
                snake_speed += 2   # Speed increases
                obstacles = create_obstacles(current_stage)
                message(f"Stage {current_stage}!", WHITE, DIS_WIDTH/3, DIS_HEIGHT/2)
                pygame.display.update()
                time.sleep(1)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()