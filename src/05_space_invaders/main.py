import random
from pathlib import Path

import pygame

# Space Invaders but fake edition for educational purposes

# TODO:
#   1. Spawn enemies per level
#   2. Be able to hit enemies
#   3. Sound for the pew pew pew
#   4. Settings
#   5. Top bar
#   6. Basic upgrades
#   7. Real spaceship img

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Settings
FPS_LIMIT = 144

PLAYER_SIZE = 40
PLAYER_SPEED = 200

ENEMY_SIZE = 30
ENEMY_GAP = 20
ENEMY_SPEED = 20
ENEMY_COLUMNS = 10
ENEMY_TOP_MARGIN = 60
ENEMY_FIRST_LEVEL = 15
ENEMY_HEALTH = 10
ENEMY_SPAWN_BAND = 400
ENEMY_MIN_GAP = 10
ENEMY_PLACE_TRIES = 30
LEVEL_GROWTH = 1.5

BULLET_WIDTH = 4
BULLET_DMG = 10
BULLET_HEIGHT = 14
BULLET_SPEED = 700
SHOT_COOLDOWN = 0.50


level = 1

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

bullets = []
shot_timer = 0

dt = 0

# Music
BASE_DIR = Path(__file__).resolve().parent
MUSIC_PATH = BASE_DIR.parent / "media" / "audio" / "soundtrack_01.mp3"
BULLET_SOUND = BASE_DIR.parent / "media" / "audio" / "basic_shot.mp3"

pygame.mixer.music.load(str(MUSIC_PATH))
pygame.mixer.music.set_volume(0.3)

pygame.mixer.music.play()

bullet_sound = pygame.mixer.Sound(str(BULLET_SOUND))
bullet_sound.set_volume(0.4)


def spawn_wave(level):
    """Scatters enemies above the screen without overlaps, x1.5 more on every level."""
    count = int(ENEMY_FIRST_LEVEL * LEVEL_GROWTH ** (level - 1))
    band = ENEMY_SPAWN_BAND * count / ENEMY_FIRST_LEVEL
    reach = ENEMY_SIZE + ENEMY_MIN_GAP

    wave = []
    for _ in range(count):
        for _ in range(ENEMY_PLACE_TRIES):
            candidate = pygame.Vector2(
                random.uniform(0, screen.get_width() - ENEMY_SIZE),
                random.uniform(-band, -ENEMY_SIZE),
            )
            if all(
                abs(candidate.x - other["pos"].x) >= reach
                or abs(candidate.y - other["pos"].y) >= reach
                for other in wave
            ):
                break
        wave.append({"pos": candidate, "health": ENEMY_HEALTH})
    return wave


enemies = spawn_wave(level)

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
        bullet_sound.play()
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

    for enemy in enemies:
        enemy["pos"].y += ENEMY_SPEED * dt
        pygame.draw.rect(
            screen, "red", (enemy["pos"].x, enemy["pos"].y, ENEMY_SIZE, ENEMY_SIZE)
        )

    # Bullet hits: mark first, rebuild both lists afterwards
    surviving_bullets = []
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet.x, bullet.y, BULLET_WIDTH, BULLET_HEIGHT)

        hit = None
        for enemy in enemies:
            if bullet_rect.colliderect(
                (enemy["pos"].x, enemy["pos"].y, ENEMY_SIZE, ENEMY_SIZE)
            ):
                hit = enemy
                break

        if hit is not None:
            hit["health"] -= BULLET_DMG
        elif bullet.y > -BULLET_HEIGHT:
            surviving_bullets.append(bullet)

    bullets = surviving_bullets
    enemies = [enemy for enemy in enemies if enemy["health"] > 0]

    if not enemies:
        level += 1
        enemies = spawn_wave(level)

    # flip() the display to put my work on screen
    pygame.display.flip()

    dt = clock.tick(FPS_LIMIT) / 1000  # Limits FPS to 144


pygame.quit()
