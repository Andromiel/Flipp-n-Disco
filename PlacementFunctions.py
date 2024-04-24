import pygame
import time

REPOS_OBJECT = 1
REPOS_ROTATION_CENTER = 2
class MapObject:
    def __init__(self, img, posx=0, posy=0, rotationcenter=None):
        self.original_img = img
        self.img = img
        self.reposition = 0
        self.rect = img.get_rect()
        self.rect.x, self.rect.y = posx, posy
        self.originaloffset = pygame.Vector2(0, 0)
        self.mask = pygame.mask.from_surface(self.img)
        self.rotationcenter = self.rect.center
        self.mouseoffset = (0,0)
        self.img_angle = 0
        self.rotation_vec_angle = 0
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
        self.img_angle+=angle
        self.rotation_vec_angle+=angle
        rotated_img = pygame.transform.rotate(self.original_img, self.img_angle)
        origin_vec = pygame.Vector2(self.rect.center)
        pivot_vec = pygame.Vector2(self.rotationcenter)
        #origin_vec.from_polar((self.rect.center[0], self.rect.center[1]))
        #pivot_vec.from_polar((self.rotationcenter[0], self.rotationcenter[1]))

        offset = pivot_vec - origin_vec
        new_center = pivot_vec - self.originaloffset.rotate(-self.rotation_vec_angle)
        self.rect = rotated_img.get_rect(center=new_center)
        self.img = rotated_img
        self.mask = pygame.mask.from_surface(self.img)


    def update(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        if self.reposition == REPOS_OBJECT:
            self.move_at(mouse_pos+pygame.Vector2(self.mouseoffset))
        elif self.reposition == REPOS_ROTATION_CENTER:
            self.rotationcenter = mouse_pos
            self.originaloffset = pygame.Vector2(self.rotationcenter)-pygame.Vector2(self.rect.center)
            self.rotation_vec_angle = 0
        self.display(surface)

'''
Guide de la classe MapObject:
- Reposition = 1 : Change la position de l'objet par rapport à la souris
- Reposition = 2 : change la position du centre de rotation de l'objet par rapport à la souris
'''