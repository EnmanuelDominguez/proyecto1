import pygame
import constantes
from personaje import personaje
import pytmx
from pytmx.util_pygame import load_pygame

class GameScreen:
    def __init__(self):
        # Cargar mapa
        self.cargar_mapa("imagenes/mapa1/mapa1.tmx")
        
        # Crear jugador en posición inicial - AJUSTADA para el mapa
        self.jugador = personaje(200, 400)  # Posición Y más abajo para el suelo
        
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


def dibujar_mapa(self):
    tw = self.tmx_data.tilewidth
    th = self.tmx_data.tileheight

    for layer in self.tmx_data.layers:

        if hasattr(layer, "tiles"):
            parallax_x = getattr(layer, "parallax_x", 1)
            parallax_y = getattr(layer, "parallax_y", 1)

            for x, y, gid in layer.tiles():
                tile = self.tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    draw_x = x * tw - self.camera_x * (1 - parallax_x)
                    draw_y = y * th - self.camera_y * (1 - parallax_y)
                    if draw_x > -tw and draw_x < constantes.ancho and draw_y > -th and draw_y < constantes.alto:
                        self.screen.blit(tile, (draw_x, draw_y))

        elif hasattr(layer, "image") and layer.image:
            parallax_x = getattr(layer, "parallax_x", 1)
            parallax_y = getattr(layer, "parallax_y", 1)
            draw_x = -self.camera_x * (1 - parallax_x)
            draw_y = -self.camera_y * (1 - parallax_y)
            self.screen.blit(layer.image, (draw_x, draw_y))
