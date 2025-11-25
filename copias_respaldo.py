#personaje.py
import pygame
import constantes
print(">>> cargando personaje desde este archivo")

class personaje:
    def __init__(self, x, y):

        self.flip = False
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0
        self.en_suelo = False
        self.moviendo = False
        self.accion = "idle"   # idle / run / attack
        self.atacando = False

        self.vida = 100

        # ----------------------------
        # Cargar animaciones
        # ----------------------------
        self.animaciones = {
            "idle": [],
            "run": [],
            "attack": []
        }

        # ---- Cargar animación idle ----
        for i in range(4):
            img = pygame.image.load(f"imagenes/characters/quieto/quieto_{i}.png").convert_alpha()
            img = self.escalar(img)
            self.animaciones["idle"].append(img)

        # ---- Cargar animación run ----
        for i in range(7):
            img = pygame.image.load(f"imagenes/characters/player/frame_{i}.png").convert_alpha()
            img = self.escalar(img)
            self.animaciones["run"].append(img)

        # ---- Cargar animación attack ----
        for i in range(5):  # AJUSTA SI TIENES MÁS O MENOS FRAMES
            #img = pygame.image.load(f"imagenes/characters/ataque/atk_{i}.png").convert_alpha()
            #img = self.escalar(img)
            self.animaciones["attack"].append(img)

        # Primer frame
        self.image = self.animaciones["idle"][0]
        self.rect = self.image.get_rect(midbottom=(x, y))

    # Escalar imágenes
    def escalar(self, img):
        w, h = img.get_size()
        return pygame.transform.scale(
            img,
            (int(w * constantes.scala_personaje), int(h * constantes.scala_personaje))
        )

    # Movimiento horizontal
    def movimiento(self, delta_x):

        if self.atacando:   # si está atacando, no cambiar animación
            return

        if delta_x == 0:
            self.moviendo = False
            self.accion = "idle"
        else:
            self.moviendo = True
            self.accion = "run"

        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False

        self.rect.x += delta_x

    # Gravedad
    def aplicar_gravedad(self):
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10

        self.rect.y += self.vel_y

    # Colisiones con plataformas
    def colisionar(self, plataformas):
        self.en_suelo = False
        for p in plataformas:
            if self.rect.colliderect(p):
                # cayendo → choca con una plataforma
                if self.vel_y > 0 and self.rect.bottom - self.vel_y <= p.top:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.en_suelo = True

    # Atacar
    def atacar(self):
        if not self.atacando:
            self.atacando = True
            self.accion = "attack"
            self.frame_index = 0

    # Actualizar animación
    def update(self):

        anim = self.animaciones[self.accion]
        cooldown = 100

        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            # si terminó animación de ataque
            if self.accion == "attack" and self.frame_index >= len(anim):
                self.atacando = False
                self.accion = "idle"
                self.frame_index = 0

            self.frame_index %= len(anim)

        self.image = anim[self.frame_index]

    # Dibujar
    def draw(self, screen, camera_x=0):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x - camera_x, self.rect.y))


#ventana_juego.py
import pygame
import constantes
from personaje import personaje
# from arma import weapon   # Descomenta si tienes el módulo arma.py
# from enemy import Enemigo  # Si añades enemigos reales

class GameScreen:
    def __init__(self):
        # Cargar animaciones del personaje y crear instancia
        self.jugador = personaje(100, constantes.alto - 60)  # posición inicial

        # --- Si tenías una animación externa, ya no es necesaria aquí ---
        # Arma (si existe tu módulo weapon)
        try:
            from arma import weapon
            self.imagen_pistola = pygame.image.load("imagenes/armas/4_1.png").convert_alpha()
            self.imagen_pistola = self.escalar_img(self.imagen_pistola, constantes.scala_arma)
            self.pistola = weapon(self.imagen_pistola)
        except Exception:
            # si no tienes arma.py o imagen, no rompas el juego
            self.pistola = None

        # Variables de control
        self.reloj = pygame.time.Clock()
        self.en_pausa = False
        self.progreso = 0
        self.font = pygame.font.SysFont(None, 36)

        # Plataformas de ejemplo (puedes cargar desde un mapa después)
        self.plataformas = [
            pygame.Rect(0, constantes.alto - 50, 2000, 50),  # suelo largo para probar cámara
            pygame.Rect(250, constantes.alto - 150, 300, 20),
            pygame.Rect(700, constantes.alto - 230, 220, 20),
        ]

        # Cámara
        self.camera_x = 0
        self.nivel_ancho = 2000  # AJUSTA al tamaño real de tu nivel

        # Enemigos (si quieres los añades más tarde)
        self.enemigos = []  # lista vacía para respetar tu estructura

    def escalar_img(self, image, scale):
        w = image.get_width()
        h = image.get_height()
        return pygame.transform.scale(image, (int(w * scale), int(h * scale)))

    def run(self, screen, change_scene, username):
        running = True
        mover_izquierda = False
        mover_derecha = False

        while running:
            dt = self.reloj.tick(constantes.FPS if hasattr(constantes, "FPS") else 60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    change_scene("menu")

                # ------------------ TECLAS ------------------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        mover_izquierda = True
                    if event.key == pygame.K_d:
                        mover_derecha = True

                    if event.key == pygame.K_SPACE:
                        # salto por tecla
                        self.jugador.saltar()

                    if event.key == pygame.K_j:
                        # tecla de ataque
                        self.jugador.atacar()

                    if event.key == pygame.K_ESCAPE:
                        self.en_pausa = not self.en_pausa  # alternar pausa

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        mover_izquierda = False
                    if event.key == pygame.K_d:
                        mover_derecha = False

            # ------------------ MODO PAUSA ------------------
            if self.en_pausa:
                self.mostrar_pausa(screen)
                pygame.display.flip()
                continue

            # ------------------ MOVIMIENTO ------------------
            delta_x = 0
            velocidad = getattr(constantes, "velocidad", 5)
            if mover_derecha:
                delta_x = velocidad
            if mover_izquierda:
                delta_x = -velocidad

            # Llamadas al jugador (respetando tu lógica original)
            self.jugador.movimiento(delta_x)
            self.jugador.aplicar_gravedad()
            # Colisiones: pasamos la lista de pygame.Rect
            self.jugador.colisionar(self.plataformas)
            self.jugador.update()

            # Actualizar arma (si existe)
            if self.pistola is not None:
                try:
                    self.pistola.update(self.jugador)
                except Exception:
                    pass

            # ------------------ CÁMARA (limitada) ------------------
            self.camera_x = self.jugador.rect.centerx - constantes.ancho // 2

            # Evitar cámara negativa (izquierda infinita)
            if self.camera_x < 0:
                self.camera_x = 0

            # Límite derecho según ancho del nivel
            max_cam = max(0, self.nivel_ancho - constantes.ancho)
            if self.camera_x > max_cam:
                self.camera_x = max_cam

            # ------------------ DIBUJAR ------------------
            screen.fill((50, 50, 60))

            # Dibujar plataformas con offset de cámara
            for p in self.plataformas:
                pygame.draw.rect(screen, (150, 150, 150),
                                 (p.x - self.camera_x, p.y, p.width, p.height))

            # Dibujar jugador y arma (offset en draw del jugador)
            self.jugador.draw(screen, self.camera_x)

            if self.pistola is not None:
                try:
                    # si tu pistola tiene draw que recibe jugador u offset, adáptalo
                    self.pistola.draw(screen, self.camera_x)
                except Exception:
                    pass

            # Dibujar barra de progreso / HUD
            self.actualizar_barra_progreso(screen)
            # vida en HUD (si quieres lo extiendes)
            vida_text = self.font.render(f"Vida: {self.jugador.vida}", True, (255, 255, 255))
            screen.blit(vida_text, (20, 50))

            pygame.display.flip()

        # Regresar al menú al salir del bucle
        change_scene("menu")

    def mostrar_pausa(self, screen):
        overlay = pygame.Surface((constantes.ancho, constantes.alto))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        texto = self.font.render("PAUSA - Presiona ESC para continuar o Q para salir", True, (255, 255, 255))
        rect = texto.get_rect(center=(constantes.ancho // 2, constantes.alto // 2))
        screen.blit(texto, rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            pygame.quit()

    def actualizar_barra_progreso(self, screen):
        self.progreso = min(self.progreso + 0.2, 100)
        barra_ancho = 300
        barra_alto = 20
        x = 20
        y = 20
        pygame.draw.rect(screen, (100, 100, 100), (x, y, barra_ancho, barra_alto))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, int(barra_ancho * (self.progreso / 100)), barra_alto))

######################## ventana_juego.py con el mapa####################################
import pygame
import constantes
from personaje import personaje
import pytmx
from pytmx.util_pygame import load_pygame

class GameScreen:
    def __init__(self):
        # Cargar mapa
        self.cargar_mapa("imagenes/mapa/mapa1.tmx")
        
        # Crear jugador en posición inicial - AJUSTADA para el mapa
        self.jugador = personaje(100, 400)  # Posición Y más abajo para el suelo
        
        # Variables de control
        self.reloj = pygame.time.Clock()
        self.progreso = 0
        self.font = pygame.font.SysFont(None, 36)
        
        # Cámara
        self.camera_x = 0
        self.camera_y = 0
        
        # Estados de teclas
        self.mover_izquierda = False
        self.mover_derecha = False

    def cargar_mapa(self, filename):
        """Carga el mapa TMX correctamente"""
        try:
            self.tmx_data = load_pygame(filename)
            self.plataformas = []
            
            # Dimensiones del nivel
            self.nivel_ancho = self.tmx_data.width * self.tmx_data.tilewidth
            self.nivel_alto = self.tmx_data.height * self.tmx_data.tileheight
            
            print(f"✅ Mapa cargado: {self.nivel_ancho}x{self.nivel_alto}")
            print(f"📐 Tamaño de tiles: {self.tmx_data.tilewidth}x{self.tmx_data.tileheight}")
            
            # Extraer plataformas para colisiones - MÉTODO CORREGIDO
            for layer in self.tmx_data.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid in layer:
                        if gid != 0:
                            tile = self.tmx_data.get_tile_image_by_gid(gid)
                            if tile:
                                rect = pygame.Rect(
                                    x * self.tmx_data.tilewidth,
                                    y * self.tmx_data.tileheight,
                                    self.tmx_data.tilewidth,
                                    self.tmx_data.tileheight
                                )
                                self.plataformas.append(rect)
            
            print(f"🎯 Plataformas extraídas: {len(self.plataformas)}")
                            
        except Exception as e:
            print(f"❌ Error cargando mapa: {e}")
            # Fallback básico
            self.plataformas = [pygame.Rect(0, 450, 5000, 50)]
            self.nivel_ancho = 5000
            self.nivel_alto = constantes.alto

    def dibujar_mapa(self, screen):
        """Dibuja el mapa CORREGIDO - como en Tiled"""
        if hasattr(self, 'tmx_data') and self.tmx_data:
            try:
                # Fondo azul cielo (como Terraria)
                screen.fill((135, 206, 235))
                
                # DIBUJO CORREGIDO - Usando el método render_to_new_surface
                # Esta es la forma más segura de dibujar mapas TMX
                temp_surface = pygame.Surface((self.nivel_ancho, self.nivel_alto))
                
                # Renderizar todas las capas visibles
                for layer in self.tmx_data.visible_layers:
                    if isinstance(layer, pytmx.TiledTileLayer):
                        for x, y, gid in layer:
                            tile = self.tmx_data.get_tile_image_by_gid(gid)
                            if tile:
                                temp_surface.blit(tile, (x * self.tmx_data.tilewidth, 
                                                       y * self.tmx_data.tileheight))
                
                # Dibujar solo la parte visible en la pantalla
                screen.blit(temp_surface, (0, 0), 
                           (self.camera_x, self.camera_y, constantes.ancho, constantes.alto))
                
            except Exception as e:
                print(f"❌ Error dibujando mapa: {e}")
                self.dibujar_mapa_fallback(screen)
        else:
            self.dibujar_mapa_fallback(screen)

    def dibujar_mapa_simple(self, screen):
        """Método alternativo SIMPLE para dibujar el mapa"""
        if hasattr(self, 'tmx_data') and self.tmx_data:
            try:
                # Fondo azul cielo
                screen.fill((135, 206, 235))
                
                # Dibujar capa por capa, tile por tile - MÉTODO SIMPLE
                for layer in self.tmx_data.visible_layers:
                    if hasattr(layer, 'data'):
                        for x, y, gid in layer:
                            if gid != 0:
                                tile = self.tmx_data.get_tile_image_by_gid(gid)
                                if tile:
                                    # POSICIÓN ABSOLUTA CORRECTA
                                    draw_x = x * self.tmx_data.tilewidth - self.camera_x
                                    draw_y = y * self.tmx_data.tileheight - self.camera_y
                                    
                                    # Solo dibujar si está en la pantalla (optimización)
                                    if (-self.tmx_data.tilewidth < draw_x < constantes.ancho and 
                                        -self.tmx_data.tileheight < draw_y < constantes.alto):
                                        screen.blit(tile, (draw_x, draw_y))
                
            except Exception as e:
                print(f"Error método simple: {e}")
                self.dibujar_mapa_fallback(screen)

    def dibujar_mapa_fallback(self, screen):
        """Mapa de fallback visual"""
        screen.fill((135, 206, 235))  # Cielo azul
        
        # Dibujar plataformas como rectángulos
        for plataforma in self.plataformas:
            if (plataforma.x < self.camera_x + constantes.ancho and 
                plataforma.x + plataforma.width > self.camera_x):
                pygame.draw.rect(screen, (100, 100, 100), 
                               (plataforma.x - self.camera_x, plataforma.y - self.camera_y, 
                                plataforma.width, plataforma.height))

    def actualizar_camara(self):
        """Cámara estilo Terraria - suave y centrada"""
        # Calcular posición objetivo
        target_x = self.jugador.rect.centerx - constantes.ancho // 2
        target_y = self.jugador.rect.centery - constantes.alto // 2
        
        # Suavizado (más lento para mejor experiencia)
        self.camera_x += (target_x - self.camera_x) * 0.05
        self.camera_y += (target_y - self.camera_y) * 0.05
        
        # Límites de la cámara
        self.camera_x = max(0, min(self.camera_x, self.nivel_ancho - constantes.ancho))
        self.camera_y = max(0, min(self.camera_y, self.nivel_alto - constantes.alto))

    def actualizar_progreso(self):
        """Progreso de exploración"""
        if self.nivel_ancho > constantes.ancho:
            distancia_recorrida = self.jugador.rect.x
            distancia_total = self.nivel_ancho - constantes.ancho
            self.progreso = (distancia_recorrida / distancia_total) * 100
            self.progreso = min(100, max(0, self.progreso))

    def dibujar_hud(self, screen):
        """HUD estilo Terraria - MEJORADO"""
        # Barra de exploración (centrada arriba)
        barra_ancho = 400
        barra_alto = 20
        x = (constantes.ancho - barra_ancho) // 2
        y = 15
        
        # Fondo de la barra
        pygame.draw.rect(screen, (40, 40, 40), (x, y, barra_ancho, barra_alto), border_radius=3)
        # Barra de progreso
        if self.progreso > 0:
            pygame.draw.rect(screen, (50, 200, 50), (x, y, int(barra_ancho * (self.progreso / 100)), barra_alto), border_radius=3)
        # Borde
        pygame.draw.rect(screen, (200, 200, 200), (x, y, barra_ancho, barra_alto), 2, border_radius=3)
        
        # Texto de exploración
        texto = self.font.render(f"Exploración: {int(self.progreso)}%", True, (255, 255, 255))
        screen.blit(texto, (x, y + 25))
        
        # Panel de información (esquina inferior izquierda)
        panel_ancho = 200
        panel_alto = 60
        panel_x = 10
        panel_y = constantes.alto - panel_alto - 10
        
        # Fondo del panel
        panel_bg = pygame.Surface((panel_ancho, panel_alto))
        panel_bg.set_alpha(180)
        panel_bg.fill((0, 0, 0))
        screen.blit(panel_bg, (panel_x, panel_y))
        
        # Información del jugador
        vida_text = self.font.render(f"Vida: {self.jugador.vida}", True, (255, 50, 50))
        screen.blit(vida_text, (panel_x + 10, panel_y + 10))
        
        # Nombre de usuario si existe
        if hasattr(self, 'username') and self.username:
            user_text = self.font.render(f"Jugador: {self.username}", True, (255, 255, 255))
            screen.blit(user_text, (panel_x + 10, panel_y + 35))

    def run(self, screen, change_scene, username):
        """Bucle principal CORREGIDO"""
        self.username = username  # Guardar nombre de usuario
        running = True
        
        while running:
            self.reloj.tick(60)
            
            # --- EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    change_scene("menu")
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.mover_izquierda = True
                    if event.key == pygame.K_d:
                        self.mover_derecha = True
                    if event.key == pygame.K_SPACE:
                        self.jugador.saltar()
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        change_scene("menu")
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.mover_izquierda = False
                    if event.key == pygame.K_d:
                        self.mover_derecha = False
            
            # --- ACTUALIZACIÓN ---
            delta_x = 0
            if self.mover_derecha:
                delta_x = 5
            if self.mover_izquierda:
                delta_x = -5
            
            self.jugador.movimiento(delta_x)
            self.jugador.aplicar_gravedad()
            self.jugador.colisionar(self.plataformas)
            self.jugador.update()
            
            self.actualizar_camara()
            self.actualizar_progreso()
            
            # --- DIBUJADO ---
            # PRUEBA AMBOS MÉTODOS - descomenta el que funcione mejor:
            self.dibujar_mapa_simple(screen)  # ← Este debería funcionar mejor
            # self.dibujar_mapa(screen)       # ← Método alternativo
            
            self.jugador.draw(screen, self.camera_x)
            self.dibujar_hud(screen)
            
            pygame.display.flip()
        
        change_scene("menu")
        ############################main.py
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
