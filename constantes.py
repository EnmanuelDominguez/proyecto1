WIDTH = 800
HEIGHT = 600
FPS = 60
FONT_NAME = None # pygame default
BG_COLOR = (30, 30, 40)
BUTTON_COLOR = (70,130,180)
BUTTON_HOVER = (90,150,200)
TEXT_COLOR = (255,255,255)

#colores
WIDTH, HEIGHT = 800, 600
BG_COLOR = (25, 25, 30)
FONT_NAME = 'arial'
BUTTON_COLOR = (80, 80, 100)
BUTTON_HOVER = (100, 100, 130)
TEXTBOX_COLOR = (60, 60, 70)
TEXTBOX_ACTIVE = (100, 100, 120)
TEXT_COLOR = (255, 255, 255)

import pygame

#TAMAÑOS Y ESCALAS
ancho = WIDTH
alto = HEIGHT
#alto_personaje = 20
#ancho_personaje = 20
scala_personaje = 0.2
scala_arma = 1

# PALETA DE COLORES:
verdeGris = (224,238,224)
limon = '#EEE9BF'
slateblue4 = '#473C8B'
mediumseagreen = '#3CB371'
yellow1 = '#FFFF00'
darkgoldenrod4 = '#8B6508'
negro = (0,0,0)
blanco = (255,255,255)
springgreen = '#00FF7F'
springgreen3 = '#008B45'
cobaltgreen = '#3D9140'
darkorange2 = '#EE7600'
tan1 = '#FFA54F'
red = '#FF0000'

#COLORES
color_arma = (255,0,0)
color_personaje = (255,255,0)
color_bg = (0, 0, 20)
#otros
FPS = 60
velocidad = 5

#IMAGENES
icono = pygame.image.load("imagenes/logos/hamburguesa.png")

#BOTONES
btn_jugar = pygame.Rect(2 - 75, 400, 150, 50)
btn_salir = pygame.Rect(2 - 75, 500, 150, 50)
btn_login = pygame.Rect(2 - 75, 450, 150, 50)
btn_registrar = pygame.Rect(2 - 90, 520, 180, 50)
btn_guardar = pygame.Rect(2 - 75, 500, 150, 50)
btn_a_ventana2 = pygame.Rect(2 - 75, 500, 150, 50)
btn_volver_menu = pygame.Rect(2 - 250, 500, 150, 50)
btn_volver_v1 = pygame.Rect( 2 - 75, 500, 150, 50)
