import copy

import pygame.key

from PlacementFunctions import *

import os

from LevelLoader import *

BALL = 0
POLYGON = 1

WIDTH = 600
HEIGHT = 750

QUIT = -1
MENU = 0
LEVEL_EDITOR = 1
PLAY = 2
MY_LEVELS = 3

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

button_name = "textures/plus sign.png"
flipper_name = "textures/flipper.png"
bumper_name = "textures/bumper1.png"
wall_name = "textures/wall.png"

button_tex = pygame.image.load(button_name)
flipper_tex = pygame.image.load(flipper_name)
bumper_tex = pygame.image.load(bumper_name)
wall_tex = pygame.image.load(wall_name)


level_map_name = "textures/LEVEL MAP.png"
level_map_tex = pygame.image.load(level_map_name)
menu_name = "textures/Menu.png"
menu_tex = pygame.image.load(menu_name)
play_button_name = "textures/play button.png"
play_button_tex = pygame.image.load(play_button_name)
level_editor_button_name = "textures/level_editor button.png"
level_editor_button_tex = pygame.image.load(level_editor_button_name)
my_levels_button_name = "textures/my_levels button.png"
my_levels_button_tex = pygame.image.load(my_levels_button_name)

directory = "textures/levels_numbers"
levels_numbers_names = os.listdir(directory)
levels_numbers_tex = [pygame.image.load("textures/levels_numbers/" + name) for name in levels_numbers_names]
class GameComponent(MapObject):
    def __init__(self, img = None, imgname = None, posx=0, posy=0, rotationcenter=None, angle=None):
        MapObject.__init__(self, img, imgname, posx, posy, show_rotating_point=True)
        self.physics_engineID = [-1, -1]#type, index
class Game:
    def __init__(self, screen):
        self.GameComponents = []
        self.screen = screen
        self.GameState = 1




    def ShowComponents(self):
        for i in range(len(self.GameComponents)):
            if self.GameComponents[i].img != None:
                self.GameComponents[i].update(self.screen)

transparent_background = pygame.Surface((WIDTH, HEIGHT))
transparent_background.set_alpha(0)

game = Game(screen)
game.GameState = LEVEL_EDITOR

loop = True
clock = pygame.time.Clock()

escape = False
while loop:
    BACKGROUND_COLOR = (30, 90, 120)
    #screen.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = False
    if game.GameState == QUIT:
        loop = False
        break
    if game.GameState == MENU:
        level_map = MapObject(level_map_tex, level_map_name, WIDTH/2, HEIGHT/2, screen.get_size(), False)
        menu = MapObject(menu_tex, menu_name, WIDTH/2, HEIGHT/2, screen.get_size(), False)
        play_button = MapObject(play_button_tex, play_button_name, WIDTH/2, HEIGHT/2, (200, 200*play_button_tex.get_height()/play_button_tex.get_width()), False)
        level_editor_button = MapObject(level_editor_button_tex, level_editor_button_name, WIDTH/2, HEIGHT/2+60, (200, 200*level_editor_button_tex.get_height()/level_editor_button_tex.get_width()), False)
        my_levels_button = MapObject(my_levels_button_tex, my_levels_button_name, WIDTH/2, HEIGHT/2+120, (200, 200*my_levels_button_tex.get_height()/my_levels_button_tex.get_width()), False)

        play_button.resize(0.3)
        play_button.move_at((WIDTH/2, HEIGHT/2))
        level_editor_button.resize(0.3)
        level_editor_button.move_at((WIDTH / 2, HEIGHT / 2+60))
        my_levels_button.resize(0.3)
        my_levels_button.move_at((WIDTH/2, HEIGHT/2 + 120))

        transparent_background.set_alpha(0)

        for i in range(0, 255, 2):
            clock.tick(60)
            screen.blit(transparent_background, (0,0))
            transparent_background.set_alpha(i)
            pygame.display.update()
        for i in range(255, 0, -2):
            clock.tick(60)
            menu.update(screen)
            screen.blit(transparent_background, (0,0))
            transparent_background.set_alpha(i)
            pygame.display.update()

        while game.GameState==MENU:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    game.GameState = QUIT
                    loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        escape = not escape
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if level_editor_button.collidesmouse():
                        game.GameState = LEVEL_EDITOR
                    if play_button.collidesmouse():
                        game.GameState = PLAY
                    if my_levels_button.collidesmouse():
                        game.GameState = MY_LEVELS
            clock.tick(60)

            if play_button.collidesmouse():
                if play_button.rect.size[0]/play_button.original_size[0] < 1.05 and play_button.rect.size[1]/play_button.original_size[1] < 1.05:
                    play_button.resize(1.02)
                    play_button.move_at((WIDTH/2, HEIGHT/2))
            else:
                if play_button.rect.size[0] / play_button.original_size[0] > 0.95 and play_button.rect.size[1] / play_button.original_size[1] > 0.95:
                    play_button.resize(0.98)
                    play_button.move_at((WIDTH / 2, HEIGHT / 2))

            if level_editor_button.collidesmouse():
                if level_editor_button.rect.size[0]/level_editor_button.original_size[0] < 1.05 and level_editor_button.rect.size[1]/level_editor_button.original_size[1] < 1.05:
                    level_editor_button.resize(1.02)
                    level_editor_button.move_at((WIDTH/2, HEIGHT/2+60))
            else:
                if level_editor_button.rect.size[0] / level_editor_button.original_size[0] > 0.95 and level_editor_button.rect.size[1] / level_editor_button.original_size[1] > 0.95:
                    level_editor_button.resize(0.98)
                    level_editor_button.move_at((WIDTH / 2, HEIGHT / 2+60))

            if my_levels_button.collidesmouse():
                if my_levels_button.rect.size[0]/my_levels_button.original_size[0] < 1.05 and my_levels_button.rect.size[1]/my_levels_button.original_size[1] < 1.05:
                    my_levels_button.resize(1.02)
                    my_levels_button.move_at((WIDTH/2, HEIGHT/2+120))
            else:
                if my_levels_button.rect.size[0] / my_levels_button.original_size[0] > 0.95 and my_levels_button.rect.size[1] / my_levels_button.original_size[1] > 0.95:
                    my_levels_button.resize(0.98)
                    my_levels_button.move_at((WIDTH / 2, HEIGHT / 2+120))
            menu.update(screen)
            play_button.update(screen)
            level_editor_button.update(screen)
            my_levels_button.update(screen)
            pygame.display.update()

    if game.GameState == LEVEL_EDITOR:
        previous_background = screen


        add_button = MapObject(pygame.transform.smoothscale(button_tex, (60,60)), button_name, WIDTH-60,HEIGHT-60)
        flipper_choose = MapObject(pygame.transform.smoothscale(flipper_tex, (100,100*(flipper_tex.get_height()/flipper_tex.get_width()))), flipper_name, 0,0)
        flipper_choose.move_at((WIDTH/2, HEIGHT/2))
        bumper_choose = MapObject(pygame.transform.smoothscale(bumper_tex, (60,60)), bumper_name, 0)
        bumper_choose.move_at((WIDTH / 2 + 150, HEIGHT / 2))
        wall_choose = MapObject(pygame.transform.smoothscale(wall_tex, (60,60 * (wall_tex.get_height()/wall_tex.get_width()))), wall_name, WIDTH/2 - 150,HEIGHT/2)
        wall_choose.move_at((WIDTH / 2 - 150, HEIGHT / 2))


        transparent_background.set_alpha(128)
        transparent_background.fill((0, 0, 0))

        SHOW_EVERYTHING = 0
        CHOOSE_OBJECT = 1
        editing_sate = SHOW_EVERYTHING


        selected_object = None, None

        selected_objects = []
        copied_objects = []

        modify_option = REPOS_OBJECT

        for i in range(0, 255, 2):
            clock.tick(60)
            screen.blit(transparent_background, (0,0))
            transparent_background.set_alpha(i)
            pygame.display.update()
        for i in range(255, 0, -2):
            clock.tick(60)
            screen.fill(BACKGROUND_COLOR)
            screen.blit(transparent_background, (0,0))
            transparent_background.set_alpha(i)
            pygame.display.update()

        transparent_background.set_alpha(128)
        while game.GameState==LEVEL_EDITOR:

            FLIPPER = 0
            BUMPER = 1
            WALL = 2

            clock.tick(60)

            screen.fill(BACKGROUND_COLOR)

            game.ShowComponents()

            events = pygame.event.get()

            if editing_sate == CHOOSE_OBJECT:

                for i in range(len(events)):
                    event = events[i]
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            editing_sate = SHOW_EVERYTHING
                            events.pop(i)
                            break

                chose_object = -1


                screen.blit(previous_background, (0, 0))
                screen.blit(transparent_background, (0, 0))
                bumper_choose.update(screen)
                wall_choose.update(screen)
                flipper_choose.update(screen)

                if bumper_choose.collidesmouse():
                    if pygame.mouse.get_pressed()[0]:
                        pygame.draw.rect(screen, (255, 0, 0), bumper_choose.rect, 3)
                        chose_object = BUMPER
                    else:
                        pygame.draw.rect(screen, (0, 255, 0), bumper_choose.rect, 3)
                if flipper_choose.collidesmouse():
                    if pygame.mouse.get_pressed()[0]:
                        pygame.draw.rect(screen, (255, 0, 0), flipper_choose.rect, 3)
                        chose_object = FLIPPER
                    else:
                        pygame.draw.rect(screen, (0, 255, 0), flipper_choose.rect, 3)
                if wall_choose.collidesmouse():
                    if pygame.mouse.get_pressed()[0]:
                        pygame.draw.rect(screen, (255, 0, 0), wall_choose.rect, 3)
                        chose_object = WALL
                    else:
                        pygame.draw.rect(screen, (0, 255, 0), wall_choose.rect, 3)
                if chose_object!=-1:
                    editing_sate = SHOW_EVERYTHING
                    if chose_object == BUMPER:
                        game.GameComponents.append(GameComponent(pygame.transform.smoothscale(bumper_tex, (bumper_tex.get_size())), bumper_name, WIDTH/2, HEIGHT/2))
                        center = game.GameComponents[-1].rect.center
                        game.GameComponents[-1].resize(60/game.GameComponents[-1].rect.size[0])
                        game.GameComponents[-1].move_at(center)
                    if chose_object == FLIPPER:
                        game.GameComponents.append(GameComponent(pygame.transform.smoothscale(flipper_tex, (flipper_tex.get_size())), flipper_name, WIDTH/2, HEIGHT/2))
                        center = game.GameComponents[-1].rect.center
                        game.GameComponents[-1].resize(60 / game.GameComponents[-1].rect.size[0])
                        game.GameComponents[-1].move_at(center)
                    if chose_object == WALL:
                        game.GameComponents.append(GameComponent(pygame.transform.smoothscale(wall_tex, (wall_tex.get_size())), wall_name, WIDTH/2, HEIGHT/2))
                        center = game.GameComponents[-1].rect.center
                        game.GameComponents[-1].resize(60 / game.GameComponents[-1].rect.size[0])
                        game.GameComponents[-1].move_at(center)

            if editing_sate == SHOW_EVERYTHING:
                add_button.update(screen)
                collided = False
                shifting = False
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    shifting = True
                if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_c]:
                    copied_elements = selected_objects[:]
                    print("copied")
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            SaveContent(game.GameComponents, "LevelData.txt")
                        elif event.key == pygame.K_l:
                            game.GameComponents = ReadContent("LevelData.txt")

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_v:
                            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                                for i in range(len(copied_elements)):
                                    print("pasted")
                                    obj = copied_elements[i][0]
                                    game.GameComponents.append(GameComponent(obj.original_img, obj.imgname, obj.rect.center[0], obj.rect.center[1]))
                                    game.GameComponents[-1].rect.size = obj.original_rect.size
                                    game.GameComponents[-1].scale_to_size(obj.scaled_img.get_rect().size)
                                    game.GameComponents[-1].rotate_around_point(obj.angle)
                                    game.GameComponents[-1].originaloffset = obj.originaloffset
                                    game.GameComponents[-1].rotationcenter = obj.rotationcenter
                                    print("tried")

                    if event.type == pygame.MOUSEBUTTONDOWN and add_button.collidesmouse():
                        editing_sate = CHOOSE_OBJECT
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if modify_option == REPOS_OBJECT:
                            modify_option = RESCALE_OBJECT
                        else:
                            modify_option = REPOS_OBJECT
                    for i in range(len(game.GameComponents)-1, -1, -1):
                        component = game.GameComponents[i]
                        if event.type == pygame.MOUSEBUTTONDOWN and component.collidesmouse():
                            collided = True
                            selected_object = component, i
                            if shifting:
                                result = list((i == j for object, j in selected_objects))
                                if not any(result):
                                    selected_objects.append((component, i))
                                else:
                                    selected_objects.pop(result.index(True))
                                    if len(selected_objects) == 1:
                                        selected_object = selected_objects[0][0], selected_objects[0][1]
                            else:
                                result = list((i == j for object, j in selected_objects))
                                if not any(result):
                                    selected_objects.clear()
                                    selected_objects.append((component, i))

                            if event.button == pygame.BUTTON_LEFT:
                                result = list((i == j for object, j in selected_objects))
                                if any(result):
                                    for j in range(len(selected_objects)):
                                        object, index = selected_objects[j]
                                        object.reposition_option(modify_option)
                                else:
                                    component.reposition_option(modify_option)

                            elif event.button == pygame.BUTTON_RIGHT:
                                component.reposition_option(REPOS_ROTATION_CENTER)
                            break
                        elif event.type == pygame.MOUSEBUTTONUP:
                            component.reposition_option(DONT_MOVE)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and not collided:
                        selected_object = None, None
                        selected_objects.clear()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            for i in range(len(selected_objects)):
                                selected_objects[i][0].flip_x_axis()

                if selected_object[0] != None and len(selected_objects)==1:
                    object, index = selected_object
                    pygame.draw.rect(screen, (0, 255, 0), object.rect, 3)
                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                object.rotate_around_point(10)
                            if event.key == pygame.K_DOWN:
                                object.rotate_around_point(-10)
                            if event.key == pygame.K_DELETE:
                                game.GameComponents.pop(index)
                                selected_object = None, None
                elif len(selected_objects)>1:
                    for i in range(len(selected_objects)):
                        object, index = selected_objects[i]
                        pygame.draw.rect(screen, (0, 255, 0), object.rect, 3)
                        for event in events:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_UP:
                                    object.rotate_around_point(10)
                                if event.key == pygame.K_DOWN:
                                    object.rotate_around_point(-10)
                                if event.key == pygame.K_DELETE:
                                    game.GameComponents.pop(index)
                                    selected_objects.pop(i)
                                    i=i-1
                                    selected_object = None, None
            for event in events:
                if event.type == pygame.QUIT:
                    game.GameState = QUIT
                    loop = False
                if event.type == pygame.MOUSEBUTTONDOWN and add_button.collidesmouse():
                    editing_sate = CHOOSE_OBJECT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.GameState = MENU
            pygame.display.update()
        game.GameState = MENU
        escape = False



    if game.GameState == PLAY:
        level_map = MapObject(level_map_tex, level_map_name, WIDTH/2, HEIGHT/2, (screen.get_size()))

        n_levels = 5
        levels_numbers = []

        for i in range(n_levels):
            levels_numbers.append(MapObject(levels_numbers_tex[i], levels_numbers_names[i], (WIDTH/4)*(i%3) + (WIDTH)/4, (HEIGHT/4)*int(i/3) + HEIGHT/4))
            levels_numbers[i].resize(0.7)
        shadows = [pygame.Surface(pygame.Vector2(levels_numbers[0].rect.size)*2, pygame.SRCALPHA) for i in range(n_levels)]
        for i in range(len(shadows)):
            n = int(levels_numbers[0].rect.size[0])
            for j in range(n, -1, -1):
                c = (n-j)/n*700
                if c>255:
                    c=255
                pygame.draw.circle(shadows[i], (0, 0, 0, c), (shadows[i].get_width()/2, shadows[i].get_height()/2), j)
        for i in range(len(shadows)):
            shadows[i] = MapObject(shadows[i], "", (WIDTH/4)*(i%3) + (WIDTH)/4, (HEIGHT/4)*int(i/3) + HEIGHT/4)
            shadows[i].resize(0.7*0.8)
        for i in range(0, 255, 2):
            clock.tick(60)
            screen.blit(transparent_background, (0,0))
            transparent_background.set_alpha(i)
            pygame.display.update()
        for i in range(255, 0, -2):
            clock.tick(60)
            level_map.update(screen)
            screen.blit(transparent_background, (0,0))
            transparent_background.set_alpha(i)
            pygame.display.update()
        while game.GameState == PLAY:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    loop = False
                    game.GameState = QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.GameState = MENU

            for i in range(n_levels):
                if levels_numbers[i].collidesmouse():
                    if(levels_numbers[i].rect.size[0]/levels_numbers[i].original_rect.size[0] < 0.8):
                        levels_numbers[i].resize(1.03)
                        shadows[i].resize(1.05)
                else:
                    if (levels_numbers[i].rect.size[0] / levels_numbers[i].original_rect.size[0] > 0.7):
                        levels_numbers[i].resize(0.97)
                        shadows[i].resize(0.95)
            for i in range(n_levels):
                if levels_numbers[i].collidesmouse():
                    if(shadows[i].rect.size[0]/shadows[i].original_rect.size[0] < 0.7*0.9):
                        shadows[i].resize(1.03)
                else:
                    if (shadows[i].rect.size[0] / shadows[i].original_rect.size[0] > 0.7*0.6):
                        shadows[i].resize(0.97)

            level_map.update(screen)
            for i in range(len(shadows)):
                shadow = shadows[i]
                shadow.update(screen)
            for i in range(n_levels):
                levels_numbers[i].update(screen)

            pygame.display.update()

    if game.GameState == MY_LEVELS:
        pass
    pygame.display.update()





