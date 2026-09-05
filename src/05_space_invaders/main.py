from pathlib import Path

import pygame

# Space Invaders but fake edition for educational purposes

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Settings
FPS_LIMIT = 144

PLAYER_SIZE = 40
PLAYER_SPEED = 200

BULLET_WIDTH = 4
BULLET_HEIGHT = 14
BULLET_SPEED = 700
SHOT_COOLDOWN = 0.50

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

bullets = []
shot_timer = 0

dt = 0

BASE_DIR = Path(__file__).resolve().parent
MUSIC_PATH = BASE_DIR.parent / "media" / "audio" / "soundtrack_01.mp3"

pygame.mixer.music.load(str(MUSIC_PATH))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

while running:
    # Poll for events
    # pygame.QUIT event means the user clicked X to close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Filling the screen with a solid color
    screen.fill("black")

    pygame.draw.rect(
        screen, "grey", (player_pos.x, player_pos.y, PLAYER_SIZE, PLAYER_SIZE)
    )

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos.y > 0:
        player_pos.y -= PLAYER_SPEED * dt
    if keys[pygame.K_s] and player_pos.y < screen.get_height() - PLAYER_SIZE:
        player_pos.y += PLAYER_SPEED * dt
    if keys[pygame.K_a] and player_pos.x > 0:
        player_pos.x -= PLAYER_SPEED * dt
    if keys[pygame.K_d] and player_pos.x < screen.get_width() - PLAYER_SIZE:
        player_pos.x += PLAYER_SPEED * dt
    if keys[pygame.K_SPACE] and shot_timer <= 0:
        bullets.append(
            pygame.Vector2(
                player_pos.x + PLAYER_SIZE / 2 - BULLET_WIDTH / 2,
                player_pos.y,
            )
        )
        shot_timer = SHOT_COOLDOWN

    shot_timer -= dt

    # Render the game
    for bullet in bullets:
        bullet.y -= BULLET_SPEED * dt
        pygame.draw.rect(
            screen, "white", (bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)
        )

    bullets = [bullet for bullet in bullets if bullet.y > -BULLET_HEIGHT]

    # flip() the display to put my work on screen
    pygame.display.flip()

    dt = clock.tick(FPS_LIMIT) / 1000  # Limits FPS to 144


pygame.quit()
