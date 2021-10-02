import time

import pygame

class TrafficSignal():
    def __init__(self):
        self.color = 0  # 0 for red , 1 for yellow, 2 for green

    def green(self):
        self.color = 1
        self.color = 2

class UpSignal(TrafficSignal):
    color = 2  # 0 for red , 1 for yellow, 2 for green


