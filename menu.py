import pygame
pygame.init()

pygame.display.set_caption("Flip'n Disco")
screen=pygame.display.set_mode((600,750))
background = pygame.image.load('jeu_flip_disco/images/accueil.png') #entre les quotes, c'est le chemin pour accéder à l'image 1 (fond d'écran)
play_button=pygame.image.load('jeu_flip_disco/images/play.png') #entre les quotes, c'est le chemin pour accéder à l'image 2 (bouton play mais faut le changer)
play_button=pygame.transform.scale(play_button,(200,90))

running=True
while running :
    screen.blit(background,(0,0))
    screen.blit(play_button, (200,500))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()
            print("Close game")
