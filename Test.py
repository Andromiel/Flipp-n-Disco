from PlacementFunctions import *

pygame.init()

screen = pygame.display.set_mode((500,600))
Ball = MapObject(pygame.transform.scale(pygame.image.load("textures/ball.png"), (60,60)), 50,50)
Disk = MapObject(pygame.transform.scale(pygame.image.load("textures/disk.png"), (60,60)), 0,0)
Flipper = MapObject(pygame.transform.scale(pygame.image.load("textures/play_button.png"), (100,100)), 90,90)
Objects = [Disk, Ball, Flipper]
loop = True
angle = 360
count = 0
test_vec = pygame.Vector2((0, 1))
test_vec=test_vec.rotate(90)
print(test_vec)
while loop:
    screen.fill((30, 90, 120))
    pygame.draw.line(screen, (200, 0, 0), test_vec, test_vec+test_vec, 3)

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

    Ball.update(screen)
    Disk.update(screen)
    Flipper.update(screen)
    pygame.display.flip()

