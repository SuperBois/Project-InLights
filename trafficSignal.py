import time

import pygame


class TrafficSignal:
    def __init__(self):
        self.color = 0  # 0 for red , 1 for yellow, 2 for green


def green():
    UpSignal.color = 1
    UpSignal.image = pygame.image.load("Images//yellow.png")
    UpSignal.color = 2
    UpSignal.image = pygame.image.load("Images//green.png")


def red():
    UpSignal.color = 0
    UpSignal.image = pygame.image.load("Images//red.png")


def yellow():
    UpSignal.color = 1
    UpSignal.image = pygame.image.load("Images//yellow.png")


def isRed():
    return UpSignal.color == 0
    
def isYellow():
    return UpSignal.color == 1

def isGreen():
    return UpSignal.color == 2


class UpSignal:
    image = pygame.image.load("Images//red.png")
    rect = pygame.rect.Rect(0, 0, image.get_width(), image.get_height())
    rect.x = 330
    rect.y = 655
    color = 0
