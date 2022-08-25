import pygame
import os

from pygame.transform import rotate
pygame.font.init()  # Initerar pygame font library
pygame.mixer.init()

# Kalids input: Homing missle aktiveras av UP + DOWMN
# Afifa input: Drop box: RAPID FIRE, FREZZE, SPEED

WIDTH, HEIGHT = 900, 500  # Display parameterar
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Den gör displayen för spelet
pygame.display.set_caption("Space Fighters")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE_KALID = (111, 35, 190)
PURPLE_MO = (255, 0, 255)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)


HELATH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'impact_spaceship.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Laser_gun.mp3'))
BACKGROUND_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'space_music.mp3'))

# BACKGROUND_SOUND = BACKGROUND_SOUND_RAW.set_volume(0.9)


FFS = 60
VEL = 5
BULLET_VEL = VEL * 2
MAX_BULLET = 5
MAX_MISSELES = 1
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55, 45)

YELLOW_HIT = pygame.USEREVENT + 1  # Så här gör man ett event i pygame
# pygame.USEREVENT är ett tal och lägger til för unik id
RED_HIT = pygame.USEREVENT + 2
# Kalid input
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png',))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), (90))
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png',))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), (270))

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health):
    """[ Funktionen: Args är de två rektanglar som output vadera spaceship ritas
        på enligt deras x och y koordinater.

        Teori 1 :Ritar allt på displayen WIN genom funktionerna DISPLAYENSNAMN.blit()
        argument är rektanglar (pygame.Rect()) eller image (pygame.image.load()).
        För att kunna se något på spelet måste pygame.display.update() skrivas på slutet ]

    Args:
        red (Rect): [Röda spaceshipen ritas på en rect som har (0,0) på vänstra översta hörnet]
        yellow ([Rect]): [Gula spaceshipen ritas på en rect som har (0,0) på vänstra översta hörnet]
    """
    # Ritar allt på displayen #
    WIN.blit(SPACE, (0, 0))
    # För ett tillägg i funktionen ska synas kräves den update av display
    # Nu kan vi rita spaceship på deras x och y koordinater Why? För att kunna flytta dem enligt WIN
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HELATH_FONT.render(
        " Health:" + str(red_health), 1, WHITE)
    yellow_health_text = HELATH_FONT.render(
        " Health:" + str(yellow_health), 1, WHITE)
    red_dead = HELATH_FONT.render(
        " Health:" + str(0), 1, WHITE)
    yellow_dead = HELATH_FONT.render(
        " Health:" + str(red_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in red_bullet:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullet:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def handle_yellow_movement(key_pressed, yellow):
    """
    [Funkiton: Flyttar den gula spaceshipen mha a,w,s,d
    Teori 2: Key_pressed[] är True eller False beroende om [pygame.K_{KNAPPEN}]
        är använd och att den gula  s.ship inte befinnner sig vid BORDER ELLER LÄMNAR SKÄRM.

        LEFT: yellow.x - VEL > 0 ska alltid var postiv om den ska röra sig åt vänster.

        RIGHT: yellow.x + VEL + yellow.width < BORDER.x + 5 den ska inte kunna passer

        BORDER genom att checka att yellow.x + steget + den bredd inte passer BORDER.

        UP: yellow.y - VEL > 0 ska alltid vara postiv om den ska röra sig mot toppen.

        DOWN: yellow.y + VEL + yellow.height < HEIGHT - 12 ska vara mindre en HEIGHT
        annars lämnar den skärmen och det vill vi inte ! +5 och -12 är för att bilden
        av yellow och red spaceship är har inte samma storlek so
        yellow och red
    ]

    Args:
        key_pressed ([type]): [ Key_pressed är en funktion som checkar medans main()
        while-loopen är aktiv om någon knapp är tryckt med output True eller False]
        yellow ([Rect]): [Gula spaceshipen ritas på en rect som har (0,0) på vänstra översta hörnet]

    """
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Vänster
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 5:  # Höger
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Upp
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 12:  # Ner
        yellow.y += VEL


def handle_red_movement(key_pressed, red):
    """[ANALOGT MED DOCSTRING OVAN]

    Args:
        key_pressed ([type]): [ Key_pressed är en funktion som checkar medans main()
        while-loopen är aktiv om någon knapp är tryckt med output True eller False]
        yellow ([Rect]): [Gula spaceshipen ritas på en rect som har (0,0) på vänstra översta hörnet]
    """
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 10:
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 12:
        red.y += VEL


# Skapa bullets, hantera kollisoner med bullet och bullet exist display
def handle_bullets(yellow_bullet, red_bullet, yellow, red):
    for bullet in yellow_bullet:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):  # Båda måste vara rect
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullet.remove(bullet)

    for bullet in red_bullet:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):  # Båda måste vara rect
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            # Den rederas för att den träffade den gula
            red_bullet.remove(bullet)
        elif bullet.x < 0:
            red_bullet.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
             2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    """[ Funktionen:
    While-loopen: Så länge den loop är TRUE så start och forsätt spelet.

    QUIT: För att göra en lista av event som kan sker under spelet så används pygame.event.get()
    om typen av event är pygame.Quit då kommer run = False och loopen kommer termineras.
    Genom att pygame.quit() kommer att köras

    FFS: För att spelupplevelsen inte ska variera beroende på vilken dator man kör med
    så är FFS = 60. "Klockan" clock = pygame.time.Clock() skapa ett objekt som hjälper
    till att hålla koll på mängd tid. clock.tick() är en funktion som gör kontroller
    antal gånger frames per second loopen går.

    BULLET: Funktionen
    """
    # Vi ritar dem på en "rektangel" för positoner
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_misseles = []
    yellow_missles = []
    red_bullet = []
    yellow_bullet = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True

    BACKGROUND_SOUND.play(-1).set_volume(0.8)
    while run:
        # Kontroller hur snabbt loopen går. Cap på 60 frames per second
        clock.tick(FFS)
        for event in pygame.event.get():  # Den ger dig en lista av alla spel
            if event.type == pygame.QUIT:
                run = False  # While loopen kommer att termineras
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(yellow_bullet) < MAX_BULLET and red_health > 0:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_m and len(red_bullet) < MAX_BULLET and yellow_health > 0:
                    # Skottet åker mot (0,0) från höger
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()
               # if event.key == pygame.K_1 and len(yellow_missles) < MAX_MISSELES

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            BACKGROUND_SOUND.stop()
            break  # Någon vann
            # Checkar om man tycker på en knapp (60 FFS)
            # Riktingen av spaceship ska vara samma som där den åker
        key_pressed = pygame.key.get_pressed()
        handle_yellow_movement(key_pressed, yellow)
        handle_red_movement(key_pressed, red)

        handle_bullets(yellow_bullet, red_bullet, yellow, red)
        draw_window(red, yellow, red_bullet, yellow_bullet,
                    red_health, yellow_health)
    main()


if __name__ == '__main__':  # Spelet kör omm denna fil körs enbart
    main()
