# register_screen.py
import pygame
import constantes as C
from botones import boton
import os

def run(screen, change_scene):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(C.FONT_NAME, 32)
    small_font = pygame.font.SysFont(C.FONT_NAME, 24)

    # Campos
    user_text = ''
    pass_text = ''
    active_field = 'user'
    show_message = ''

    # Recuadros de entrada
    user_rect = pygame.Rect(C.WIDTH//2 - 150, 220, 300, 50)
    pass_rect = pygame.Rect(C.WIDTH//2 - 150, 300, 300, 50)

    # Colores
    color_inactive = (60, 60, 70)
    color_active = (100, 100, 120)
    border_color = (130, 130, 150)

    # === Funciones internas ===
    def go_back():
        change_scene('login')

    def save_user():
        nonlocal show_message
        if not user_text or not pass_text:
            show_message = 'Complete ambos campos.'
            return
        if ',' in user_text or ',' in pass_text:
            show_message = 'No se permiten comas (,).'
            return

        with open('users.txt', 'a', encoding='utf-8') as f:
            f.write(f'{user_text},{pass_text}\n')

        show_message = 'Usuario registrado con éxito.'
        change_scene('login')

    # === Botones ===
    save_btn = boton((C.WIDTH//2 - 70, 380, 140, 45), 'Guardar', small_font, save_user)
    back_btn = boton((C.WIDTH//2 - 70, 440, 140, 45), 'Volver', small_font, go_back)

    # === Bucle principal ===
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                change_scene('quit')

            # Clic en campos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if user_rect.collidepoint(event.pos):
                    active_field = 'user'
                elif pass_rect.collidepoint(event.pos):
                    active_field = 'pass'
                save_btn.handle_event(event)
                back_btn.handle_event(event)

            # Teclado
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_TAB, pygame.K_RETURN):
                    # Cambiar entre usuario y contraseña
                    active_field = 'pass' if active_field == 'user' else 'user'
                elif event.key == pygame.K_ESCAPE:
                    go_back()
                else:
                    if active_field == 'user':
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        else:
                            user_text += event.unicode
                    elif active_field == 'pass':
                        if event.key == pygame.K_BACKSPACE:
                            pass_text = pass_text[:-1]
                        else:
                            pass_text += event.unicode

        # === Dibujo ===
        screen.fill(C.BG_COLOR)

        # Título
        title = font.render('Registrar Usuario', True, (255, 255, 255))
        screen.blit(title, (C.WIDTH//2 - title.get_width()//2, 120))

        # Etiquetas
        screen.blit(small_font.render('Usuario:', True, (200, 200, 200)), (user_rect.x, user_rect.y - 28))
        screen.blit(small_font.render('Contraseña:', True, (200, 200, 200)), (pass_rect.x, pass_rect.y - 28))

        # Campos con estilo
        pygame.draw.rect(screen, color_active if active_field == 'user' else color_inactive, user_rect, border_radius=8)
        pygame.draw.rect(screen, border_color, user_rect, width=2, border_radius=8)
        pygame.draw.rect(screen, color_active if active_field == 'pass' else color_inactive, pass_rect, border_radius=8)
        pygame.draw.rect(screen, border_color, pass_rect, width=2, border_radius=8)

        # Texto de los campos
        user_surf = font.render(user_text, True, (255, 255, 255))
        pass_surf = font.render('*' * len(pass_text), True, (255, 255, 255))
        screen.blit(user_surf, (user_rect.x + 10, user_rect.y + (user_rect.height - user_surf.get_height()) // 2))
        screen.blit(pass_surf, (pass_rect.x + 10, pass_rect.y + (pass_rect.height - pass_surf.get_height()) // 2))

        # Mensaje inferior
        if show_message:
            msg = small_font.render(show_message, True, (255, 200, 100))
            screen.blit(msg, (C.WIDTH//2 - msg.get_width()//2, 520))

        # Botones
        save_btn.draw(screen)
        back_btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)
