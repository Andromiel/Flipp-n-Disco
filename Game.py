import copy

import pygame.key

from PlacementFunctions import *

from MenuScroller import *

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
RUN_LEVEL = 4
LOST = 5

menu_music = "Sounds/music_level1_MJ.mp3"
editor_music = "Sounds/music_level_editor_creep.mp3"
level_music = "Sounds/music_level3_CD.mp3"

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

button_name = "textures/plus sign.png"
save_button_name = "textures/savebutton.png"
load_button_name = "textures/loadbutton.png"
help_button_name = "textures/helpbutton.png"
custom_levels_play_button_name = "textures/custom_levels_play_button.png"
custom_levels_edit_button_name = "textures/custom_levels_edit_button.png"

ball_name = "textures/ball.png"
flipper_name = "textures/flipper.png"
bumper_name = "textures/bumper1.png"
wall_name = "textures/wall.png"
canon_name = "textures/canon.png"

instructions_tex = pygame.image.load("textures/instructions.png")
instructions_tex = pygame.transform.smoothscale(instructions_tex, (
    WIDTH, WIDTH * instructions_tex.get_height() / instructions_tex.get_width()))
ball_tex = pygame.transform.smoothscale(pygame.image.load(ball_name), (50,50))
button_tex = pygame.image.load(button_name)
flipper_tex = pygame.image.load(flipper_name)
bumper_tex = pygame.image.load(bumper_name)
wall_tex = pygame.image.load(wall_name)
canon_tex = pygame.image.load(canon_name)

save_button_tex = pygame.image.load(save_button_name)
load_button_tex = pygame.image.load(load_button_name)
help_button_tex = pygame.image.load(help_button_name)
custom_levels_play_button_tex = pygame.image.load(custom_levels_play_button_name)
custom_levels_edit_button_tex = pygame.image.load(custom_levels_edit_button_name)

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
custom_levels = os.listdir("custom_levels")
custom_levels = [custom_levels[i][:-4] for i in range(len(custom_levels))]
game_levels = os.listdir("game_levels")
#game_levels = [game_levels[i] for i in range(len(game_levels))]
current_level = game_levels[0] if len(game_levels)>0 else None

from PlacementFunctions import GameComponent
from PlacementFunctions import PhysicsEngine

engine = PhysicsEngine()


class Game:
    def __init__(self, screen):
        self.GameComponents = []
        self.screen = screen
        self.GameState = MENU
        self.lives = 3

    def ShowComponents(self):
        for i in range(len(self.GameComponents)):
            if self.GameComponents[i].img != None:
                self.GameComponents[i].update(self.screen)

    def DisplayLives(self):
        for i in range(self.lives):
            screen.blit(ball_tex, (10+60*i, 10))

    def CheckState(self):
        if self.lives == 0:
            game.GameState = LOST

transparent_background = pygame.Surface((WIDTH, HEIGHT))
transparent_background.set_alpha(0)

game = Game(screen)
game.GameState = MENU
game.GameComponents = ReadContent("custom_levels/level1.txt")

loop = True
clock = pygame.time.Clock()

escape = False
while loop:
    BACKGROUND_COLOR = (30, 90, 120)
    # screen.fill(BACKGROUND_COLOR)
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

        #pygame.mixer.music.load(menu_music)
        #pygame.mixer.music.set_volume(0.1)
        #pygame.mixer.music.play()

        level_map = MapObject(level_map_tex, level_map_name, WIDTH / 2, HEIGHT / 2, screen.get_size(), False)
        menu = MapObject(menu_tex, menu_name, WIDTH / 2, HEIGHT / 2, screen.get_size(), False)
        play_button = MapObject(play_button_tex, play_button_name, WIDTH / 2, HEIGHT / 2,
                                (200, 200 * play_button_tex.get_height() / play_button_tex.get_width()), False)
        level_editor_button = MapObject(level_editor_button_tex, level_editor_button_name, WIDTH / 2, HEIGHT / 2 + 60, (
            200, 200 * level_editor_button_tex.get_height() / level_editor_button_tex.get_width()), False)
        my_levels_button = MapObject(my_levels_button_tex, my_levels_button_name, WIDTH / 2, HEIGHT / 2 + 120,
                                     (200, 200 * my_levels_button_tex.get_height() / my_levels_button_tex.get_width()),
                                     False)

        play_button.resize(0.3)
        play_button.move_at((WIDTH / 2, HEIGHT / 2))
        level_editor_button.resize(0.3)
        level_editor_button.move_at((WIDTH / 2, HEIGHT / 2 + 60))
        my_levels_button.resize(0.3)
        my_levels_button.move_at((WIDTH / 2, HEIGHT / 2 + 120))

        transparent_background.set_alpha(0)

        for i in range(0, 255, 2):
            clock.tick(60)
            screen.blit(transparent_background, (0, 0))
            transparent_background.set_alpha(i)
            pygame.display.update()
        for i in range(255, 0, -2):
            clock.tick(60)
            menu.update(screen)
            screen.blit(transparent_background, (0, 0))
            transparent_background.set_alpha(i)
            pygame.display.update()

        while game.GameState == MENU:
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
                if play_button.rect.size[0] / play_button.original_size[0] < 1.05 and play_button.rect.size[1] / \
                        play_button.original_size[1] < 1.05:
                    play_button.resize(1.02)
                    play_button.move_at((WIDTH / 2, HEIGHT / 2))
            else:
                if play_button.rect.size[0] / play_button.original_size[0] > 0.95 and play_button.rect.size[1] / \
                        play_button.original_size[1] > 0.95:
                    play_button.resize(0.98)
                    play_button.move_at((WIDTH / 2, HEIGHT / 2))

            if level_editor_button.collidesmouse():
                if level_editor_button.rect.size[0] / level_editor_button.original_size[0] < 1.05 and \
                        level_editor_button.rect.size[1] / level_editor_button.original_size[1] < 1.05:
                    level_editor_button.resize(1.02)
                    level_editor_button.move_at((WIDTH / 2, HEIGHT / 2 + 60))
            else:
                if level_editor_button.rect.size[0] / level_editor_button.original_size[0] > 0.95 and \
                        level_editor_button.rect.size[1] / level_editor_button.original_size[1] > 0.95:
                    level_editor_button.resize(0.98)
                    level_editor_button.move_at((WIDTH / 2, HEIGHT / 2 + 60))

            if my_levels_button.collidesmouse():
                if my_levels_button.rect.size[0] / my_levels_button.original_size[0] < 1.05 and \
                        my_levels_button.rect.size[1] / my_levels_button.original_size[1] < 1.05:
                    my_levels_button.resize(1.02)
                    my_levels_button.move_at((WIDTH / 2, HEIGHT / 2 + 120))
            else:
                if my_levels_button.rect.size[0] / my_levels_button.original_size[0] > 0.95 and \
                        my_levels_button.rect.size[1] / my_levels_button.original_size[1] > 0.95:
                    my_levels_button.resize(0.98)
                    my_levels_button.move_at((WIDTH / 2, HEIGHT / 2 + 120))
            menu.update(screen)
            play_button.update(screen)
            level_editor_button.update(screen)
            my_levels_button.update(screen)
            pygame.display.update()

    if game.GameState == LEVEL_EDITOR:
        if current_level != None:
            game.GameComponents = ReadContent(current_level)

        #pygame.mixer.music.load(editor_music)
        #pygame.mixer.music.set_volume(0.1)
        #pygame.mixer.music.play()

        previous_background = screen

        add_button = MapObject(pygame.transform.smoothscale(button_tex, (60, 60)), button_name, WIDTH - 60, HEIGHT - 60)
        save_button = MapObject(pygame.transform.smoothscale(save_button_tex, (
            120, 120 * save_button_tex.get_height() / save_button_tex.get_width())), save_button_name, WIDTH - 70, 70)
        load_button = MapObject(pygame.transform.smoothscale(load_button_tex, (
            120, 120 * load_button_tex.get_height() / load_button_tex.get_width())), load_button_name, WIDTH - 70, 140)
        help_button = MapObject(pygame.transform.smoothscale(help_button_tex, (
            40, 40 * help_button_tex.get_height() / help_button_tex.get_width())), help_button_name, WIDTH - 70, 210)

        flipper_choose = MapObject(pygame.transform.smoothscale(flipper_tex, (
            100, 100 * (flipper_tex.get_height() / flipper_tex.get_width()))), flipper_name, WIDTH / 2, HEIGHT / 2)
        bumper_choose = MapObject(pygame.transform.smoothscale(bumper_tex, (60, 60)), bumper_name, WIDTH / 2 + 150,
                                  HEIGHT / 2)
        wall_choose = MapObject(
            pygame.transform.smoothscale(wall_tex, (60, 60 * (wall_tex.get_height() / wall_tex.get_width()))),
            wall_name, WIDTH / 2 - 150, HEIGHT / 2)
        canon_choose = MapObject(
            pygame.transform.smoothscale(canon_tex, (60, 60 * canon_tex.get_height() / canon_tex.get_width())),
            canon_name, WIDTH / 2, HEIGHT / 2 + 150)

        transparent_background.set_alpha(128)
        transparent_background.fill((0, 0, 0))

        SHOW_EVERYTHING = 0
        CHOOSE_OBJECT = 1
        INSTRUCTIONS = 2
        ENTER_LEVEL_NAME = 3
        editing_state = SHOW_EVERYTHING

        selected_object = None, None

        selected_objects = []
        copied_objects = []

        modify_option = REPOS_OBJECT

        for i in range(0, 255, 2):
            clock.tick(60)
            screen.blit(transparent_background, (0, 0))
            transparent_background.set_alpha(i)
            pygame.display.update()
        for i in range(255, 0, -2):
            clock.tick(60)
            screen.fill(BACKGROUND_COLOR)
            screen.blit(transparent_background, (0, 0))
            transparent_background.set_alpha(i)
            pygame.display.update()

        transparent_background.set_alpha(128)
        while game.GameState == LEVEL_EDITOR:

            FLIPPER = 0
            BUMPER = 1
            WALL = 2
            CANON = 3

            clock.tick(60)

            screen.fill(BACKGROUND_COLOR)

            game.ShowComponents()

            events = pygame.event.get()

            if editing_state == CHOOSE_OBJECT:

                for i in range(len(events)):
                    event = events[i]
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            editing_state = SHOW_EVERYTHING
                            events.pop(i)
                            break

                chose_object = -1

                screen.blit(previous_background, (0, 0))
                screen.blit(transparent_background, (0, 0))
                bumper_choose.update(screen)
                wall_choose.update(screen)
                flipper_choose.update(screen)
                canon_choose.update(screen)

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
                if canon_choose.collidesmouse():
                    if pygame.mouse.get_pressed()[0]:
                        pygame.draw.rect(screen, (255, 0, 0), canon_choose.rect, 3)
                        chose_object = CANON
                    else:
                        pygame.draw.rect(screen, (0, 255, 0), canon_choose.rect, 3)
                if chose_object != -1:
                    editing_state = SHOW_EVERYTHING
                    if chose_object == BUMPER:
                        game.GameComponents.append(
                            GameComponent(bumper_tex, bumper_name, WIDTH / 2, HEIGHT / 2, object_type=BUMPER_TYPE))
                        center = game.GameComponents[-1].rect.center
                        game.GameComponents[-1].resize(60 / game.GameComponents[-1].rect.size[0])
                        game.GameComponents[-1].move_at(center)
                    if chose_object == FLIPPER:
                        game.GameComponents.append(
                            GameComponent(flipper_tex, flipper_name, WIDTH / 2, HEIGHT / 2, object_type=FLIPPER_TYPE))
                        center = game.GameComponents[-1].rect.center
                        game.GameComponents[-1].resize(60 / game.GameComponents[-1].rect.size[0])
                        game.GameComponents[-1].move_at(center)
                    if chose_object == WALL:
                        game.GameComponents.append(
                            GameComponent(wall_tex, wall_name, WIDTH / 2, HEIGHT / 2, object_type=WALL_TYPE))
                        center = game.GameComponents[-1].rect.center
                        game.GameComponents[-1].resize(60 / game.GameComponents[-1].rect.size[0])
                        game.GameComponents[-1].move_at(center)
                    if chose_object == CANON:
                        game.GameComponents.append(
                            GameComponent(canon_tex, canon_name, WIDTH / 2, HEIGHT / 2, object_type=CANON_TYPE))
                        center = game.GameComponents[-1].rect.center
                        game.GameComponents[-1].resize(60 / game.GameComponents[-1].rect.size[0])
                        game.GameComponents[-1].move_at(center)
            if editing_state == SHOW_EVERYTHING:
                add_button.update(screen)
                load_button.update(screen)
                save_button.update(screen)
                help_button.update(screen)
                collided = False
                shifting = False
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    shifting = True
                if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_c]:
                    copied_elements = selected_objects[:]
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if add_button.collidesmouse():
                            editing_state = CHOOSE_OBJECT
                        if save_button.collidesmouse():
                            editing_state = ENTER_LEVEL_NAME
                        if load_button.collidesmouse():
                            game.GameComponents = ReadContent("custom_levels/LevelData.txt")
                            selected_objects.clear()
                            selected_object = None, None
                        if help_button.collidesmouse():
                            editing_state = INSTRUCTIONS

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_v:
                            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                                selected_objects.clear()
                                for i in range(len(copied_elements)):
                                    obj = copied_elements[i][0]
                                    game.GameComponents.append(
                                        GameComponent(obj.original_img, obj.imgname, obj.rect.center[0],
                                                      obj.rect.center[1], flipped=obj.flipped))
                                    game.GameComponents[-1].rect.size = obj.original_rect.size
                                    game.GameComponents[-1].scale_to_size(obj.scaled_img.get_rect().size)
                                    game.GameComponents[-1].rotate_around_point(obj.angle)
                                    game.GameComponents[-1].originaloffset = obj.originaloffset
                                    game.GameComponents[-1].rotationcenter = obj.rotationcenter
                                    game.GameComponents[-1].component_type = obj.component_type

                                    selected_objects.append((game.GameComponents[-1], len(game.GameComponents) - 1))
                                selected_object = selected_objects[0]

                        elif event.key == pygame.K_x:
                            if not selected_objects:
                                game.GameComponents = []

                        elif event.key == pygame.K_p:
                            game.GameState = RUN_LEVEL

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if modify_option == REPOS_OBJECT:
                            modify_option = RESCALE_OBJECT
                        else:
                            modify_option = REPOS_OBJECT
                    for i in range(len(game.GameComponents) - 1, -1, -1):
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

                if selected_object[0] != None and len(selected_objects) == 1:
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
                elif len(selected_objects) > 1:
                    for i in range(len(selected_objects)):
                        object, index = selected_objects[i]
                        pygame.draw.rect(screen, (0, 255, 0), object.rect, 3)
                        for event in events:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_UP:
                                    object.rotate_around_point(10)
                                if event.key == pygame.K_DOWN:
                                    object.rotate_around_point(-10)
                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_DELETE:
                                temp_components = []
                                selected_objects_indexes = [selected_objects[i][1] for i in
                                                            range(len(selected_objects))]
                                for i in range(len(game.GameComponents)):
                                    if selected_objects_indexes.count(i) == 0:
                                        temp_components.append(game.GameComponents[i])
                                game.GameComponents = temp_components
                                selected_object = None, None
                                selected_objects.clear()

            if editing_state == INSTRUCTIONS:
                screen.fill((112, 48, 160))
                screen.blit(instructions_tex, (0, 0))
                help_button.update(screen)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        editing_state = SHOW_EVERYTHING
            if editing_state == ENTER_LEVEL_NAME:
                font = pygame.font.Font(None, 32)
                input_active = False
                input_box = pygame.Rect(WIDTH / 2 - 105, HEIGHT / 2 - 32, 140, 32)
                color_inactive = pygame.Color('lightskyblue3')
                color_active = pygame.Color('dodgerblue2')
                text = ''
                enter_level_title = "Click the box to enter your level's name"
                done = False
                level_name = None
                while editing_state == ENTER_LEVEL_NAME:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            editing_state = QUIT
                            game.GameState = QUIT
                            break
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if input_box.collidepoint(event.pos):
                                input_active = not input_active
                            else:
                                input_active = False
                        color = color_active if input_active else color_inactive
                        if event.type == pygame.KEYDOWN:
                            if input_active:
                                if event.key == pygame.K_RETURN:
                                    level_name = text
                                    text = ''
                                    editing_state = SHOW_EVERYTHING
                                    break
                                elif event.key == pygame.K_BACKSPACE:
                                    text = text[:-1]
                                else:
                                    text += event.unicode
                    screen.fill((150, 100, 170))
                    if input_active:
                        if int(pygame.time.get_ticks()/500)%2 == 0:
                            txt_surface = font.render(text, True, color_inactive)
                        else:
                            txt_surface = font.render(text + '|', True, color_inactive)
                    else:
                        txt_surface = font.render(text, True, color_inactive)

                    title_surface = font.render(enter_level_title, True, color_inactive)
                    input_box.w = max(200, txt_surface.get_width() + 10)
                    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                    screen.blit(title_surface, (WIDTH/2 - title_surface.get_width()/2, input_box.y - 50))
                    pygame.draw.rect(screen, color_inactive, input_box, 2)
                    pygame.display.update()
                if level_name is not None:
                    SaveContent(game.GameComponents, "custom_levels/" + level_name + ".txt")
                    if level_name not in custom_levels:
                        custom_levels.append(level_name)
            for event in events:
                if event.type == pygame.QUIT:
                    game.GameState = QUIT
                    loop = False
                if event.type == pygame.MOUSEBUTTONDOWN and add_button.collidesmouse():
                    editing_state = CHOOSE_OBJECT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.GameState = MENU
            pygame.display.update()
        game.GameState = MENU
        escape = False

    if game.GameState == PLAY:

        level_map = MapObject(level_map_tex, level_map_name, WIDTH / 2, HEIGHT / 2, (screen.get_size()))

        n_levels = len(game_levels)
        levels_numbers = []

        for i in range(n_levels):
            levels_numbers.append(
                MapObject(levels_numbers_tex[i], levels_numbers_names[i], (WIDTH / 4) * (i % 3) + (WIDTH) / 4,
                          (HEIGHT / 4) * int(i / 3) + HEIGHT / 4))
            levels_numbers[i].resize(0.7)
        shadows = [pygame.Surface(pygame.Vector2(levels_numbers[0].rect.size) * 2, pygame.SRCALPHA) for i in
                   range(n_levels)]
        for i in range(len(shadows)):
            n = int(levels_numbers[0].rect.size[0])
            for j in range(n, -1, -1):
                c = (n - j) / n * 700
                if c > 255:
                    c = 255
                pygame.draw.circle(shadows[i], (0, 0, 0, c), (shadows[i].get_width() / 2, shadows[i].get_height() / 2),
                                   j)
        for i in range(len(shadows)):
            shadows[i] = MapObject(shadows[i], "", (WIDTH / 4) * (i % 3) + (WIDTH) / 4,
                                   (HEIGHT / 4) * int(i / 3) + HEIGHT / 4)
            shadows[i].resize(0.7 * 0.8)
        for i in range(0, 255, 2):
            clock.tick(60)
            screen.blit(transparent_background, (0, 0))
            transparent_background.set_alpha(i)
            pygame.display.update()
        for i in range(255, 0, -2):
            clock.tick(60)
            level_map.update(screen)
            screen.blit(transparent_background, (0, 0))
            transparent_background.set_alpha(i)
            pygame.display.update()
        while game.GameState == PLAY:
            events = pygame.event.get()
            clicked = False
            for event in events:
                if event.type == pygame.QUIT:
                    loop = False
                    game.GameState = QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.GameState = MENU
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        clicked = True
            pressed = pygame.key.get_pressed()

            for i in range(n_levels):
                if levels_numbers[i].collidesmouse():
                    if (levels_numbers[i].rect.size[0] / levels_numbers[i].original_rect.size[0] < 0.8):
                        levels_numbers[i].resize(1.03)
                        shadows[i].resize(1.05)
                    if clicked:
                        game.GameState = RUN_LEVEL
                        current_level = "game_levels/"+game_levels[i]
                else:
                    if (levels_numbers[i].rect.size[0] / levels_numbers[i].original_rect.size[0] > 0.7):
                        levels_numbers[i].resize(0.97)
                        shadows[i].resize(0.95)
            for i in range(n_levels):
                if levels_numbers[i].collidesmouse():
                    if (shadows[i].rect.size[0] / shadows[i].original_rect.size[0] < 0.7 * 0.9):
                        shadows[i].resize(1.03)
                else:
                    if (shadows[i].rect.size[0] / shadows[i].original_rect.size[0] > 0.7 * 0.6):
                        shadows[i].resize(0.97)

            level_map.update(screen)
            for i in range(len(shadows)):
                shadow = shadows[i]
                shadow.update(screen)
            for i in range(n_levels):
                levels_numbers[i].update(screen)

            pygame.display.update()

    if game.GameState == RUN_LEVEL and current_level != None:
        game.lives = 3

        #pygame.mixer.music.load(level_music)
        #pygame.mixer.music.set_volume(0.1)
        #pygame.mixer.music.play()

        game.GameComponents = ReadContent(current_level)

        launched = False

        engine.clear()
        for component in game.GameComponents:
            component.connect_with_physics_engine(engine)
        ball_radius = 30
        added_ball = False
        #engine.balls.append(Ball(WIDTH / 2 - 100, HEIGHT / 2, ball_radius, 1.0, False))

        lost_screen = False

        lost_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        lost_font = pygame.font.Font( None, 100)
        lost_text = lost_font.render("YOU LOST", True, (255, 0, 0))
        lost_surface.blit(lost_text, (WIDTH/2-lost_text.get_width()/2, HEIGHT/2))

        canon_pos = (0, 0)
        while game.GameState == RUN_LEVEL:
            clock.tick(60)
            screen.fill((0, 120, 35))
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    loop = False
                    game.GameState = QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.GameState = MENU
                    if event.key == pygame.K_p:
                        for component in game.GameComponents:
                            if component.component_type == CANON_TYPE:
                                canon_pos = component.rect.center
                                added_ball = True
                                engine.balls.append(Ball(canon_pos[0], canon_pos[1], ball_radius, 1.0, False))
                                engine.balls[-1].velocity = (0, -500)
                                break
            engine.Update(screen, 1.0 / 60.0)
            game.ShowComponents()

            for component in game.GameComponents:
                component.adjust_to_physics(engine)
            for polygon in engine.convex_polygons:
                for point in polygon.points:
                    pygame.draw.circle(screen, (255, 0, 0), point, 3)

            # engine.convex_polygons[game.GameComponents[0].physics_engineID[1]].Rotate(-10 * 1/60, pygame.Vector2(game.GameComponents[0].rotationcenter))

            for component in game.GameComponents:
                if component.component_type == FLIPPER_TYPE:
                    angle = engine.convex_polygons[component.physics_engineID[1]].rotation
                    coeff = pi / 180
                    angle_in_degrees = angle / coeff
                    if pygame.key.get_pressed()[pygame.K_SPACE]:
                        if component.flipped == True:
                            engine.convex_polygons[component.physics_engineID[1]].Rotate(10 * 1 / 60, pygame.Vector2(
                                component.rotationcenter))
                        else:
                            engine.convex_polygons[component.physics_engineID[1]].Rotate(-10 * 1 / 60, pygame.Vector2(
                                component.rotationcenter))
                    else:
                        if component.flipped == True:
                            if angle > 0:
                                engine.convex_polygons[component.physics_engineID[1]].Rotate(-10 * 1 / 60,
                                                                                             pygame.Vector2(
                                                                                                 component.rotationcenter))

                        else:
                            if angle < 0:
                                engine.convex_polygons[component.physics_engineID[1]].Rotate(10 * 1 / 60,
                                                                                             pygame.Vector2(
                                                                                                 component.rotationcenter))

                    angle = engine.convex_polygons[component.physics_engineID[1]].rotation
                    coeff = pi / 180
                    angle_in_degrees = angle / coeff
                    if component.flipped == True:
                        if angle_in_degrees < 0:
                            engine.convex_polygons[component.physics_engineID[1]].Rotate(-angle, pygame.Vector2(
                                component.rotationcenter))
                        elif angle_in_degrees > 90:
                            engine.convex_polygons[component.physics_engineID[1]].Rotate(-angle + pi / 2,
                                                                                         pygame.Vector2(
                                                                                             component.rotationcenter))
                    else:
                        if angle_in_degrees > 0:
                            engine.convex_polygons[component.physics_engineID[1]].Rotate(-angle, pygame.Vector2(
                                component.rotationcenter))
                        elif angle_in_degrees < -90:
                            engine.convex_polygons[component.physics_engineID[1]].Rotate(-angle - pi / 2,
                                                                                         pygame.Vector2(
                                                                                             component.rotationcenter))

            if added_ball:
                if game.lives <= 0:
                    lost_screen = True
                if engine.balls[-1].position[1] - ball_radius > HEIGHT and game.lives>=1:
                    game.lives -=1
                    if game.lives>0:
                        engine.balls[-1].position = canon_pos
                        engine.balls[-1].velocity = (0, -500)

                if lost_screen:
                    screen.blit(lost_surface, (0, 0))

            # engine.convex_polygons[0].Rotate(0.1)
            for ball in engine.balls:
                pygame.draw.circle(screen, (255, 0, 0), ball.position, ball.radius, width=3)

            if engine.balls and added_ball:
                engine.balls[-1].Display(screen)
            game.DisplayLives()
            pygame.display.update()

    if game.GameState == MY_LEVELS:
        menu_data = GenerateMenu(custom_levels, screen)
        menu_rect, scrollerbar_rect, scroller_rect, text_surfaces, text_rects, font = menu_data
        selected_level = [False, None]

        custom_levels_play_button = MapObject(custom_levels_play_button_tex, custom_levels_play_button_name, 50, 150,
                                              (200, 200 * custom_levels_play_button_tex.get_height() / custom_levels_play_button_tex.get_width()))
        custom_levels_play_button.scale_to_size(((100, 100 * custom_levels_play_button_tex.get_height() / custom_levels_play_button_tex.get_width())))
        custom_levels_edit_button = MapObject(custom_levels_edit_button_tex, custom_levels_edit_button_name, 50, 200,
                                              (200, 200 * custom_levels_edit_button_tex.get_height() / custom_levels_edit_button_tex.get_width()))
        custom_levels_edit_button.scale_to_size((100, 100 * custom_levels_edit_button_tex.get_height() / custom_levels_edit_button_tex.get_width()))
        level_id = 0
        while game.GameState == MY_LEVELS:

            events = pygame.event.get()
            screen.fill((200, 180, 90))
            selected_level[0] = False
            mouse_scroll = (0, 0)

            custom_levels_play_button.update(screen)
            custom_levels_edit_button.update(screen)

            for i in range(len(events)):
                event = events[i]
                if event.type == pygame.MOUSEWHEEL:
                    mouse_scroll = (event.x, event.y)
            for event in events:
                if event.type == pygame.QUIT:
                    loop = False
                    game.GameState = QUIT
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game.GameState = MENU
                elif event.type == pygame.MOUSEBUTTONDOWN and mouse_scroll == (0, 0):
                    if scrollerbar_rect.collidepoint(event.pos):
                        scrolling = True
                    for i in range(len(text_rects)):
                        if not selected_level[0]:
                            if text_rects[i].collidepoint(event.pos):
                                selected_level[0] = True
                                selected_level[1] = text_rects[i]
                                level_id = i
                elif event.type == pygame.MOUSEBUTTONUP:
                    scrolling = False

            scroller_rect.center = (scroller_rect.center[0], scroller_rect.center[1] - mouse_scroll[1] * 4)
            if scrolling:
                scroller_rect.center = (scroller_rect.center[0], pygame.mouse.get_pos()[1])
            if scroller_rect.top < scrollerbar_rect.top:
                scroller_rect.center = (scroller_rect.center[0], scrollerbar_rect.top + (scroller_rect.height / 2))
            if scroller_rect.bottom > scrollerbar_rect.bottom:
                scroller_rect.center = (scroller_rect.center[0], scrollerbar_rect.bottom - (scroller_rect.height / 2))
            else:
                if scroller_rect.top < scrollerbar_rect.top:
                    scroller_rect.top = scrollerbar_rect.top
                elif scroller_rect.bottom > scrollerbar_rect.bottom:
                    scroller_rect.bottom = scrollerbar_rect.bottom

            UpdateMenu(menu_data, screen)

            if selected_level[1] is not None:
                pygame.draw.rect(screen, (0, 255, 0), selected_level[1], 3)
                #current_level = custom_levels[level_id] + '.txt'
                #game.GameState = LEVEL_EDITOR


            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        if custom_levels_play_button.collidesmouse():
                            if selected_level[1] is not None:
                                current_level = "custom_levels/"+custom_levels[level_id] + '.txt'
                                game.GameState = RUN_LEVEL
                        if custom_levels_edit_button.collidesmouse():
                            if selected_level[1] is not None:
                                current_level = "custom_levels/"+custom_levels[level_id] + '.txt'
                                game.GameState = LEVEL_EDITOR


            pygame.display.update()

    pygame.display.update()
