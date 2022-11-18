from sys import exit
import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            './graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            './graphics/Player/player_walk_2.png').convert_alpha()
        self.frames = [player_walk_1, player_walk_2]
        self.frame_index = 0

        self.player_jump = pygame.image.load(
            './graphics/Player/jump.png').convert_alpha()
        
        self.player_damage = pygame.image.load(
            './graphics/Player/player_damage.png').convert_alpha()

        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=(80, 432))

        self.gravity = 0
        self.lives = 3
        self.get_damage = False

        self.jump_sound = pygame.mixer.Sound('./audio/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 432:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 432:
            self.rect.bottom = 432
            self.get_damage = False

    def animation_state(self):
        if self.get_damage:
            self.image = self.player_damage
        elif self.rect.bottom < 432:
            self.image = self.player_jump
        else:
            self.frame_index += 0.1

            if self.frame_index > 2:
                self.frame_index = 0

            self.image = self.frames[int(self.frame_index)]

    def damage(self):
        self.lives -= 1
        self.gravity = -15
        self.get_damage = True

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type: str):
        super().__init__()

        if type.lower() == 'fly':
            fly_1 = pygame.image.load(
                './graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load(
                './graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 300

        elif type.lower() == 'snail':
            snail_1 = pygame.image.load(
                './graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load(
                './graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]

            y_pos = 432

        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(
            midbottom=(random.randint(800, 1100), y_pos))

        self.lives = 1

    def animation_state(self):
        self.frame_index += 0.1

        if self.frame_index > 2:
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def damage(self):
        self.lives -= 1
        if self.lives == 0:
            self.kill()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_lives():
    lives_surf = font.render(f'Lives: {player.sprite.lives}', False, 'Black')
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


def collision_sprite():
    sprites = pygame.sprite.spritecollide(player.sprite, obstacle_group, False)
    if sprites:
        player.sprite.damage()
        for sprite in sprites:
            sprite.damage()


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('./font/Pixeltype.ttf', 80)
game_active = True
start_time = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Background
sky_surf = pygame.image.load('./graphics/sky.png').convert()
ground_surf = pygame.image.load('./graphics/ground.png').convert()

sky_1_pos = 0
sky_2_pos = 800
ground_pos_1 = 0
ground_pos_2 = 800

# Intro scene
player_stand = pygame.image.load(
    './graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 300))

name_surf = font.render('Pixel Runner', False, '#C0E8EC')
name_rect = name_surf.get_rect(center=(400, 100))

continue_surf = font.render('Press Space to run', False, '#C0E8EC')
continue_rect = continue_surf.get_rect(center=(400, 500))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

bg_music = pygame.mixer.Sound('./audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)


while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(
                    ['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                player.sprite.lives = 3
                player.sprite.rect.bottom = 432
                player.sprite.get_damage = False
                start_time = pygame.time.get_ticks()

    if game_active:
        # Background
        screen.fill((208, 244, 247))
        screen.blit(sky_surf, (sky_1_pos, 132))
        screen.blit(sky_surf, (sky_2_pos, 132))
        screen.blit(ground_surf, (ground_pos_1, 432))
        screen.blit(ground_surf, (ground_pos_2, 432))

        sky_1_pos -= 1.5
        sky_2_pos -= 1.5
        ground_pos_1 -= 3
        ground_pos_2 -= 3

        if sky_1_pos <= -800:
            sky_1_pos = 0
            sky_2_pos = 800
        
        if ground_pos_1 <= -800:
            ground_pos_1 = 0
            ground_pos_2 = 800

        # Score
        score = display_score()
        display_lives()

        # Player
        player.draw(screen)
        player.update()

        # Enemies
        obstacle_group.draw(screen)
        obstacle_group.update()

        collision_sprite()

        game_active = player.sprite.lives > 0
    else:
        obstacle_group.empty()

        screen.fill('#5e80a3')
        screen.blit(name_surf, name_rect)
        screen.blit(player_stand, player_stand_rect)

        final_score_surf = font.render(f"You're score: {score}", False, '#C0E8EC')
        final_score_rect = final_score_surf.get_rect(center=(400, 450))
        screen.blit(final_score_surf, final_score_rect)

        screen.blit(continue_surf, continue_rect)

    pygame.display.update()
    clock.tick(60)
