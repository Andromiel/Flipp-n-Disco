import pygame.draw

from Ball import Ball, BallList

from Physics2D import SignedAngle, ConvexPolygon, LineIntersection, SegmentIntersection, PhysicsEngine

import pygame
import numpy as np
import random as rd
import time



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

print(SignedAngle((-1.0, -1.0)))

pygame.init()

# Set the width and height of the screen [width, height]

WIDTH = 1000
HEIGHT = 700
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

ball = Ball()

g = 9.81

ball_list = BallList(WIDTH, HEIGHT)

polygon = ConvexPolygon(*[(rd.randint(100, 400), rd.randint(100, 400)) for i in range(20)])
polygon.Translate(np.array((400, 400)))

print(SegmentIntersection(np.array((1, 1)), np.array((3, 2)), np.array((2.5, 0)), np.array((2.1, 1.4))))

engine = PhysicsEngine()
#engine.convex_polygons.append(ConvexPolygon(*[np.array((np.cos(i*np.pi/8), np.sin(i*np.pi/8)))*40 for i in range(16)]))
#engine.convex_polygons[-1].Translate((200, 200))
engine.convex_polygons.append(ConvexPolygon((0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT), fixed=True))
engine.convex_polygons[-1].Translate((-WIDTH/2, HEIGHT/2))
engine.convex_polygons.append(ConvexPolygon((0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT), fixed=True))
engine.convex_polygons[-1].Translate((WIDTH/2, -HEIGHT/2))
engine.convex_polygons.append(ConvexPolygon((0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT), fixed=True))
engine.convex_polygons[-1].Translate((WIDTH/2, HEIGHT*1.5))
engine.convex_polygons.append(ConvexPolygon((0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT), fixed=True))
engine.convex_polygons[-1].Translate((WIDTH*1.5, HEIGHT/2))

for i in range(2):
    engine.convex_polygons.append(ConvexPolygon((0, 0), (100, 100), (100, 0), (0, 100)))
    print(engine.convex_polygons[-1].mean_point)
engine.convex_polygons.append(ConvexPolygon((0, 0), (400, 100), (400, 0), (0, 100), fixed=True))
engine.convex_polygons[-1].Translate((500, 400))
engine.convex_polygons[-1].Rotate(-0.0)
engine.convex_polygons.append(ConvexPolygon((0, 0), (100, 150), (100, -20), (0, 10), fixed=True))
engine.convex_polygons[-2].Translate((100, 100))
engine.convex_polygons[-2].velocity = np.array((100, 0))
engine.convex_polygons[-1].Translate((300, 100))
engine.convex_polygons[-3].Translate((400, 300))



#engine.convex_polygons[-1].Rotate(-0.1)

now_time = time.time()
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
    #polygon.DisplayPoints(screen)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        engine.convex_polygons[1].Translate((0, 1))
    if keys[pygame.K_DOWN]:
        engine.convex_polygons[1].Translate((0, -1))
    if keys[pygame.K_LEFT]:
        engine.convex_polygons[1].Translate((1, 0))
    if keys[pygame.K_RIGHT]:
        engine.convex_polygons[1].Translate((-1, 0))
    if keys[pygame.K_SPACE]:
        engine.convex_polygons.append(ConvexPolygon((0, 0), (0, 100), (100, 100), (100, 0)))
        engine.convex_polygons[-1].Translate(np.array(pygame.mouse.get_pos()))
        time.sleep(1)
    delta_time = time.time()-now_time
    now_time += delta_time
    engine.Update(screen, delta_time)

    '''if keys[pygame.K_SPACE]:
        polygon.DisplayAllPoints(screen)
    if keys[pygame.K_LCTRL]:
        polygon = ConvexPolygon(*[(rd.randint(100, 400), rd.randint(100, 400)) for i in range(100)])
        polygon.Translate(np.array((300, 300)))'''

    '''
    ball_list.Update()

    for i in range(len(ball_list.balls)):
        pygame.draw.circle(screen, (0, 255, 0), (WIDTH - ball_list.balls[i].position[0], HEIGHT - ball_list.balls[i].position[1]), ball_list.balls[i].radius)
        if (ball_list.balls[i].position[0] + ball_list.balls[i].radius >= WIDTH):
            ball_list.balls[i].velocity[0] = -abs(ball_list.balls[i].velocity[0])
        if (ball_list.balls[i].position[0] - ball_list.balls[i].radius <= 0):
            ball_list.balls[i].velocity[0] = abs(ball_list.balls[i].velocity[0])
        if (ball_list.balls[i].position[1] + ball_list.balls[i].radius >= HEIGHT):
            ball_list.balls[i].velocity[1] = -abs(ball_list.balls[i].velocity[1])
        if (ball_list.balls[i].position[1] - ball_list.balls[i].radius <= 0):
            ball_list.balls[i].velocity[1] = abs(ball_list.balls[i].velocity[1])
    '''

    # --- Drawing code should go here

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()