import pygame, sys
from pygame.locals import *
import random, time

# Initialize Pygame
pygame.init()

# Set up FPS (frames per second) and the clock to control game speed
FPS = 60
FramePerSec = pygame.time.Clock()

# Define colors (RGB)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Initial game values
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0

# Load fonts for displaying text
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load("AnimatedStreet.png")

# Create the game window
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Enemy car class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")  # Load enemy image
        self.rect = self.image.get_rect()
        # Place enemy randomly at the top of the screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        # Move enemy downward
        self.rect.move_ip(0, SPEED)
        # If the enemy goes off the screen, reset its position and increase score
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")  # Load player image
        self.rect = self.image.get_rect()
        # Start the player in the bottom center
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Move player left and right within screen bounds
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


# Create game objects
P1 = Player()
E1 = Enemy()


# Group sprites for easier management
enemies = pygame.sprite.Group()
enemies.add(E1)



all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)


# Custom event to increase enemy speed over time
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Every second

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Increase speed every second
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background image
    DISPLAYSURF.blit(background, (0, 0))

    # Draw score and coin count at the top
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10))

    # Update and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Check collision between player and enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        # Stop game after crash
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()


    pygame.display.update()
    FramePerSec.tick(FPS)
