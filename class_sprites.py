import pygame
import random

pygame.init()

screen_width = 600
screen_height = 750
BLACK = (0, 0, 0)

class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.original_image = pygame.image.load('images/ball.png')
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.bottomright = (screen_width, screen_height)
        self.speed_x = 0
        self.speed_y = 0
        self.started = False

    def update(self):
        if self.started:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if self.rect.y <= 0 or self.rect.y >= screen_height:
                self.speed_y = -self.speed_y
            if self.rect.x <= 0 or self.rect.x >= screen_width:
                self.speed_x = -self.speed_x

    def launch(self):
        if not self.started:
            self.speed_x = random.choice([-5, 5])
            self.speed_y = random.choice([-5, 5])
            self.started = True

class Flipper(pygame.sprite.Sprite):
    def __init__(self, x, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, screen_height - 50))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.x > screen_width // 2:
            self.rect.x -= 5
        if keys[pygame.K_k] and self.rect.x < screen_width // 2:
            self.rect.x += 5

flipper_left = Flipper(screen_width // 3, 'images/flipper.png')
flipper_right = Flipper(screen_width * 2 // 3, 'images/flipper.png')

all_sprites = pygame.sprite.Group()
all_sprites.add(flipper_left, flipper_right)
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Flip'n Disco")

all_sprites = pygame.sprite.Group()
ball = Ball(20, 20)
all_sprites.add(ball)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.launch()

    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
