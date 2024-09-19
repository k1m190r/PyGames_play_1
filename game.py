import random
import pygame

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, KEYUP

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
MAX_PLAYER_SPEED = 3
SCORE = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -MAX_PLAYER_SPEED)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, MAX_PLAYER_SPEED)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-MAX_PLAYER_SPEED, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(MAX_PLAYER_SPEED, 0)

        # limit to screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface(size=(20, 10))
        self.surf.fill(color=(255,255,255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 2)
    
    # move the sprite based on speed
    # remove the sprite when it passes the left edge of the screen
    def update(self):
        global SCORE
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            SCORE += 1
            self.kill()



player1 = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
running = True

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)


while running:
    for event in pygame.event.get():
        # Quitting
        if event.type == KEYDOWN:
            print(event.key)
            if event.key == K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    screen.fill((0, 0, 0))  # white

    pressed_keys = pygame.key.get_pressed()
    player1.update(pressed_keys)



    # screen.blit(player1.surf, player1.rect)
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player1, enemies):
        player1.kill()
        print(f"You died :( - Your score: {SCORE}")
        running = False

    enemies.update()

    pygame.display.flip()


pygame.quit()
