import pygame
import math
from ennemi import Ennemi

#importer la carte des niveaux
background2=pygame.image.load('LEVEL MAP VERTE.png')
chiffre1=pygame.image.load('Chiffre 1 (encore).png')
chiffre2=pygame.image.load('Chiffre2.png')
chiffre3=pygame.image.load('Chiffre3.png')
chiffre4=pygame.image.load('Chiffre4.png')
chiffre5=pygame.image.load('Chiffre5.png')
chiffre6=pygame.image.load('Chiffre6.png')
chiffre7=pygame.image.load('Chiffre7.png')
chiffre8=pygame.image.load('Chiffre8.png')
chiffre9=pygame.image.load('Chiffre9.png')

chiffre1_rect = chiffre1.get_rect()
chiffre2_rect = chiffre1.get_rect()
chiffre3_rect = chiffre1.get_rect()
chiffre4_rect = chiffre1.get_rect()
chiffre5_rect = chiffre1.get_rect()
chiffre6_rect = chiffre1.get_rect()
chiffre7_rect = chiffre1.get_rect()
chiffre8_rect = chiffre1.get_rect()
chiffre9_rect = chiffre1.get_rect()

#créer une classe pour le jeu
class Game:
    def __init__(self):
        # définir si le jeu a commencé
        self.is_playing = False

        self.display = False
        self.display2 = False
        self.display3 = False
        self.display4 = False
        self.display5 = False
        self.display6 = False
        self.display7 = False
        self.display8 = False
        self.display9 = False
    def update(self,screen):
        screen.blit(background2,(0,0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.display= True

        if self.display:
            chiffre1_rect = chiffre1.get_rect()
            chiffre1_rect.x = math.ceil(screen.get_width() - 550)
            chiffre1_rect.y = math.ceil(screen.get_height() - 650)
            screen.blit(chiffre1, chiffre1_rect)

        if keys[pygame.K_2]:
            self.display=True
            self.display2=True
        if self.display2:
            chiffre2_rect = chiffre2.get_rect()
            chiffre2_rect.x = math.ceil(screen.get_width() - 350)
            chiffre2_rect.y = math.ceil(screen.get_height() - 650)
            screen.blit(chiffre2, chiffre2_rect)

        if keys[pygame.K_3]:
            self.display=True
            self.display2=True
            self.display3 = True
        if self.display3:
            chiffre3_rect = chiffre3.get_rect()
            chiffre3_rect.x = math.ceil(screen.get_width() - 150)
            chiffre3_rect.y = math.ceil(screen.get_height() - 650)
            screen.blit(chiffre3, chiffre3_rect)

        if keys[pygame.K_4]:
            self.display=True
            self.display2=True
            self.display3 = True
            self.display4 = True
        if self.display4:
            chiffre4_rect = chiffre4.get_rect()
            chiffre4_rect.x = math.ceil(screen.get_width() - 550)
            chiffre4_rect.y = math.ceil(screen.get_height() - 425)
            screen.blit(chiffre4, chiffre4_rect)

        if keys[pygame.K_5]:
            self.display=True
            self.display2=True
            self.display3 = True
            self.display4 = True
            self.display5=True
        if self.display5:
            chiffre5_rect = chiffre5.get_rect()
            chiffre5_rect.x = math.ceil(screen.get_width() - 350)
            chiffre5_rect.y = math.ceil(screen.get_height() - 425)
            screen.blit(chiffre5, chiffre5_rect)

        if keys[pygame.K_6]:
            self.display=True
            self.display2=True
            self.display3 = True
            self.display4 = True
            self.display5=True
            self.display6=True
        if self.display6:
            chiffre6_rect = chiffre6.get_rect()
            chiffre6_rect.x = math.ceil(screen.get_width() - 150)
            chiffre6_rect.y = math.ceil(screen.get_height() - 425)
            screen.blit(chiffre6, chiffre6_rect)

        if keys[pygame.K_7]:
            self.display=True
            self.display2=True
            self.display3 = True
            self.display4 = True
            self.display5=True
            self.display6=True
            self.display7 = True
        if self.display7:
            chiffre7_rect = chiffre7.get_rect()
            chiffre7_rect.x = math.ceil(screen.get_width() - 550)
            chiffre7_rect.y = math.ceil(screen.get_height() - 200)
            screen.blit(chiffre7, chiffre7_rect)

        if keys[pygame.K_8]:
            self.display=True
            self.display2=True
            self.display3 = True
            self.display4 = True
            self.display5=True
            self.display6=True
            self.display7 = True
            self.display8 = True
        if self.display8:
            chiffre8_rect = chiffre8.get_rect()
            chiffre8_rect.x = math.ceil(screen.get_width() - 350)
            chiffre8_rect.y = math.ceil(screen.get_height() - 200)
            screen.blit(chiffre8, chiffre8_rect)

        if keys[pygame.K_9]:
            self.display=True
            self.display2=True
            self.display3 = True
            self.display4 = True
            self.display5=True
            self.display6=True
            self.display7=True
            self.display8=True
            self.display9=True
        if self.display9:
            chiffre9_rect = chiffre9.get_rect()
            chiffre9_rect.x = math.ceil(screen.get_width() - 150)
            chiffre9_rect.y = math.ceil(screen.get_height() - 200)
            screen.blit(chiffre9, chiffre9_rect)



