"""Exemple d'affichage d'une fenêtre simple."""
from time import sleep

import pygame
from pygame.locals import QUIT

# Initialise screen
from engine.map import Map
# My Mac has a resolution of（2560 × 1600）

pygame.init()

# todo display Map
m = Map()


screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption('Basic Pygame program')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()

# Définir les couleurs que nous utiliserons au format RVB
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

background.fill((250, 250, 250))

# Display some text
font = pygame.font.Font(None, 36)
text = font.render("Hello There", 1, (10, 10, 10))
textpos = text.get_rect()
textpos.centerx = background.get_rect().centerx
background.blit(text, textpos)
pygame.draw.line(screen, GREEN, [0, 0], [500,500], 5)
# sleep(3)
# Blit everything to the screen
screen.blit(background, (0, 0))


pygame.display.flip()

# Event loop
continuer = 1
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
    screen.blit(background, (0, 0))
    pygame.display.flip()

