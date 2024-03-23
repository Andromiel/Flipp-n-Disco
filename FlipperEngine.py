import pygame
import numpy as np
import random as rd
clock = pygame.time.Clock()
pygame.init()
loop = True

WIDTH = 1000
HEIGHT = 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")

class Flipper(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        if self.type == -1:
            self.image = pygame.transform.scale(pygame.image.load("textures/flipper.png"),(150,75))
        else:
            self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("textures/flipper.png"),(150,75)), True, False)
        self.x = x
        self.y = y
        self.angle = 0
        self.rotation = 0
        self.pivot = [self.x+75, self.y+35]

    def rotate_img(self):
        offset = pygame.math.Vector2(0,100)
        if self.rotation == 1:
            self.angle -= 2
            rotated_img = pygame.transform.rotozoom(self.image, self.angle, 1)
            rect = rotated_img.get_rect(center=self.pivot)
            return pygame.transform.rotate(self.image, self.type*self.angle), rect

        elif self.rotation == 2:
            self.angle += 2
            rotated_img = pygame.transform.rotozoom(self.image, self.angle, 1)
            rect = rotated_img.get_rect(center=self.pivot)
            return pygame.transform.rotate(self.image, self.type*self.angle), rect
    def update(self):

        if self.angle <= -50:
            self.rotation = 2
        elif self.angle == 0 and self.rotation == 2:
            self.rotation = 0

        if self.rotation != 0:
            rotated_img, rect = self.rotate_img()[0], self.rotate_img()[1]
            screen.blit(rotated_img, rect)
            pygame.draw.rect(screen, (30, 250, 70), rect, 1)
        else:
            screen.blit(self.image, (self.x, self.y))


flipper1 = Flipper(100,500, -1)
flipper2 = Flipper(250,500, 1)


while loop:
    pygame.draw.rect(screen, RED, pygame.Rect(0,0,500,800))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            loop = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                flipper1.rotation = 1
            if keys[pygame.K_RIGHT]:
                flipper2.rotation = 1
    print(pygame.mouse.get_pos())
    print(flipper1.angle)
    flipper1.update()
    flipper2.update()
    pygame.display.flip()
    clock.tick(60)
