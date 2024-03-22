import pygame
import math
from game import Game
pygame.init()

#générer la fenêtre du jeu
pygame.display.set_caption("Flip'n'Disco")
screen = pygame.display.set_mode((600,750))

#importer l'arrière-plan
background = pygame.image.load('Menu (600 x 750 px).jpg')


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
            #elif custom_button.collidepoint(event.pos):
                #basculer sur le mode custom
