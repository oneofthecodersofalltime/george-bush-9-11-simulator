import pygame
import os
pygame.init()

FPS = 60
VEL = 5
ROCKET_VEL = 3
NUM_ROCKETS = 3

FG_HIT = pygame.USEREVENT + 1
AB_HIT = pygame.USEREVENT + 2

ROCKET_WIDTH, ROCKET_HEIGHT = 150, 50
ROCKET_IMAGE_FG = pygame.image.load(os.path.join("Assets", "rocket.png"))
ROCKET_FG = pygame.transform.scale(ROCKET_IMAGE_FG, (ROCKET_WIDTH, ROCKET_HEIGHT))

ROCKET_AB = pygame.transform.rotate(ROCKET_FG, 180)

AIRBUS_WIDTH, AIRBUS_HEIGHT = 200, 60
AIRBUS_IMAGE = pygame.image.load(os.path.join("Assets", "airbug.png"))
AIRBUS = pygame.transform.scale(AIRBUS_IMAGE, (AIRBUS_WIDTH, AIRBUS_HEIGHT))  # airbus

FIGHTER_WIDTH, FIGHTER_HEIGHT = 200, 50
FIGHTER_IMAGE = pygame.image.load(os.path.join("Assets", "figter.png"))
FIGHTER = pygame.transform.scale(FIGHTER_IMAGE, (FIGHTER_WIDTH, FIGHTER_HEIGHT))  # fighter

BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "background.jpg"))  # new york
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (900, 700))

BUSH = pygame.image.load(os.path.join("Assets", "bush'.png"))  # bush
BUSH_TALK_IMAGE = pygame.image.load(os.path.join("Assets", "NEW YORK.png"))
BUSH_TALK = pygame.transform.scale(BUSH_TALK_IMAGE, (500, 500))

USA_LOSES_IMAGE = pygame.image.load(os.path.join("Assets", "usa loses.jpg"))
USA_LOSES = pygame.transform.scale(USA_LOSES_IMAGE, (900, 500))

USA_WINS_IMAGE = pygame.image.load(os.path.join("Assets", "usa wins.jpg"))
USA_WINS = pygame.transform.scale(USA_WINS_IMAGE, (900, 500))


WIDTH, HEIGHT = 900, 500  # screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dont let Bush do 9/11!")

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BLACK = (0, 0, 0)


def window_drawer(fg_player, ab_player, ab_rocket, fg_rocket):
    screen.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(screen, BLACK, BORDER)
    screen.blit(BUSH, (350, 0))
    screen.blit(BUSH_TALK_IMAGE, (350, 50))
    screen.blit(AIRBUS, (ab_player.x, ab_player.y))
    screen.blit(FIGHTER, (fg_player.x, fg_player.y))
    for bullet in ab_rocket:
        pygame.draw.rect(screen, (255, 0, 0), bullet)
        screen.blit(ROCKET_AB, (bullet.x, bullet.y-25))
    for bullet in fg_rocket:
        pygame.draw.rect(screen, (0, 0, 255), bullet)
        screen.blit(ROCKET_FG, (bullet.x, bullet.y-25))
    pygame.display.update()  # updates the screen


def fg_movement(keys_pressed, fg_player):
    if keys_pressed[pygame.K_a] and fg_player.x - VEL > 0:  # left FG
        fg_player.x -= VEL
    if keys_pressed[pygame.K_w] and fg_player.y - VEL > 0:  # upward FG
        fg_player.y -= VEL
    if keys_pressed[pygame.K_s] and fg_player.y + VEL < 450:  # downward FG
        fg_player.y += VEL
    if keys_pressed[pygame.K_d] and fg_player.x + VEL < 300:  # RIGHT FG
        fg_player.x += VEL


def ab_movement(keys_pressed, ab_player):
    if keys_pressed[pygame.K_UP] and ab_player.y > 0:
        ab_player.y -= VEL
    if keys_pressed[pygame.K_RIGHT] and ab_player.x < 700:
        ab_player.x += VEL
    if keys_pressed[pygame.K_LEFT] and ab_player.x > 450:
        ab_player.x -= VEL
    if keys_pressed[pygame.K_DOWN] and ab_player.y < 450:
        ab_player.y += VEL


def handle_bullets(ab_rocket, fg_rocket, ab_player, fg_player, fg_hp, ab_hp):
    for bullet in ab_rocket:
        bullet.x -= ROCKET_VEL
        if fg_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(FG_HIT))
            ab_rocket.remove(bullet)
            fg_hp = fg_hp - 1
            if fg_hp == 0:
                while 1:
                    screen.blit(USA_LOSES, (0, 0))
                    pygame.display.update()
        elif bullet.x < 0:
            ab_rocket.remove(bullet)

    for bullet in fg_rocket:
        bullet.x += ROCKET_VEL
        if ab_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(AB_HIT))
            fg_rocket.remove(bullet)
            ab_hp = ab_hp - 1
            if ab_hp == 0:
                while 1:
                    screen.blit(USA_WINS, (0, 0))
                    pygame.display.update()
        elif bullet.x > WIDTH:
            fg_rocket.remove(bullet)
    return fg_hp, ab_hp


def main():
    fg_player = pygame.Rect(200, 200, FIGHTER_WIDTH, FIGHTER_HEIGHT)
    ab_player = pygame.Rect(600, 200, AIRBUS_WIDTH, AIRBUS_HEIGHT)
    clock = pygame.time.Clock()
    run = True
    fg_rocket = []
    ab_rocket = []
    ab_hp = 5
    fg_hp = 5
    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        fg_movement(keys_pressed, fg_player)
        ab_movement(keys_pressed, ab_player)
        for event in pygame.event.get():  # checks for events or something
            if event.type == pygame.QUIT:
                run = False  # quits from the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l and len(ab_rocket) < NUM_ROCKETS:
                    bullet = pygame.Rect(ab_player.x, ab_player.y + ab_player.height//2 - 2, 10, 5)
                    ab_rocket.append(bullet)
                if event.key == pygame.K_f and len(fg_rocket) < NUM_ROCKETS:
                    bullet = pygame.Rect(fg_player.x + fg_player.width, fg_player.y + fg_player.height//2 - 2, 10, 5)
                    fg_rocket.append(bullet)
        ab_hp, fg_hp = handle_bullets(ab_rocket, fg_rocket, ab_player, fg_player, fg_hp, ab_hp)
        window_drawer(fg_player, ab_player, ab_rocket, fg_rocket)
    pygame.quit()


if __name__ == "__main__":  # mysterious safety feature
    main()
