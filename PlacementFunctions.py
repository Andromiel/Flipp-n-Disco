import pygame
import time

DONT_MOVE = 0
REPOS_OBJECT = 1
REPOS_ROTATION_CENTER = 2
RESCALE_OBJECT = 3

NO_TYPE = 0
BUMPER_TYPE = 1
FLIPPER_TYPE = 2
WALL_TYPE = 3
CANON_TYPE = 4
from Physics2D import PhysicsEngine, ConvexPolygon
from Ball import Ball
from math import pi


class MapObject:
    def __init__(self, img, imgname, posx=0, posy=0, size=(20, 20), show_rotating_point=False, angle=0, flipped=False,
                 rotate_offset=None):
        self.size = 1
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
        self.originaloffset = pygame.Vector2((0, 0))
        self.mask = pygame.mask.from_surface(self.img)
        self.rotationcenter = self.rect.center
        # if rotate_offset != None:
        #    self.originaloffset = pygame.Vector2(rotate_offset)
        if rotate_offset != None:
            self.originaloffset = pygame.Vector2(rotate_offset)
            self.rotationcenter = pygame.Vector2(self.rect.center) + pygame.Vector2(self.originaloffset)
        self.move_at((posx, posy))
        self.mouseoffset = (0, 0)
        self.angle = angle
        self.original_angle = angle
        self.rotating = False
        self.show_rotating_point = show_rotating_point

        self.flipped = False
        self.flip_x_axis(flipped)

        self.type = NO_TYPE

        self.liste_index = None

    def display(self, surface):
        surface.blit(self.img, self.rect)
        if self.show_rotating_point:
            pygame.draw.circle(surface, (255, 0, 0), self.rotationcenter, 3)
            pygame.draw.line(surface, (0, 255, 255), self.rect.center, self.rotationcenter)

    def move_at(self, pos):
        pos = pygame.Vector2(pos)
        offset = pygame.Vector2(self.rect.center)
        offset = self.rotationcenter - offset

        self.rect.center = pygame.Vector2(pos)
        self.rotationcenter = pos + offset

    def collidesmouse(self):
        mouse_pos = pygame.mouse.get_pos()
        pos_distance = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
        self.mouseoffset = (self.rect.center[0] - mouse_pos[0], self.rect.center[1] - mouse_pos[1])
        return self.rect.collidepoint(mouse_pos) and self.mask.get_at(pos_distance)

    def resize(self, size: float):
        self.size *= size
        center = self.rect.center
        self.rect.size = (
        self.rect.size[0] * size, self.rect.size[0] * size * self.original_rect.size[1] / self.original_rect.size[0])
        self.rect.center = center
        self.rotationcenter = self.rect.center + self.originaloffset * size
        self.img = pygame.transform.smoothscale(self.original_img, self.rect.size)
        if self.flipped:
            self.img = pygame.transform.flip(self.img, True, False)
        self.scaled_img = pygame.transform.smoothscale(self.original_img, self.rect.size)
        self.mask = pygame.mask.from_surface(self.img)

    def rotate_around_point(self, angle):
        if self.flipped == True:
            self.angle += angle
            rotated_img = pygame.transform.rotate((self.scaled_img), self.angle)
            pivot_vec = pygame.Vector2(self.rotationcenter)
            new_center = pivot_vec - self.originaloffset.rotate(angle)
            self.rect = rotated_img.get_rect(center=new_center)
            self.img = rotated_img
            if self.flipped:
                self.img = pygame.transform.flip(self.img, True, False)
            self.mask = pygame.mask.from_surface(self.img)
            self.originaloffset = self.originaloffset.rotate(angle)
        else:
            self.angle += angle
            rotated_img = pygame.transform.rotate(self.scaled_img, self.angle)
            pivot_vec = pygame.Vector2(self.rotationcenter)

            new_center = pivot_vec - self.originaloffset.rotate(-angle)
            self.rect = rotated_img.get_rect(center=new_center)
            self.img = rotated_img
            self.mask = pygame.mask.from_surface(self.img)
            self.originaloffset = self.originaloffset.rotate(-angle)

    def rescale(self, surface, type=None):
        mouse_pos = pygame.mouse.get_pos()
        self.mouseoffset = (- self.rect.center[0] + mouse_pos[0], - self.rect.center[1] + mouse_pos[1])
        offset = pygame.Vector2(self.mouseoffset)
        offset = offset.rotate(self.angle)
        self.rect.size = abs(offset[0]) * 2, abs(offset[1]) * 2
        if type == BUMPER_TYPE or type == FLIPPER_TYPE:
            self.rect.size = abs(offset[0]), abs(offset[0] * self.original_rect.height / self.original_rect.width)
        self.scaled_img = pygame.transform.smoothscale(self.original_img, self.rect.size)
        if self.flipped:
            # print("hello")
            self.img = pygame.transform.rotate(self.scaled_img, -self.angle)
            self.img = pygame.transform.flip(self.img, True, False)
        else:
            self.img = pygame.transform.rotate(self.scaled_img, self.angle)
        self.mask = pygame.mask.from_surface(self.img)

        self.rotate_around_point(0)

    def scale_to_size(self, size):
        self.rect.size = abs(size[0]), abs(size[1])
        self.scaled_img = pygame.transform.smoothscale(self.original_img, self.rect.size)
        self.img = pygame.transform.rotate(self.scaled_img, self.angle)
        if self.flipped:
            self.img = pygame.transform.flip(self.img, True, False)
        self.mask = pygame.mask.from_surface(self.img)

        self.rotate_around_point(0)

    def reposition_option(self, option):
        self.reposition = option
        if option == REPOS_OBJECT:
            self.mouseoffset = (pygame.Vector2(self.rect.center) - pygame.Vector2(pygame.mouse.get_pos()))

    def flip_x_axis(self, flip=None):
        if flip == None:
            self.flipped = not self.flipped
            self.img = pygame.transform.flip(self.img, True, False)
            self.mask = pygame.mask.from_surface(self.img)
            center = self.rect.center
            self.rect = self.img.get_rect()
            self.rect.center = center
        else:
            if flip == self.flipped:
                pass
            else:
                self.flip_x_axis()
                # self.flipped = flip

    def update(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        if self.reposition == REPOS_OBJECT:
            self.move_at(mouse_pos + pygame.Vector2(self.mouseoffset))
        elif self.reposition == REPOS_ROTATION_CENTER:
            self.rotationcenter = mouse_pos
            self.originaloffset = pygame.Vector2(self.rotationcenter) - pygame.Vector2(self.rect.center)
        elif self.reposition == RESCALE_OBJECT:
            self.rescale(surface, self.shadow_type)
        self.display(surface)


class GameComponent(MapObject):
    def __init__(self, img=None, imgname=None, posx=0, posy=0, angle=None, object_type=NO_TYPE, size=(20, 20),
                 flipped=False, rotation_offset=None):
        MapObject.__init__(self, img, imgname, posx, posy, show_rotating_point=True, size=size, flipped=flipped,
                           rotate_offset=rotation_offset)
        self.physics_engineID = [-1, -1]  # type, index
        self.component_type = object_type
        self.shadow_type = object_type

    def connect_with_physics_engine(self, engine: PhysicsEngine):
        if self.component_type == BUMPER_TYPE:
            engine.balls.append(Ball(self.rect.center[0], self.rect.center[1], self.rect.height / 2.0, 1.0, True))
            self.physics_engineID = [0, len(engine.balls) - 1]
        elif self.component_type == FLIPPER_TYPE:
            points = [(-0.9, 0), (0.8, 1.0 / 3), (0.8, -1.0 / 8), (-0.5, 0.6), (-0.5, -0.6)]
            points = [
                (pygame.Vector2(points[i]).elementwise() * pygame.Vector2(self.scaled_img.get_size()) / 2.0).rotate(
                    -self.angle) + pygame.Vector2(self.rect.center) for i in range(len(points))]
            if self.flipped:
                for i in range(len(points)):
                    points[i] = pygame.Vector2((-points[i][0], points[i][1]))

            engine.convex_polygons.append(ConvexPolygon(*points, fixed=True, fixed_rotation=True, mass_per_area=100))
            engine.convex_polygons[-1].Translate((self.rect.center[0], self.rect.center[1]))
            self.physics_engineID = [1, len(engine.convex_polygons) - 1]
        elif self.component_type == WALL_TYPE:
            points = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]
            points = [
                (pygame.Vector2(points[i]).elementwise() * pygame.Vector2(self.scaled_img.get_size()) / 2.0).rotate(
                    -self.angle) + pygame.Vector2(self.rect.center) for i in range(len(points))]
            if self.flipped:
                for i in range(len(points)):
                    points[i] = pygame.Vector2((-points[i][0], points[i][1]))
            engine.convex_polygons.append(ConvexPolygon(*points, fixed=True, fixed_rotation=True))
            engine.convex_polygons[-1].Translate((self.rect.center[0], self.rect.center[1]))
            self.physics_engineID = [1, len(engine.convex_polygons) - 1]

    def adjust_to_physics(self, engine: PhysicsEngine):
        if self.physics_engineID[0] == 0:
            ball = engine.balls[self.physics_engineID[1]]
            if ball.fixed_in_space != True:
                self.rect.center = ball.position
        if self.physics_engineID[0] == 1:
            polygon = engine.convex_polygons[self.physics_engineID[1]]
            self.rect.center = polygon.center_of_mass
            if self.component_type == FLIPPER_TYPE:
                if self.flipped:
                    self.rotate_around_point(-self.angle + self.original_angle + polygon.rotation * 180 / pi)
                else:
                    self.rotate_around_point(-self.angle + self.original_angle - polygon.rotation * 180 / pi)


'''
Guide de la classe MapObject:
- Reposition = 1 : Change la position de l'objet par rapport à la souris
- Reposition = 2 : change la position du centre de rotation de l'objet par rapport à la souris
'''
