from PlacementFunctions import *

class GameComponent(MapObject):
    def __init__(self, img = None, imgname = None, posx=0, posy=0, size=(20,20), rotationcenter=None, angle=None):
        MapObject.__init__(self, img, imgname, posx, posy, show_rotating_point=True)
        self.physics_engineID = [-1, -1]#type, index

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
        skin = pygame.transform.smoothscale(skin, (size[0], size[1]))
        skin = pygame.transform.rotate(skin, angle)
        rotation_pos = attributes[3].split(",")
        rotation_pos = (int(float(rotation_pos[0])), int(float(rotation_pos[1])))
        object = GameComponent(skin, skin_name, pos[0], pos[1], size, rotation_pos, angle)
        list_objects.append(object)
    return list_objects

def SaveContent(list_game_object, filename):
    level_data = open(filename, "w")
    nb_objects = len(list_game_object)
    for i in range(nb_objects):
        object = list_game_object[i]
        level_data.write(str(object.rect.centerx) + ',' + str(list_game_object[i].rect.centery))
        level_data.write(';' + object.imgname.replace("textures/", ''))
        level_data.write(';'+str(object.rect.width)+','+str(object.rect.height))
        level_data.write(';'+str(object.rotationcenter[0])+','+str(object.rotationcenter[1]))
        level_data.write(';'+str(object.angle)+'\n')
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