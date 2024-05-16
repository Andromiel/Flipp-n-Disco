from PlacementFunctions import *


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
        skin = str(attributes[1])
        size = attributes[2].split(",")
        size = (int(size[0]), int(size[1]))
        rotation_pos = attributes[3].split(",")
        rotation_pos = (int(rotation_pos[0]), int(rotation_pos[1]))
        angle = int(attributes[0])
        object = MapObject(skin, pos[0], pos[1], size, rotation_pos, angle)
        list_objects.append(object)
    return list_objects

def SaveContent(list_game_object, filename):
    level_data = open(filename, "w")
    nb_objects = len(list_game_object)
    for i in range(nb_objects):
        level_data.write(str(list_game_object[i].rect.x) + ',' + str(list_game_object[i].rect.y))
        level_data.write(';' + object.imgname.replace("textures/", ''))
        level_data.write(';'+str(object.size))
        level_data.write(';'+str(object.rotationcenter))
        level_data.write(';'+str(object.angle))
    level_data.close()

def DefaultContent(filename):
    level_data = open(filename, "w")
    for i in range(5):
        level_data.write(str(i * 30) + ',' + str(i * 30))
        level_data.write('; ball.png')
        level_data.write(';50,50')
        level_data.write(';'+str(i * 30+25) + ',' + str(i * 30+25))
        level_data.write(';0\n')

    level_data.close()

DefaultContent("LevelData.txt")