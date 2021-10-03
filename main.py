# Simple pygame program
# Import and initialize the pygame library
import random

import pygame
from car import *
from trafficSignal import *
from timer import *
import time

pygame.init()

font = pygame.font.SysFont("Consolas",30)
clock = pygame.time.Clock()
# Set up the drawing window
screen = pygame.display.set_mode([1050, 1050])
# Run until the user asks to quit
running = True

signal_time = 0

car_list = []  # a list that stores the reference of every single car

# for i in range(10):
#     car = UpCar()
#     car_list.append(car)

i = 0
car_count = 0
background = pygame.image.load("Images\\background.png")

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # measuring time
    current_time = pygame.time.get_ticks()
    
    # Fill the background with white
    screen.blit(background, (0,0,0,0))

    # displaying all cars on the screen
    for car in car_list:
        screen.blit(car.image, car.rect)
        car.move()
    
    screen.blit(UpSignal.image, UpSignal.rect)
    elapsed_time = (current_time - signal_time)
    
    # Displaying time on screen
    draw_time(screen, f"Master Time: {int(current_time / 1000)} sec", font, 200, 150)
    draw_time(screen, f"Signal Time:  {int(elapsed_time / 1000)} sec", font, 200, 700)
    
    # Flip the display
    pygame.display.flip()

    if random.randint(1,10) == 5 and car_count < 15:
        car = UpCar()
        car_list.append(car)
        car_count += 1

    #print(elapsed_time/1000, " seconds passed")
    #print(current_time / 1000, " seconds passed")
    
    
    # After 10 seconds, change red signal to yellow
    if isRed() and elapsed_time > 10000:
        yellow()
        signal_time = current_time
        
    # After 5 seconds, change yellow signal to green
    elif isYellow() and elapsed_time > 5000:
        green()
        signal_time = current_time

    # After 10 seconds, change green to red
    elif isGreen() and elapsed_time > 10000:
        red()
        signal_time = current_time

    clock.tick(30)

# Done! Time to quit.
pygame.quit()
