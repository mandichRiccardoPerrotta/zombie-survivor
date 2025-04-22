import pygame
import math
import random
import sys
import time

# Inizializzazione
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survivor")
clock = pygame.time.Clock()
pygame.mixer.init()
start_time = pygame.time.get_ticks()
tempo_paused = pygame.time.get_ticks() - start_time
tempo_paused = 0

#immagini
prato_image = pygame.transform.scale(
    pygame.image.load("images/prato.png").convert_alpha(),
    (WIDTH, HEIGHT)
)
proiettili_image = pygame.transform.scale(
    pygame.image.load("images/proiettili.png").convert_alpha(),
    (50, 50)
)

# Suoni
suono_proiettile = pygame.mixer.Sound("suoni/bulletshot-impact-sound-effect-230462.mp3")
raccolta_munizioni = pygame.mixer.Sound("suoni/pistol-cock-6014.mp3")
suono_zombie_colpito = pygame.mixer.Sound("suoni/zombie-6851.mp3")
musica_fondo = pygame.mixer.Sound("suoni/fx-braam-subdown-with-intense-drop-with-distortion-and-reverb-162383.mp3")


# Colori
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Giocatore
player_size = 40
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
life_player = 3

# Spawn proiettili
grandezza_proiettili = 10
proiettili = 10


timer_proiettili = 1000
posizione_proiettile = None  # Per disegnare il proiettile spawnato

# Zombie
zombie_size = 40
zombie_pos = [100, 100]
zombie_speed = 2

# Proiettili sparati
bullets = []
bullet_speed = 10
bullet_radius = 5

# Font
font = pygame.font.SysFont("Arial", 30)



# Disegna tutto
def draw_window():
    win.fill((30, 30, 30))
    x = (WIDTH - prato_image.get_width()) // 2
    y = (HEIGHT - prato_image.get_height()) // 2
    win.blit(prato_image, (x, y))
    pygame.draw.rect(win, GREEN, (*player_pos, player_size, player_size))
    pygame.draw.rect(win, RED, (*zombie_pos, zombie_size, zombie_size))

    # Carica la musica di sottofondo
    #musica_fondo.play()

    for b in bullets:
        pygame.draw.circle(win, BLUE, (int(b[0]), int(b[1])), bullet_radius)

    if posizione_proiettile:
        win.blit(proiettili_image, posizione_proiettile)

    # Disegna il numero di proiettili in alto a sinistra
    proiettili_text = font.render(f"︻╦╤─ {proiettili}", True, WHITE)
    win.blit(proiettili_text, (10, 10))

    # Disegna il tempo di gioco in alto a destra
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    time_text = font.render(f"Tempo: {elapsed_time}s", True, WHITE)
    win.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

    # Disegna le vite in basso a sinistra
    lives_text = font.render(f"Vite: {life_player}", True, WHITE)  # Usato 'life_player' invece di 'lives'
    win.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 10))





def calcolo_angolo_zombie():
    dx = player_pos[0] + player_size // 2 - (zombie_pos[0] + zombie_size // 2)
    dy = player_pos[1] + player_size // 2 - (zombie_pos[1] + zombie_size // 2)
    angle = math.atan2(dy, dx)
    return angle

# Movimento zombie verso il player
def move_zombie():
    dx = player_pos[0] + player_size // 2 - (zombie_pos[0] + zombie_size // 2)
    dy = player_pos[1] + player_size // 2 - (zombie_pos[1] + zombie_size // 2)
    angle = math.atan2(dy, dx)
    zombie_pos[0] += math.cos(angle) * zombie_speed
    zombie_pos[1] += math.sin(angle) * zombie_speed

# Gestisce lo spawn degli zombie


# Sparo con angolo verso il mouse
def shoot_bullet(target_x, target_y):
    dx = target_x - (player_pos[0] + player_size // 2)
    dy = target_y - (player_pos[1] + player_size // 2)
    angle = math.atan2(dy, dx)
    dir_x = math.cos(angle)
    dir_y = math.sin(angle)
    bullets.append([
        player_pos[0] + player_size // 2,
        player_pos[1] + player_size // 2,
        dir_x,
        dir_y
    ])
    suono_proiettile.play()

# Spawn di proiettili in posizione casuale
def spawn_proiettili():
    global posizione_proiettile
    x = random.randint(0, WIDTH - proiettili_image.get_width())
    y = random.randint(0, HEIGHT - proiettili_image.get_height())
    posizione_proiettile = (x, y)

# Aggiorna proiettili sparati
def update_bullets():
    global bullets, zombie_pos
    new_bullets = []
    for b in bullets:
        b[0] += b[2] * bullet_speed
        b[1] += b[3] * bullet_speed

        if zombie_pos[0] < b[0] < zombie_pos[0] + zombie_size and zombie_pos[1] < b[1] < zombie_pos[1] + zombie_size:
            zombie_pos = [random.randint(0, WIDTH // 2- zombie_size), random.randint(0, HEIGHT // 2 - zombie_size)]
            suono_zombie_colpito.play()
        else:
            new_bullets.append(b)
    bullets = new_bullets


def calcolo_collisione():
    if (player_pos[0] < zombie_pos[0] + zombie_size and
            player_pos[0] + player_size > zombie_pos[0] and
            player_pos[1] < zombie_pos[1] + zombie_size and
            player_pos[1] + player_size > zombie_pos[1]):
        angle = calcolo_angolo_zombie()

        # Sposta zombie indietro
        for _ in range(50):
            draw_window()
            zombie_pos[0] -= math.cos(angle) * zombie_speed
            zombie_pos[1] -= math.sin(angle) * zombie_speed
            pygame.display.update()

        pygame.time.delay(700)
        return 1
    else:
        return 0

def raccogli_proiettili():
    global proiettili, posizione_proiettile

    if posizione_proiettile:  # Se c'è un proiettile spawnato
        px, py = posizione_proiettile
        pw, ph = proiettili_image.get_size()

        # Rettangoli per il controllo collisione
        player_rect = pygame.Rect(*player_pos, player_size, player_size)
        proiettile_rect = pygame.Rect(px, py, pw, ph)

        if player_rect.colliderect(proiettile_rect):
            proiettili += 10
            posizione_proiettile = None

def pausa_gioco():
    global running, life_player, tempo_paused, start_time
    pausa_inizio = pygame.time.get_ticks()
    pause = True
    spessore = 3

    # Rettangoli
    posizioni_dimensioni1 = pygame.Rect(WIDTH // 10 * 3, (HEIGHT // 10 * 2) + ((HEIGHT * 2) // 100), WIDTH // 10 * 4, HEIGHT // 10)
    posizioni_dimensioni2 = pygame.Rect(WIDTH // 10 * 3, (HEIGHT // 10 * 3) + ((HEIGHT * 4) // 100), WIDTH // 10 * 4, HEIGHT // 10)
    posizioni_dimensioni3 = pygame.Rect(WIDTH // 10 * 3, (HEIGHT // 10 * 4) + ((HEIGHT * 6) // 100), WIDTH // 10 * 4, HEIGHT // 10)



    color1 = [183, 27, 27]
    color2 = [255, 255, 255]
    color3 = [230, 180, 180]

    while pause:


        mouse_pos = pygame.mouse.get_pos()

        if(life_player > 0):
            # Rettangolo 1
            pygame.draw.rect(win, color1, posizioni_dimensioni1)
            pygame.draw.rect(win, color3, posizioni_dimensioni1, spessore)
            if posizioni_dimensioni1.collidepoint(mouse_pos):
                pygame.draw.rect(win, color2, posizioni_dimensioni1, spessore)

            # Rettangolo 2
            pygame.draw.rect(win, color1, posizioni_dimensioni2)
            pygame.draw.rect(win, color3, posizioni_dimensioni2, spessore)
            if posizioni_dimensioni2.collidepoint(mouse_pos):
                pygame.draw.rect(win, color2, posizioni_dimensioni2, spessore)

            # Rettangolo 3
            pygame.draw.rect(win, color1, posizioni_dimensioni3)
            pygame.draw.rect(win, color3, posizioni_dimensioni3, spessore)
            if posizioni_dimensioni3.collidepoint(mouse_pos):
                pygame.draw.rect(win, color2, posizioni_dimensioni3, spessore)

            # Testo dentro i rettangoli
            win.blit(font.render("Resume", True, (255, 255, 255)),
                    (posizioni_dimensioni1.centerx - 50, posizioni_dimensioni1.centery - 15))
            win.blit(font.render("Restart", True, (255, 255, 255)),
                     (posizioni_dimensioni2.centerx - 50, posizioni_dimensioni2.centery - 15))
            win.blit(font.render("Quit", True, (255, 255, 255)),
                    (posizioni_dimensioni3.centerx - 30, posizioni_dimensioni3.centery - 15))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause = False
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if posizioni_dimensioni1.collidepoint(mouse_pos):
                        pausa_fine = pygame.time.get_ticks()
                        tempo_paused += pausa_fine - pausa_inizio
                        start_time += pausa_fine - pausa_inizio
                        pause = False

                    elif posizioni_dimensioni2.collidepoint(mouse_pos):
                        reset()
                        pause = False

                    elif posizioni_dimensioni3.collidepoint(mouse_pos):
                        pause = False
                        running = False
        else:
            #Rettangolo 1
            pygame.draw.rect(win, color1, posizioni_dimensioni2)
            pygame.draw.rect(win, color3, posizioni_dimensioni2, spessore)
            if posizioni_dimensioni2.collidepoint(mouse_pos):
                pygame.draw.rect(win, color2, posizioni_dimensioni2, spessore)
            # Rettangolo 2
            pygame.draw.rect(win, color1, posizioni_dimensioni3)
            pygame.draw.rect(win, color3, posizioni_dimensioni3, spessore)
            if posizioni_dimensioni3.collidepoint(mouse_pos):
                pygame.draw.rect(win, color2, posizioni_dimensioni3, spessore)

            win.blit(font.render("Restart", True, (255, 255, 255)),
                         (posizioni_dimensioni2.centerx - 50, posizioni_dimensioni2.centery - 15))
            win.blit(font.render("Quit", True, (255, 255, 255)),
                     (posizioni_dimensioni3.centerx - 30, posizioni_dimensioni3.centery - 15))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause = False
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if posizioni_dimensioni2.collidepoint(mouse_pos):
                        reset()
                        pause = False

                    elif posizioni_dimensioni3.collidepoint(mouse_pos):
                        pause = False
                        running = False
        pygame.display.update()
    # prima della pausa



def reset():
    global player_pos, life_player, proiettili, timer_proiettili, posizione_proiettile, zombie_pos, zombie_speed, bullets, start_time

    start_time = pygame.time.get_ticks()

    player_pos = [WIDTH // 2, HEIGHT // 2]
    life_player = 3
    proiettili = 10
    timer_proiettili = 1000
    posizione_proiettile = None  # Per disegnare il proiettile spawnato
    zombie_pos = [100, 100]
    zombie_speed = 2
    bullets = []


# Ciclo principale

running = True
while running:


    clock.tick(60)
    draw_window()

    # verifico che il giocatore abbia ancora vite disponibili
    if life_player <= 0:
        pausa_gioco()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and proiettili > 0:
            proiettili -= 1
            shoot_bullet(*pygame.mouse.get_pos())

    # aumento velocita dello zombie, gradualmente
    zombie_speed += 0.001
    #player_speed += 0.001
    print(zombie_speed, player_speed)
    life_player -= calcolo_collisione()

    # Movimento giocatore
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
        timer_proiettili -= 1
    if keys[pygame.K_s]:
        player_pos[1] += player_speed
        timer_proiettili -= 1
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
        timer_proiettili -= 1
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
        timer_proiettili -= 1
    if keys[pygame.K_ESCAPE]:
        pausa_gioco()



    calcolo_collisione()
    move_zombie()
    update_bullets()
    raccogli_proiettili()

    print(life_player)
    if timer_proiettili <= 0:
        spawn_proiettili()
        timer_proiettili = 1000
    pygame.display.update()


pygame.quit()
sys.exit()
