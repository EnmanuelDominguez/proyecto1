import pygame

class weapon:
    def __init__(self, image):
        self.original_image = image     # se guarda la original para poder voltearla
        self.image = image
        self.rect = self.image.get_rect()
        self.offset = (20, 10)  # posición relativa cuando mira a la derecha

    def update(self, jugador):
        # Voltear arma si el jugador está volteado
        if jugador.flip:
            self.image = pygame.transform.flip(self.original_image, True, False)
            offset_x = -self.offset[0]
        else:
            self.image = self.original_image
            offset_x = self.offset[0]

        # Posicionar arma respecto al jugador
        self.rect.centerx = jugador.rect.centerx + offset_x
        self.rect.centery = jugador.rect.centery + self.offset[1]

    def draw(self, screen, camera_x=0):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        screen.blit(self.image, draw_rect)

