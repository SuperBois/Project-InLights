import math
import random

import pygame

from trafficSignal import *


class Car:
    def __init__(self, speed):
        self.speed = 15
        self.crossed = False
        self.image = None
        self.original_image = None
        self.rect = None


class UpCar(Car):
    id = 0
    pos_x = 400
    pos_y = 1050
    carList = {}
    lanes = 4

    def __init__(self):
        super().__init__(100)
        # initializing the car object
        self.image = pygame.image.load("Images//car_up.png")
        self.original_image = self.image
        # create rect and set its position
        self.rect = pygame.rect.Rect(UpCar.pos_x, UpCar.pos_y, self.original_image.get_width(),
                                     self.original_image.get_height() + 30)
        self.rect.x = 400 + (30 * (self.id % UpCar.lanes))
        self.rect.y = UpCar.pos_y
        # assign a unique id to the car
        self.id = UpCar.id
        # set the angles for the rotation of the car
        self.angle = 0
        self.next_angle = 90
        self.angle_increment = 15
        self.rotate = False
        # add the car to carList and update car id
        UpCar.carList[self.id] = self.rect
        UpCar.id += 1

    def resetCar(self):
        # resets the car to start from the bottom
        self.id = UpCar.id
        self.angle = 0
        self.next_angle = 90
        self.angle_increment = 15
        # resets the rotation and position of the car
        self.rotate = False
        self.rot_center()
        self.rect.x = 400 + (30 * (self.id % UpCar.lanes))
        self.rect.y = UpCar.pos_y
        # adding the car to the car list
        UpCar.carList[self.id] = self.rect
        UpCar.id += 1

    def rot_center(self):
        # rotates the original image
        rotated_image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)
        # assign the rotated image and rect to the image and rect of this car
        self.image = rotated_image
        self.rect = new_rect
        # stretches the rect by 30 px along y
        self.rect.inflate_ip(0, 30)

    def shouldRotate(self):
        # checks whether to start the rotation of car from angle to next_angle
        if self.rotate and self.angle != self.next_angle:
            self.angle += self.angle_increment
            self.rot_center()
        # if the rotation is completed
        if self.angle == self.next_angle:
            self.rotate = False

    def move(self):
        # move the car if it should not stop
        if not self.shouldStop():
            self.rect.x += round(self.speed * math.cos(math.radians(self.angle + 90)))
            self.rect.y -= round(self.speed * math.sin(math.radians(self.angle + 90)))
        # rotate the car if it has crossed the junction
        if self.id % UpCar.lanes == 3 and 480 < self.rect.y < 500:
            self.rotate = True
        elif self.id % UpCar.lanes != 3 and 580 < self.rect.y < 590:
            self.rotate = True
        # rotate the car towards left if it is in the first lane
        if self.id % UpCar.lanes == 0:
            self.next_angle = 90
            self.angle_increment = 15
        # dont rotate the car in the middle two lanes
        if self.id % UpCar.lanes in [1, 2]:
            self.next_angle = 0
            self.angle_increment = 15
        # rotate the car towards right if it is in the 4th lane
        if self.id % UpCar.lanes == 3:
                self.next_angle = -90
                self.angle_increment = -15
        # calling the functions to check if the car should rotate or reposition
        self.shouldRotate()
        self.shouldReset()
        # update the position of the rect in the class variable carList
        UpCar.carList[self.id] = self.rect

    def shouldStop(self):
        # send stop signal if traffic signal is red
        if 630 < self.rect.y < 650 and isRed():
            return True
        # # send stop signal if car is about to collide with next car

        if self.id > UpCar.lanes - 1:
            car_rect = UpCar.carList[self.id - UpCar.lanes]
            if self.rect.colliderect(car_rect):
                # return true if the car is behind the colliding rect
                if self.rect.y - car_rect.y >= 10 and car_rect.y > 0:
                    return True

        # keep the car moving else
        return False

    def shouldReset(self):
        # repositions the car that goes out of the screen
        if self.rect.x < 0 or self.rect.x > 1100 or self.rect.y > 1100 or self.rect.y < 0:
            self.resetCar()
