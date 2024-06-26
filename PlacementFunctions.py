import pygame
import time

REPOS_OBJECT = 1
REPOS_ROTATION_CENTER = 2
RESCALE_OBJECT = 3

class MapObject:
    def __init__(self, imgname, posx=0, posy=0, size=(20,20), rotationcenter=None, angle=0):
        self.imgname = imgname
        self.img = pygame.transform.smoothscale(pygame.image.load("textures/"+imgname), size)
        self.original_img = self.img
        self.reposition = 0
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = posx, posy
        self.originaloffset = pygame.Vector2(0, 0)
        self.mask = pygame.mask.from_surface(self.img)
        if rotationcenter is None:
            self.rotationcenter = self.rect.center
        else:
            self.rotationcenter = rotationcenter
        self.mouseoffset = (0,0)
        self.angle = angle
        self.rotating = False

    def display(self, surface):
        surface.blit(self.img, self.rect)
        pygame.draw.circle(surface, (255,0,0), self.rotationcenter, 3)
        pygame.draw.line(surface, (0, 255, 255), self.rect.center, self.rotationcenter)
    def move_at(self, pos):
        pos = pygame.Vector2(pos[0], pos[1])
        offset = pygame.Vector2(self.rect.center)
        offset = self.rotationcenter-offset

        self.rect.center = pygame.Vector2(pos)
        self.rotationcenter = pos + offset

    def collidesmouse(self):
        mouse_pos = pygame.mouse.get_pos()
        pos_distance = (mouse_pos[0]-self.rect.x, mouse_pos[1]-self.rect.y)
        self.mouseoffset = (self.rect.center[0] - mouse_pos[0], self.rect.center[1] - mouse_pos[1])
        return self.rect.collidepoint(mouse_pos) and self.mask.get_at(pos_distance)

    def resize(self, size):
        self.rect.height = size[0]
        self.rect.width = size[0]
        self.img = self.rect.size

    def rotate_around_point(self, angle):
        self.angle+=angle
        rotated_img = pygame.transform.rotate(self.original_img, self.angle)
        origin_vec = pygame.Vector2(self.rect.center)
        pivot_vec = pygame.Vector2(self.rotationcenter)
        #origin_vec.from_polar((self.rect.center[0], self.rect.center[1]))
        #pivot_vec.from_polar((self.rotationcenter[0], self.rotationcenter[1]))

        offset = pivot_vec - origin_vec
        new_center = pivot_vec - self.originaloffset.rotate(-self.angle)
        self.rect = rotated_img.get_rect(center=new_center)
        self.img = rotated_img
        self.mask = pygame.mask.from_surface(self.img)

    def rescale(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self.mouseoffset = (- self.rect.y + mouse_pos[0], - self.rect.y + mouse_pos[1])
        self.rect.size = abs(self.mouseoffset[0]), abs(self.mouseoffset[1])
        pygame.draw.rect(surface, (255, 50, 10), self.rect, 3)
        self.img = pygame.transform.smoothscale(self.original_img, self.rect.size)
        print(self.mouseoffset[0], self.mouseoffset[1])

    def update(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        if self.reposition == REPOS_OBJECT:
            self.move_at(mouse_pos+pygame.Vector2(self.mouseoffset))
        elif self.reposition == REPOS_ROTATION_CENTER:
            self.rotationcenter = mouse_pos
            self.originaloffset = pygame.Vector2(self.rotationcenter)-pygame.Vector2(self.rect.center)
        elif self.reposition == RESCALE_OBJECT:
            self.rescale(surface)
        self.display(surface)

'''
Guide de la classe MapObject:
- Reposition = 1 : Change la position de l'objet par rapport à la souris
- Reposition = 2 : change la position du centre de rotation de l'objet par rapport à la souris
'''