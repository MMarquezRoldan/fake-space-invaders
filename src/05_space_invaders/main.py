import pygame

# Space Invaders but fake edition for educational purposes

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

dt = 0

while running:
    # Poll for events
    # pygame.QUIT event means the user clicked X to close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Filling the screen with a solid color
    screen.fill("black")

    pygame.draw.rect(screen, "grey", (player_pos.x, player_pos.y, 40, 40))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 200 * dt
    if keys[pygame.K_s]:
        player_pos.y += 200 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 200 * dt
    if keys[pygame.K_d]:
        player_pos.x += 200 * dt

    # Render the game

    # flip() the display to put my work on screen
    pygame.display.flip()

    dt = clock.tick(144) / 1000  # Limits FPS to 144

pygame.quit()
