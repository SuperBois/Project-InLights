import math
import random

import pygame

from trafficSignal import UpSignal


class Car:
    def __init__(self, speed):
        self.speed = 15
        self.crossed = False
        self.image = None
        self.original_image = None
        self.rect = None

    def set_crossed(self):
        self.crossed = True


class UpCar(Car):
    id = 0
    pos_x = 400
    pos_y = 1050
    carList = {}
    lanes = 4

    def __init__(self):
        super().__init__(100)
        self.angle = 0
        self.next_angle = 180
        self.image = pygame.image.load("Images//car_up.png")
        self.original_image = self.image
        self.rect = pygame.rect.Rect(UpCar.pos_x, UpCar.pos_y, self.image.get_width(), self.image.get_height())
        self.id = UpCar.id
        self.angle_increment = 15
        self.rotate = False
        # the initial position of the new car
        if UpCar.pos_x >= 400 + (30 * (UpCar.lanes - 1)):
            UpCar.pos_x = 400
        else:
            UpCar.pos_x += 30
        # adding the car to the car list
        UpCar.carList[self.id] = self.rect
        UpCar.id += 1

    def rot_center(self):
        # rotates the original image
        rotated_image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(center=(self.rect.centerx, self.rect.centery)).center)
        self.image = rotated_image
        self.rect = new_rect

    def shouldRotate(self):
        # checks whether to start the rotation of car from angle to next_angle
        if self.rotate and self.angle != self.next_angle:
            self.angle += self.angle_increment
            self.rot_center()

        if self.angle == self.next_angle:
            self.rotate = False

    def move(self):
        # move the car if it should not stop
        if not self.shouldStop():
            self.rect.x += round(self.speed * math.cos(math.radians(self.angle + 90)))
            self.rect.y -= round(self.speed * math.sin(math.radians(self.angle + 90)))
        # rotate the car if it has crossed the junction
        if self.id % UpCar.lanes == 2 and 450 < self.rect.y < 460:
            self.rotate = True
        elif self.id % UpCar.lanes != 2 and 580 < self.rect.y < 590:
            self.rotate = True

        if self.id % UpCar.lanes == 0:
            self.next_angle = 90
            self.angle_increment = 15

        if self.id % UpCar.lanes == 1:
            self.next_angle = 0
            self.angle_increment = 15

        if self.id % UpCar.lanes == 2:
            self.next_angle = -90
            self.angle_increment = -15

        if self.id % UpCar.lanes == 3:
            self.next_angle = -180
            self.angle_increment = -15
        self.shouldRotate()
        UpCar.carList[self.id] = self.rect

    def shouldStop(self):
        # send stop signal if car signal is red
        if 590 < self.rect.y < 600 and UpSignal.color == 0:
            return True
        # send stop signal if car is about to collide with next car
        my_pos_x = UpCar.carList[self.id].x
        my_pos_y = UpCar.carList[self.id].y

        if self.id > UpCar.lanes - 1:
            next_pos_x = UpCar.carList[self.id - UpCar.lanes].x
            next_pos_y = UpCar.carList[self.id - UpCar.lanes].y

            if my_pos_x == next_pos_x and my_pos_y - next_pos_y <= 20:
                return True

        # keep the car moving else
        return False
