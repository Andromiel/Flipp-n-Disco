import pygame
import math
from game import Game, chiffre1_rect, chiffre2_rect, chiffre3_rect, chiffre4_rect, chiffre5_rect, chiffre6_rect, chiffre7_rect, chiffre8_rect, chiffre9_rect
pygame.init()

"""chiffre1=pygame.image.load('Chiffre 1 (encore).png')
chiffre1_rect = chiffre1.get_rect()
chiffre2=pygame.image.load('Chiffre2.png')
chiffre2_rect = chiffre1.get_rect()
chiffre3=pygame.image.load('Chiffre3.png')
chiffre3_rect = chiffre1.get_rect()
chiffre4=pygame.image.load('Chiffre4.png')
chiffre4_rect = chiffre1.get_rect()
chiffre5=pygame.image.load('Chiffre5.png')
chiffre5_rect = chiffre1.get_rect()
chiffre6=pygame.image.load('Chiffre6.png')
chiffre6_rect = chiffre1.get_rect()
chiffre7=pygame.image.load('Chiffre7.png')
chiffre7_rect = chiffre1.get_rect()
chiffre8=pygame.image.load('Chiffre8.png')
chiffre8_rect = chiffre1.get_rect()
chiffre9=pygame.image.load('Chiffre9.png')
chiffre9_rect = chiffre1.get_rect()"""

#générer la fenêtre du jeu
pygame.display.set_caption("Flip'n'Disco")
screen = pygame.display.set_mode((600,750))

#importer l'arrière-plan
background = pygame.image.load('Menu (600 x 750 px).jpg')

#importer la carte des niveaux
background2=pygame.image.load('LEVEL MAP.png')


#charger notre bouton pour lancer la partie
play_button = pygame.image.load('transp.png')
play_button = pygame.transform.scale(play_button, (600,600))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width()-600)
play_button_rect.y = math.ceil(screen.get_height()-650)

#charger notre bouton pour le lancement du mode custom
custom_button = pygame.image.load('Custom button.png')
custom_button = pygame.transform.scale(custom_button, (600,600))
custom_button_rect = play_button.get_rect()
custom_button_rect.x = math.ceil(screen.get_width()-560)
custom_button_rect.y = math.ceil(screen.get_height()-350)

#chargement du jeu

game=Game()
running=True

#chargement du niveau 1:
level_1=False
if level_1:
    screen.blit(background2,(0,0))

#boucle tant que fenêtre allumée
while running:
    #appliquer arrière-plan:
    screen.blit(background, (0,0))

    #vérifier si le jeu a commencé
    if game.is_playing:
        #déclencher les instructions de la partie:
        game.update(screen)
    #vérifier si le jeu n'a pas commencé:
    else:
        #ajout du menu
        screen.blit(play_button, play_button_rect)
        screen.blit(custom_button, custom_button_rect)

    # mettre à jour l'écran
    pygame.display.flip()

    # si le joueur ferme cette fenêtre
    for event in pygame.event.get():
        # que l'évènement est fermeture de fenêtre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #vérification si souris en collision avec bouton jouer
            if play_button_rect.collidepoint(event.pos):
                #mettre le jeu en mode lancé
                game.is_playing = True
                """if chiffre1_rect.collidepoint(event.pos):
                    screen.blit(background2, (0, 0))
                elif chiffre2_rect.collidepoint(event.pos):
                    screen.blit(background2, (0, 0))
                elif chiffre3_rect.collidepoint(event.pos):
                    screen.blit(background2, (0, 0))
                elif chiffre4_rect.collidepoint(event.pos):
                    screen.blit(background2, (0, 0))
                elif chiffre5_rect.collidepoint(event.pos):
                    screen.blit(background2, (0, 0))
                elif chiffre6_rect.collidepoint(event.pos):
                    screen.blit(background2, (0, 0))
                elif chiffre7_rect.collidepoint(event.pos):
                    screen.blit(background2, (0, 0))
                elif chiffre8_rect.collidepoint(event.pos):
                    screen.blit(background2, (0, 0))
                elif chiffre9_rect.collidepoint(event.pos):
                    screen.blit(background2, (0, 0))
            #elif custom_button.collidepoint(event.pos):
                #basculer sur le mode custom"""
