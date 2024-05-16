import pygame
import time

DONT_MOVE = 0
REPOS_OBJECT = 1
REPOS_ROTATION_CENTER = 2
RESCALE_OBJECT = 3

class MapObject:
    def __init__(self, img, imgname, posx=0, posy=0, size=(20,20), show_rotating_point = False):
        self.imgname = imgname
        self.img = img
        self.original_img = self.img
        self.scaled_img = self.img
        self.reposition = 0
        self.rect = self.img.get_rect()
        self.rect.center = (posx, posy)
        self.original_rect = self.img.get_rect()
        self.original_size = size
        self.rect.x, self.rect.y = posx, posy
        self.originaloffset = pygame.Vector2(0, 0)
        self.mask = pygame.mask.from_surface(self.img)
        self.rotationcenter = self.rect.center
        self.mouseoffset = (0,0)
        self.angle = 0
        self.rotating = False

        self.size = 1
        self.show_rotating_point = show_rotating_point
        self.move_at((posx, posy))

        self.flipped = False
    def display(self, surface):
        surface.blit(self.img, self.rect)
        if self.show_rotating_point:
            pygame.draw.circle(surface, (255,0,0), self.rotationcenter, 3)
            pygame.draw.line(surface, (0, 255, 255), self.rect.center, self.rotationcenter)
    def move_at(self, pos):
        pos = pygame.Vector2(pos)
        offset = pygame.Vector2(self.rect.center)
        offset = self.rotationcenter-offset

        self.rect.center = pygame.Vector2(pos)
        self.rotationcenter = pos + offset

    def collidesmouse(self):
        mouse_pos = pygame.mouse.get_pos()
        pos_distance = (mouse_pos[0]-self.rect.x, mouse_pos[1]-self.rect.y)
        self.mouseoffset = (self.rect.center[0] - mouse_pos[0], self.rect.center[1] - mouse_pos[1])
        return self.rect.collidepoint(mouse_pos) and self.mask.get_at(pos_distance)

    def resize(self, size : float):
        self.size*=size
        center = self.rect.center
        self.rect.size=(self.rect.size[0]*size, self.rect.size[0]*size * self.original_rect.size[1]/self.original_rect.size[0])
        self.rect.center = center
        self.rotationcenter = self.rect.center + self.originaloffset*size
        self.img = pygame.transform.smoothscale(self.original_img, self.rect.size)
        if self.flipped:
            self.img = pygame.transform.flip(self.img, False, True)
        self.scaled_img = pygame.transform.smoothscale(self.original_img, self.rect.size)
        self.mask = pygame.mask.from_surface(self.img)

    def rotate_around_point(self, angle):
        #print(self.originaloffset)
        self.angle+=angle
        rotated_img = pygame.transform.rotate(self.scaled_img, self.angle)
        pivot_vec = pygame.Vector2(self.rotationcenter)

        new_center = pivot_vec - self.originaloffset.rotate(-angle)
        self.rect = rotated_img.get_rect(center=new_center)
        self.img = rotated_img
        if self.flipped:
            self.img = pygame.transform.flip(self.img, False, True)
        self.mask = pygame.mask.from_surface(self.img)
        self.originaloffset = self.originaloffset.rotate(-angle)

    def rescale(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self.mouseoffset = (- self.rect.center[0] + mouse_pos[0], - self.rect.center[1] + mouse_pos[1])
        offset = pygame.Vector2(self.mouseoffset)
        offset = offset.rotate(self.angle)
        self.rect.size = abs(offset[0])*2, abs(offset[1])*2
        self.scaled_img = pygame.transform.smoothscale(self.original_img, self.rect.size)
        self.img = pygame.transform.rotate(self.scaled_img, self.angle)
        if self.flipped:
            self.img = pygame.transform.flip(self.img, False, True)
        self.mask = pygame.mask.from_surface(self.img)

        self.rotate_around_point(0)

    def scale_to_size(self, size):
        self.rect.size = abs(size[0]), abs(size[1])
        self.scaled_img = pygame.transform.smoothscale(self.original_img, self.rect.size)
        self.img = pygame.transform.rotate(self.scaled_img, self.angle)
        if self.flipped:
            self.img = pygame.transform.flip(self.img, False, True)
        self.mask = pygame.mask.from_surface(self.img)

        self.rotate_around_point(0)
    def reposition_option(self, option):
        self.reposition = option
        if option == REPOS_OBJECT:
            self.mouseoffset = (pygame.Vector2(self.rect.center) - pygame.Vector2(pygame.mouse.get_pos()))
    def flip_x_axis(self):
        self.flipped = True
        self.img = pygame.transform.flip(self.img, False, True)
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