import numpy as np
import pygame
class Ball:
    def __init__(self, posx = 100.0, posy = 100.0, radius = 10.0):
        self.mass = 10.0
        self.radius = radius

        self.position = np.array([posx, posy])
        self.velocity = np.array([-2.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

class BallList:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.balls = []
        self.gravity = np.array([0, -9.81*0.01])

        for i in range(2):
            self.balls.append(Ball(160.0*i-160, 160.0+i*5, 20.0))

    def ComputeCollision(self, b1, b2):
        b1tob2 = b2.position - b1.position
        b1tob2 = b1tob2/np.linalg.norm(b1tob2)
        v1i = np.dot(b1tob2, b1.velocity) * b1tob2
        v1inormal = b1.velocity - v1i
        v2i = np.dot(-b1tob2, b2.velocity) * (-b1tob2)
        v2inormal = b2.velocity - v2i


        v1f = (v1i * (b1.mass - b2.mass) + 2.0 * b2.mass * v2i)/(b1.mass + b2.mass)
        v2f = (v2i * (b2.mass - b1.mass) + 2.0 * b1.mass * v1i)/(b1.mass + b2.mass)
        b1.velocity = v1f + v1inormal
        b2.velocity = v2f + v2inormal
        offset = abs((b1.radius+b2.radius) - np.linalg.norm(b1.position-b2.position))
        b1.position -= (b1tob2) * offset
        b2.position += (b1tob2) * offset


    def Update(self):
        for i in range(len(self.balls)-1):
            for j in range(i+1, len(self.balls)):
                if(np.linalg.norm(self.balls[i].position-self.balls[j].position) <= (self.balls[i].radius + self.balls[j].radius)):
                    self.ComputeCollision(self.balls[i], self.balls[j])
        for i in range(len(self.balls)):
            self.balls[i].position += self.balls[i].velocity
            self.balls[i].velocity += self.balls[i].acceleration
            self.balls[i].velocity *= 0.999

            theta = np.radians(pygame.time.get_ticks()/10.0)
            c, s = np.cos(theta), np.sin(theta)
            R = np.array(((c, -s), (s, c)))
            self.gravity.reshape((2, 1))
            self.balls[i].acceleration = np.dot(R,self.gravity*4)
            self.balls[i].acceleration.reshape((1, 2))
            self.gravity.reshape((1, 2))

