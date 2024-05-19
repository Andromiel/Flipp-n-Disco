from PlacementFunctions import *

from PlacementFunctions import GameComponent

def ReadContent(filename):
    level_data = open(filename, "r")
    data_list = level_data.readlines()
    nb_objects = len(data_list)
    level_data.close()
    list_objects = []
    for i in range(nb_objects):

        if data_list[i][-1] == '\n':
            data_list[i] = data_list[i][:-1]

        attributes = str(data_list[i]).split(";")
        pos = attributes[0].split(",")
        pos = (int(pos[0]), int(pos[1]))
        size = attributes[2].split(",")
        size = (int(size[0]), int(size[1]))
        angle = int(attributes[4])
        skin_name = str(attributes[1])[0:]
        skin = pygame.image.load("textures/" + skin_name)
        #skin = pygame.transform.rotate(skin, angle)
        rotation_pos = attributes[3].split(",")
        rotation_pos = (int(float(rotation_pos[0])), int(float(rotation_pos[1])))
        component_type = int(attributes[5])
        object = GameComponent(skin, skin_name, pos[0], pos[1], rotation_pos, 0, component_type)
        center = object.rect.center
        object.resize(60 / object.rect.size[0])
        object.move_at(center)
        object.scale_to_size(size)
        object.rotate_around_point(angle)
        list_objects.append(object)
    return list_objects

def SaveContent(list_game_object, filename):
    level_data = open(filename, "w")
    nb_objects = len(list_game_object)
    for i in range(nb_objects):
        object = list_game_object[i]
        level_data.write(str(object.rect.centerx) + ',' + str(list_game_object[i].rect.centery))
        level_data.write(';' + object.imgname.replace("textures/", ''))
        level_data.write(';'+str(object.scaled_img.get_width())+','+str(object.scaled_img.get_height()))
        level_data.write(';'+str(object.rotationcenter[0])+','+str(object.rotationcenter[1]))
        level_data.write(';'+str(object.angle))
        level_data.write(';' + str(object.component_type))
        level_data.write('\n')
    level_data.close()

def DefaultContent(filename):
    level_data = open(filename, "w")
    for i in range(5):
        level_data.write(str(i * 30) + ',' + str(i * 30))
        level_data.write(';ball.png')
        level_data.write(';50,50')
        level_data.write(';'+str(i * (30+25)) + ',' + str(i * (30+25)))
        level_data.write(';0\n')

    level_data.close()