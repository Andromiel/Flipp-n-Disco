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
        coordinates = attributes[0].split(",")
        coordinates = (int(coordinates[0]), int(coordinates[1]))
        skin = str(attributes[1])
        object = MapObject(skin, coordinates[0], coordinates[1])
        list_objects.append(object)
    return list_objects

def SaveContent(list_game_object, filename):
    level_data = open(filename, "w")
    nb_objects = len(list_game_object)
    for i in range(nb_objects):
        level_data.write(str(list_game_object[i].rect.x) + ',' + str(list_game_object[i].rect.y))
        level_data.write(';' + object.imgname.replace("textures/", '') + "\n")
    level_data.close()

def DefaultContent(filename):
    level_data = open(filename, "w")
    for i in range(5):
        level_data.write(str(i * 30) + ',' + str(i * 30))
        level_data.write(';' + "ball.png" + "\n")
    level_data.close()

