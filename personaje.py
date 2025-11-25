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
        self.moviendo = False  # Para cambiar entre idle y run
        self.accion = "idle"   # idle / run / attack
        self.atacando = False

        # Vida (HUD)
        self.vida = 100

        # ----------------------------
        # Cargar animaciones
        # ----------------------------
        # Mantengo el mismo diccionario que tenías
        self.animaciones = {
            "idle": [],
            "run": [],
            "attack": []
        }

        # ---- Cargar animación idle (las 4 imágenes nuevas) ----
        for i in range(4):
            img = pygame.image.load(f"imagenes/movimientos/quieto/quieto_{i}.png").convert_alpha()
            img = self.escalar(img)
            self.animaciones["idle"].append(img)

        # ---- Cargar animación run (las 7 imágenes viejas que tenías antes) ----
        for i in range(3):
            img = pygame.image.load(f"imagenes/movimientos/caminar/caminar_{i}.png").convert_alpha()
            img = self.escalar(img)
            self.animaciones["run"].append(img)

        # ---- Cargar animación attack (ajusta la cantidad de frames si es necesario) ----
        # Si no tienes las imágenes, puedes dejar range(0) y la lista quedará vacía -> manejado en update()
        for i in range(5):
            try:
                img = pygame.image.load(f"imagenes/characters/ataque/atk_{i}.png").convert_alpha()
                img = self.escalar(img)
                self.animaciones["attack"].append(img)
            except Exception:
                # si faltan imágenes de ataque, no rompes la carga
                pass

        # Frame inicial (asegurarse de que exista)
        if len(self.animaciones["idle"]) > 0:
            self.image = self.animaciones["idle"][0]
        else:
            # imagen fallback si algo falla
            self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
            self.image.fill((200, 200, 200))

        self.rect = self.image.get_rect(midbottom=(x, y))

    # Escalar imágenes
    def escalar(self, img):
        w, h = img.get_size()
        return pygame.transform.scale(
            img,
            (int(w * constantes.scala_personaje), int(h * constantes.scala_personaje))
        )

    # ----------------------------
    # Movimiento horizontal
    # ----------------------------
    def movimiento(self, delta_x):

        # Si está atacando, permitir mover horizontalmente pero no cambiar la animación de ataque
        accion_anterior = self.accion

        if delta_x == 0:
            self.moviendo = False
            # Solo cambiar a idle si no está atacando
            if not self.atacando:
                self.accion = "idle"
        else:
            self.moviendo = True
            # Solo cambiar a run si no está atacando
            if not self.atacando:
                self.accion = "run"

        # Si la animación cambió (p. ej. run -> idle), reiniciar frame_index para evitar out-of-range
        if self.accion != accion_anterior:
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        # Dirección del sprite
        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False

        # Aplicar movimiento horizontal
        self.rect.x += delta_x

    # ----------------------------
    # Saltar (método separado)
    # ----------------------------
    def saltar(self):
        # Solo puede saltar si está en suelo y no está en medio de una animación que lo bloquee
        if self.en_suelo and not self.atacando:
            self.vel_y = -20
            self.en_suelo = False

    # ----------------------------
    # Gravedad
    # ----------------------------
    def aplicar_gravedad(self):
        # Aumenta la velocidad vertical (gravedad)
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10

        # Mover verticalmente; las colisiones se ajustan en colisionar()
        self.rect.y += self.vel_y

    # ----------------------------
    # Colisiones con plataformas (mejorada)
    # ----------------------------
    def colisionar(self, plataformas):
        """
        Revisa colisiones con una lista de pygame.Rect (plataformas).
        Ajusta rect y en_suelo correctamente; tolerancia para evitar atravesar.
        """
        self.en_suelo = False
        for p in plataformas:
            if self.rect.colliderect(p):
                # Si venimos desde arriba (vel_y >= 0) y la parte inferior está cerca de la parte superior de la plataforma
                if self.vel_y >= 0 and self.rect.bottom <= p.top + 12:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.en_suelo = True
                else:
                    # Colisión horizontal fina: intentar separar lateralmente para evitar quedarse pegado
                    if self.rect.centerx < p.centerx:
                        # estamos a la izquierda -> empujar hacia la izquierda
                        self.rect.right = p.left
                    else:
                        # estamos a la derecha -> empujar hacia la derecha
                        self.rect.left = p.right

    # ----------------------------
    # Atacar
    # ----------------------------
    def atacar(self):
        # Inicia la animación de ataque solo si no está atacando
        if not self.atacando and len(self.animaciones.get("attack", [])) > 0:
            self.atacando = True
            self.accion = "attack"
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # ----------------------------
    # Animación según estado (segura)
    # ----------------------------
    def update(self):

        # Asegurarnos de que la acción existe en el diccionario
        if self.accion not in self.animaciones:
            self.accion = "idle"

        anim = self.animaciones[self.accion]
        cooldown = 100

        # Si por alguna razón la animación está vacía, evitar crash
        if len(anim) == 0:
            # fallback: dibujar la imagen actual sin cambiar frame
            return

        # Avanzar el frame por tiempo
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            # Si estamos en ataque y la animación terminó -> volver a idle
            if self.accion == "attack" and self.frame_index >= len(anim):
                self.atacando = False
                self.accion = "idle"
                self.frame_index = 0

        # Garantizar que frame_index esté dentro del rango
        # (evita IndexError si cambiamos rapido de animación)
        if len(anim) > 0:
            self.frame_index %= len(anim)
            self.image = anim[self.frame_index]
        else:
            # si anim vacía, mantener la imagen previa
            pass

    # ----------------------------
    # Dibujar (con soporte cámara)
    # ----------------------------
    def draw(self, screen, camera_x=0, camera_y=0):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x - camera_x, self.rect.y - camera_y))
