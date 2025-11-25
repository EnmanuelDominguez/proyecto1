import pygame


class boton:
    def __init__(self, rect, text, font, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.hover = False      


    def draw(self, surf):
        color = (90,150,200) if self.hover else (70,130,180)
        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        txt = self.font.render(self.text, True, (255,255,255))
        txt_rect = txt.get_rect(center=self.rect.center)
        surf.blit(txt, txt_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()