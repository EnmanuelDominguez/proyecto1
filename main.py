import pygame
from constantes import *
import ventana_menu
import ventana_login
import ventana_registro
import ventana_juego
 
class SceneSwitch(Exception):
    """Excepción interna para cambiar de escena inmediatamente."""
    def __init__(self, target):
        super().__init__('switch to ' + str(target))
        self.target = target

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('IC - Invasion Chatarra')

    current_scene = 'menu'
    scene_args = None

    # change_scene ahora lanza SceneSwitch para salir instantáneo de la escena
    def change_scene(value):
        # value puede ser string ('menu') o tupla ('game', username)
        raise SceneSwitch(value)

    running = True
    while running:
        try:
            if current_scene == 'menu':
                ventana_menu.run(screen, change_scene)
            elif current_scene == 'login':
                ventana_login.run(screen, change_scene)
            elif current_scene == 'register':
                ventana_registro.run(screen, change_scene)
            elif current_scene == 'game':
                username = scene_args[0] if scene_args else None
                juego = ventana_juego.GameScreen()  # ✅ crear instancia
                juego.run(screen, change_scene, username)  # ✅ llamar método
            elif current_scene == 'quit':
                running = False
            else:
                # fallback
                ventana_menu.run(screen, change_scene)
        except SceneSwitch as s:
            # s.target puede ser string o tupla
            val = s.target
            if isinstance(val, tuple):
                current_scene = val[0]
                scene_args = val[1:]
            else:
                current_scene = val
                scene_args = None
            # si es 'quit' salimos
            if current_scene == 'quit':
                running = False

    pygame.quit()

if __name__ == '__main__':
    main()