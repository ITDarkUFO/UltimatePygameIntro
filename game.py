from sys import exit
import pygame


def display_lives():
    lives_surf = font.render(f'Lives: {lives}', False, 'Black')
    lives_rect = lives_surf.get_rect(topleft=(50, 20))

    lives_background = pygame.Rect(
        lives_rect.left - 10, lives_rect.top - 5, lives_rect.width + 15, lives_rect.height + 5)
    pygame.draw.rect(screen, '#C0E8EC', lives_background, 0, 10)
    pygame.draw.rect(screen, '#C0E8EC', lives_background, 6, 10)

    screen.blit(lives_surf, lives_rect)


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score = int(current_time / 1000)
    score_surf = font.render(
        f'Score: {score}', False, 'Black')
    score_rect = score_surf.get_rect(topleft=(300, 20))

    score_background = pygame.Rect(
        score_rect.left - 10, score_rect.top - 5, score_rect.width + 15, score_rect.height + 5)
    pygame.draw.rect(screen, '#C0E8EC', score_background, 0, 10)
    pygame.draw.rect(screen, '#C0E8EC', score_background, 6, 10)

    screen.blit(score_surf, score_rect)

    return score


pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()
font = pygame.font.Font('./font/Pixeltype.ttf', 80)

game_active = True
start_time = 0

sky_surf = pygame.image.load('./graphics/sky.png').convert()
ground_surf = pygame.image.load('./graphics/ground.png').convert()

player_surf = pygame.image.load(
    './graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 432))
player_gravity = 0
lives = 3

snail_surf = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(850, 432))

while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lives = 3
                    player_gravity = 0
                    start_time = pygame.time.get_ticks()
                    player_rect.bottom = 432
                    snail_rect.left = 850
                    game_active = True
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 432:
                if event.button == 1:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN and player_rect.bottom >= 432:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20

    if game_active:
        # Background
        screen.fill((208, 244, 247))
        screen.blit(sky_surf, (0, 132))
        screen.blit(ground_surf, (0, 432))

        # Score
        score = display_score()
        display_lives()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom > 432:
            player_rect.bottom = 432
            player_gravity = 0

        screen.blit(player_surf, player_rect)

        # Enemies
        snail_rect.x -= 5
        if snail_rect.right < 0:
            snail_rect.left = 800

        screen.blit(snail_surf, snail_rect)

        # Colliders
        if player_rect.colliderect(snail_rect):
            lives -= 1

        if lives <= 0:
            game_active = False
    else:
        screen.fill('#5e80a3')

        name_surf = font.render('Pixel Runner', False, '#C0E8EC')
        name_rect = name_surf.get_rect(center=(400, 100))
        screen.blit(name_surf, name_rect)

        player_endgame_surf = pygame.image.load(
            './graphics/Player/player_stand.png').convert_alpha()
        player_endgame_surf = pygame.transform.rotozoom(
            player_endgame_surf, 0, 2)
        player_endgame_rect = player_endgame_surf.get_rect(center=(400, 300))
        screen.blit(player_endgame_surf, player_endgame_rect)

        final_score_surf = font.render(
            f"You're score: {score}", False, '#C0E8EC')
        final_score_rect = final_score_surf.get_rect(center=(400, 450))
        screen.blit(final_score_surf, final_score_rect)

        continue_surf = font.render('Press Space to run', False, '#C0E8EC')
        continue_rect = continue_surf.get_rect(center=(400, 500))
        screen.blit(continue_surf, continue_rect)

    pygame.display.update()
    clock.tick(60)
