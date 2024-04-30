from PlacementFunctions import *

pygame.init()

screen = pygame.display.set_mode((500,600))
Ball = MapObject(pygame.transform.smoothscale(pygame.image.load("textures/ball.png"), (60,60)), 50,50)
Disk = MapObject(pygame.transform.smoothscale(pygame.image.load("textures/disk.png"), (60,60)), 0,0)
Flipper = MapObject(pygame.transform.smoothscale(pygame.image.load("textures/flipper.png"), (100,50)), 90,90)
Objects = [Disk, Ball, Flipper]
loop = True
angle = 360
count = 0
current_option = 1
font = pygame.font.Font("freesansbold.ttf", 32)
text1 = font.render("Option :", True, (255,255,255))
text2_1 = font.render("Reposition", True, (255,255,255))
text2_2 = font.render("Rescale", True, (255,255,255))
text = text2_1

while loop:
    screen.fill((30, 90, 120))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        for object in Objects:
            if event.type == pygame.MOUSEBUTTONDOWN and object.collidesmouse():
                if event.button == pygame.BUTTON_LEFT:
                    if current_option == 1:
                        object.reposition = REPOS_OBJECT
                    else:
                        object.reposition = RESCALE_OBJECT
                elif event.button == pygame.BUTTON_RIGHT:
                    object.reposition = REPOS_ROTATION_CENTER
            elif event.type == pygame.MOUSEBUTTONUP:
                object.reposition = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    object.rotate_around_point(10)
                elif event.key == pygame.K_DOWN:
                    object.rotate_around_point(-10)
                elif event.key == pygame.K_SPACE:
                    if current_option == 1:
                        current_option = 2
                    else:
                        current_option = 1

    if current_option == 1:
        text = text2_1
    else:
        text = text2_2

    screen.blit(text1, (10,10))
    screen.blit(text, (150,10))

    Ball.update(screen)
    Disk.update(screen)
    Flipper.update(screen)
    pygame.display.update()

