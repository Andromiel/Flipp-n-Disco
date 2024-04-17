import pygame
import time
from PlacementFunctions import *

pygame.init()

screen = pygame.display.set_mode((500,600))
Ball = MapObject(pygame.transform.scale(pygame.image.load("textures/ball.png"), (60,60)), 50,50)
Disk = MapObject(pygame.transform.scale(pygame.image.load("textures/disk.png"), (60,60)), 0,0)
Flipper = MapObject(pygame.transform.scale(pygame.image.load("textures/flipper.png"), (100,60)), 90,90)
Objects = [Disk, Ball, Flipper]
loop = True
angle = 360
count = 0
while loop:
    screen.fill((30, 90, 120))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        for object in Objects:
            if event.type == pygame.MOUSEBUTTONDOWN and object.collidesmouse():
                if event.button == 1:
                    object.reposition = 1
                elif event.button == 3:
                    object.reposition = 2
            elif event.type == pygame.MOUSEBUTTONUP:
                object.reposition = 0
            elif event.type == pygame.KEYDOWN:
                object.rotate_around_point()

    Ball.update(screen)
    Disk.update(screen)
    Flipper.update(screen)
    pygame.display.flip()

