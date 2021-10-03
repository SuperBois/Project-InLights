# Simple pygame program
# Import and initialize the pygame library
import random

import pygame
from car import *
from trafficSignal import *

pygame.init()


clock = pygame.time.Clock()
# Set up the drawing window
screen = pygame.display.set_mode([1050, 1050])
# Run until the user asks to quit
running = True

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

    # Fill the background with white
    screen.blit(background, (0,0,0,0))

    # displaying all cars on the screen
    for car in car_list:
        screen.blit(car.image, car.rect)
        car.move()
    screen.blit(UpSignal.image, UpSignal.rect)
    # Flip the display
    pygame.display.flip()

    if random.randint(1,10) == 5 and car_count < 10:
        car = UpCar()
        car_list.append(car)
        car_count += 1
    if i > 150:
        if isRed():
            if i < 200:
                yellow()
            else:
                green()
                i = 0
        else:
            red()
            i=0
    i += 1

    clock.tick(30)

# Done! Time to quit.
pygame.quit()
