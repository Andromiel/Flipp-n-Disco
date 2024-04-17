import pygame
import time


class MapObject:
    def __init__(self, img, posx=None, posy=None, rotationcenter=None):
        self.img = img
        self.pos = (posx, posy)
        self.reposition = 0
        self.rect = img.get_rect()
        self.rect.x, self.rect.y = posx, posy
        self.mask = pygame.mask.from_surface(self.img)
        self.rotationcenter = self.rect.center
        self.mouseoffset = (0,0)
        self.centeroffset = (0,0)
        self.angle = 0
        self.rotating = False

    def display(self, surface):
        surface.blit(self.img, self.rect)
        pygame.draw.circle(surface, (255,0,0), self.rotationcenter, 3)
        pygame.draw.line(surface, (0, 255, 255), self.rect.center, self.rotationcenter)

    def collidesmouse(self):
        mouse_pos = pygame.mouse.get_pos()
        pos_distance = (mouse_pos[0]-self.rect.x, mouse_pos[1]-self.rect.y)
        self.mouseoffset = (self.rect.x - mouse_pos[0], self.rect.y - mouse_pos[1])
        return self.rect.collidepoint(mouse_pos) and self.mask.get_at(pos_distance)

    def resize(self, size):
        self.rect.height = size[0]
        self.rect.width = size[0]
        self.img = self.rect.size

    def rotate_around_point(self):
        rotated_img = pygame.transform.rotate(self.img, 1)
        origin_vec = pygame.Vector2.from_polar((self.rect.center[0], self.rect.center[1]))
        pivot_vec = pygame.Vector2.from_polar((self.rotationcenter[0], self.rotationcenter[1]))
        offset = pivot_vec + (origin_vec - pivot_vec).rotate(-1)
        self.rect = rotated_img.get_rect(center=offset)

    def update(self, surface):
        if self.reposition == 1:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.x = mouse_pos[0]+self.mouseoffset[0]
            self.rect.y = mouse_pos[1]+self.mouseoffset[1]
        elif self.reposition == 2:
            mouse_pos = pygame.mouse.get_pos()
            self.centeroffset = (self.rect.centerx-mouse_pos[0], self.rect.centery-mouse_pos[1])
        if self.rotating:
            self.rotate_around_point()
        self.rotationcenter = (self.rect.center[0]-self.centeroffset[0], self.rect.center[1]-self.centeroffset[1])
        self.display(surface)

'''
Guide de la classe MapObject:
- Reposition = 1 : Change la position de l'objet par rapport à la souris
- Reposition = 2 : change la position du centre de rotation de l'objet par rapport à la souris
'''