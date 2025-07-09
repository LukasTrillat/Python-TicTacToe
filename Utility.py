import pygame as PG
from pygame.locals import *

def load_image(sFile,transp=False, scale = (1,1)):
    try: image = PG.image.load(sFile)
    except PG.error:
           raise SystemExit()
    image = image.convert_alpha()

    if transp:
       color = image.get_at((0,0))
       image.set_colorkey(color,RLEACCEL)

    if scale:
         image = PG.transform.scale(image, scale)

    return image

def draw_text(screen,texto, pos_x,pos_y, color, align = "center",scale = 36):
    fuente = PG.font.Font("Minecraft.ttf", scale) #Fuente de texto
    superficie = fuente.render(texto, True, color) 

    text_w = superficie.get_width() #Calcular anchura del texto
    text_h = superficie.get_height() #Calcular longitud del texto
    if align == "center": #Alinear en en centro
        screen.blit(superficie, (pos_x - text_w/2,pos_y - (text_h/2)))
    elif align == "left": #Alinear a la izquierda
        screen.blit(superficie, (pos_x,pos_y - (text_h/2)))

def draw_sprite(screen, sprites_list, pos_x=0, pos_y=0, x_scale=1, y_scale=1, frame=0, speed=0.005):

    #frame = ut.draw_sprite(screen, sprites_list, 100, 100, 1, 1, frame)
    frame += speed
    if int(frame) >= len(sprites_list):
        frame = 0

    sprite = sprites_list[int(frame)]
    xsc = int(sprite.get_width() * x_scale)
    ysc = int(sprite.get_height() * y_scale)
    sprite_escalado = PG.transform.scale(sprite, (xsc, ysc))
    screen.blit(sprite_escalado, (pos_x, pos_y))
    return frame  

def show_data(screen, variables_dict):
    fuente = PG.font.SysFont("Arial", 24)
    y_offset = 0

    rect_surface = PG.Surface((100,300), PG.SRCALPHA)
    rect_surface.fill((0, 0, 0, 20)) 
    screen.blit(rect_surface, (0, 0))

    for n, v in variables_dict.items():
        texto = f"{n}: {v}"
        superficie = fuente.render(texto, True, (255, 255, 255))
        text_w = superficie.get_width()/2
        screen.blit(superficie, (20, 10 + y_offset))
        y_offset += 30

def play_sound(sound,volumen = 1.0): 
    PG.mixer.init()
    sound = PG.mixer.Sound(sound)
    sound.set_volume(volumen)
    sound.play()


