# Importez une bibliothèque de fonctions appelée 'pygame'
import pygame
from math import pi

# Initialiser le moteur de jeu
pygame.init()

# Définir les couleurs que nous utiliserons au format RVB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Définir la hauteur et la largeur de l'écran
size = [400, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

# Loop jusqu'à ce que l'utilisateur clique sur le bouton de fermeture.
done = False
clock = pygame.time.Clock()

while not done:

    # Cela limite la boucle while à un maximum de 10 fois par seconde.
    # Laissez cela de côté et nous utiliserons tout le processeur possible.
    clock.tick(10)

    for event in pygame.event.get():  # L'utilisateur a fait quelque chose
        if event.type == pygame.QUIT:  # Si l'utilisateur a cliqué sur fermer
            done = True  # Signalez que nous avons terminé afin que nous quittions cette boucle

    # Tout le code de dessin se produit après la boucle for et mais
    # dans la boucle principale while done==False loop.

    # Effacer l'écran et définir l'arrière-plan de l'écran
    screen.fill(WHITE)

    # Tracez sur l'écran une ligne VERTE de (0, 0) à (50, 30)
    # 5 pixels de large.
    pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)

    # Dessinez sur l'écran 3 lignes NOIRES, chacune de 5 pixels de large.
    # Le 'False' signifie que le premier et le dernier point ne sont pas connectés.
    pygame.draw.lines(screen, BLACK, False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)

    # Tracez sur l'écran une ligne VERTE de (0, 50) à (50, 80)
    # Parce que c'est une ligne anticrénelée, elle fait 1 pixel de large.
    pygame.draw.aaline(screen, GREEN, [0, 50], [50, 80], True)

    # Dessinez un contour rectangulaire
    pygame.draw.rect(screen, BLACK, [75, 10, 50, 20], 2)

    # Dessinez un rectangle solide
    pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])

    # Dessinez un rectangle aux coins arrondis
    pygame.draw.rect(screen, GREEN, [115, 210, 70, 40], 10, border_radius=15)
    pygame.draw.rect(screen, RED, [135, 260, 50, 30], 0, border_radius=10, border_top_left_radius=0,
                     border_bottom_right_radius=15)

    # Dessinez un contour d'ellipse, en utilisant un rectangle comme limites extérieures
    pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2)

    # Dessinez une ellipse solide, en utilisant un rectangle comme limites extérieures
    pygame.draw.ellipse(screen, RED, [300, 10, 50, 20])

    # Ceci dessine un triangle en utilisant la commande polygone
    pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)

    # Dessinez un arc dans le cadre d'une ellipse.
    # Utilisez des radians pour déterminer l'angle à dessiner.
    pygame.draw.arc(screen, BLACK, [210, 75, 150, 125], 0, pi / 2, 2)
    pygame.draw.arc(screen, GREEN, [210, 75, 150, 125], pi / 2, pi, 2)
    pygame.draw.arc(screen, BLUE, [210, 75, 150, 125], pi, 3 * pi / 2, 2)
    pygame.draw.arc(screen, RED, [210, 75, 150, 125], 3 * pi / 2, 2 * pi, 2)

    # Tracez un cercle
    pygame.draw.circle(screen, BLUE, [60, 250], 40)

    # Dessinez un seul quadrant de cercle
    pygame.draw.circle(screen, BLUE, [250, 250], 40, 0, draw_top_right=True)
    pygame.draw.circle(screen, RED, [250, 250], 40, 30, draw_top_left=True)
    pygame.draw.circle(screen, GREEN, [250, 250], 40, 20, draw_bottom_left=True)
    pygame.draw.circle(screen, BLACK, [250, 250], 40, 10, draw_bottom_right=True)

    # Allez-y et mettez à jour l'écran avec ce que nous avons dessiné.
    # Cela DOIT se produire après toutes les autres commandes de dessin.
    pygame.display.flip()

# Soyez sympa au ralenti
pygame.quit()