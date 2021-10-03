import math
import pygame

from trafficSignal import *


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

        self.image = pygame.image.load("Images//car_up.png")
        self.original_image = self.image
        self.rect = pygame.rect.Rect(UpCar.pos_x, UpCar.pos_y, self.original_image.get_width(),
                                     self.original_image.get_height()+30)
        self.rect.x = UpCar.pos_x
        self.rect.y = UpCar.pos_y
        UpCar.carList[self.id] = None
        self.id = UpCar.id
        self.angle = 0
        self.next_angle = 90
        self.angle_increment = 15
        self.rotate = False
        UpCar.carList[self.id] = self.rect
        UpCar.id += 1
        # the initial position of the new car
        if UpCar.pos_x >= 400 + (30 * (UpCar.lanes - 1)):
            UpCar.pos_x = 400
        else:
            UpCar.pos_x += 30

    def placeCar(self):
        self.rect.x = UpCar.pos_x
        self.rect.y = UpCar.pos_y
        self.id = UpCar.id
        self.angle = 0
        self.next_angle = 90
        self.angle_increment = 15
        self.rotate = False
        self.rot_center()

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
        if self.id % UpCar.lanes == 3 and 480 < self.rect.y < 500:
            self.rotate = True
        elif self.id % UpCar.lanes != 3 and 580 < self.rect.y < 590:
            self.rotate = True

        if self.id % UpCar.lanes == 0:
            self.next_angle = 90
            self.angle_increment = 15

        if self.id % UpCar.lanes in [1, 2]:
            self.next_angle = 0
            self.angle_increment = 15

        if self.id % UpCar.lanes == 3:
            self.next_angle = -90
            self.angle_increment = -15

        self.shouldRotate()
        self.shouldDelete()
        UpCar.carList[self.id] = self.rect

    def shouldStop(self):
        # send stop signal if traffic signal is red
        if 630 < self.rect.y < 650 and isRed():
            return True
        # # send stop signal if car is about to collide with next car
        # my_pos_x = UpCar.carList[self.id].x
        # my_pos_y = UpCar.carList[self.id].y
        #
        # if self.id > UpCar.lanes - 1:
        #     next_car = UpCar.carList[self.id - UpCar.lanes]
        #     if next_car is not None:
        #         next_pos_x = next_car.x
        #         next_pos_y = next_car.y
        #
        #         if my_pos_x == next_pos_x and my_pos_y - next_pos_y <= 60:
        #             return True

        for car_rect in UpCar.carList.values():
            # if any car rect collides with this car rect
            if self.rect != car_rect and self.rect.colliderect(car_rect):
                # return true if the car is behind the colliding rect
                    if self.rect.y - car_rect.y >= 10:
                        return True

        # keep the car moving else
        return False

    def shouldDelete(self):
        # delete the object if it goes of screen
        my_pos_x = self.rect.x
        my_pos_y = self.rect.y

        if self.rect.x < 0 or self.rect.x > 1100 or self.rect.y > 1100 or self.rect.y < 0:
            print(self.id, " is deleted")
            self.placeCar()
