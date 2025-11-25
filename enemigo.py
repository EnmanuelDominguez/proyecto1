import pygame

class Enemigo:
    def __init__(self, x1, x2, y):
        self.x1 = x1
        self.x2 = x2
        self.vel = 2
        self.image = pygame.Surface((40, 60))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(midbottom=(x1, y))

    def update(self):
        self.rect.x += self.vel
        if self.rect.x < self.x1 or self.rect.x > self.x2:
            self.vel *= -1

    def draw(self, screen, camera_x=0):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        screen.blit(self.image, draw_rect)

