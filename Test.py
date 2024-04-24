from PlacementFunctions import *

pygame.init()

screen = pygame.display.set_mode((500,600))
Ball = MapObject(pygame.transform.smoothscale(pygame.image.load("textures/ball.png"), (60,60)), 50,50)
Disk = MapObject(pygame.transform.smoothscale(pygame.image.load("textures/disk.png"), (60,60)), 0,0)
Flipper = MapObject(pygame.transform.smoothscale(pygame.image.load("textures/play_button.png"), (100,100)), 90,90)
Objects = [Disk, Ball, Flipper]
loop = True
angle = 360
count = 0
pygame.transform.scale2x(screen)
pygame.transform.scale2x(screen)
pygame.transform.scale2x(screen)




while loop:
    screen.fill((30, 90, 120))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        for object in Objects:
            if event.type == pygame.MOUSEBUTTONDOWN and object.collidesmouse():
                if event.button == pygame.BUTTON_LEFT:
                    object.reposition = REPOS_OBJECT
                elif event.button == pygame.BUTTON_RIGHT:
                    object.reposition = REPOS_ROTATION_CENTER
            elif event.type == pygame.MOUSEBUTTONUP:
                object.reposition = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    object.rotate_around_point(10)
                elif event.key == pygame.K_DOWN:
                    object.rotate_around_point(-10)

    #surface = pygame.Surface((500, 600))
    Ball.update(screen)
    Disk.update(screen)
    Flipper.update(screen)
    #pygame.transform.scale(surface,(screen.get_width(), screen.get_height()))
    #screen.blit(surface, (0, 0))
    #pygame.display.flip()
    pygame.display.update()

