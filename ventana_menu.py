import pygame
from botones import boton
import constantes as C


next_scene = None


def run(screen, change_scene):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(C.FONT_NAME, 36)


    def play_cb():
        change_scene('login')
        return


    def quit_cb():
        change_scene('quit')
        return


    play_btn = boton((C.WIDTH//2-120, 220, 240, 60), 'Jugar', font, play_cb)
    quit_btn = boton((C.WIDTH//2-120, 320, 240, 60), 'Salir', font, quit_cb)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                change_scene('quit')
                return
            play_btn.handle_event(event)
            quit_btn.handle_event(event)


        screen.fill(C.BG_COLOR)
        title_font = pygame.font.SysFont(C.FONT_NAME, 72)
        title = title_font.render('IC - Invasion Chatarra', True, C.TEXT_COLOR)
        screen.blit(title, title.get_rect(center=(C.WIDTH//2, 120)))


        play_btn.draw(screen)
        quit_btn.draw(screen)


        pygame.display.flip()
        clock.tick(C.FPS)