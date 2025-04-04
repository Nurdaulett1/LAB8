import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up game window
width, height = 500, 500         # Window size
cell_size = 10                   # Size of each square (snake block and food)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SNAKE")

# Define colors
black = (0, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Initial snake position and body segments
snake_pos = [100, 100]                            # Head of the snake
snake_body = [[100, 100], [90, 100], [80, 100]]   # Body follows head

# Load and scale images
snake_img = pygame.image.load('snake.jpg').convert_alpha()
snake_img = pygame.transform.scale(snake_img, (cell_size, cell_size))

apple_img = pygame.image.load('apple.png').convert_alpha()
apple_img = pygame.transform.scale(apple_img, (cell_size, cell_size))

# Font for score and level
font = pygame.font.SysFont("Verdana", 20)

# Function to place food at a random position (not on the snake)
def generate_food():
    while True:
        x = random.randint(0, (width - cell_size) // cell_size) * cell_size
        y = random.randint(0, (height - cell_size) // cell_size) * cell_size
        if [x, y] not in snake_body:
            return pygame.Rect(x, y, cell_size, cell_size)

# Generate the first apple
apple_rect = generate_food()

# Direction handling
direction = 'RIGHT'    # Current direction
change_to = direction  # Next direction to switch to

# Game speed controller
clock = pygame.time.Clock()

# Score and level system
score = 0
level = 1
speed = 10             # Initial speed (frames per second)

# Game loop control
Running = True

# Main game loop
while Running:
    # Check for user inputs (keyboard or exit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Change direction but prevent 180-degree turn
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'

    # Apply the new direction
    direction = change_to

    # Update snake head position
    if direction == 'UP':
        snake_pos[1] -= cell_size
    elif direction == 'DOWN':
        snake_pos[1] += cell_size
    elif direction == 'RIGHT':
        snake_pos[0] += cell_size
    elif direction == 'LEFT':
        snake_pos[0] -= cell_size

    # Make snake reappear on the opposite side (teleport through walls)
    snake_pos[0] %= width
    snake_pos[1] %= height

    # Add new position to the front of the body (snake moves forward)
    snake_body.insert(0, list(snake_pos))

    # Check for collision with apple
    if pygame.Rect(snake_pos[0], snake_pos[1], cell_size, cell_size).colliderect(apple_rect):
        score += 1
        # Increase level and speed every 4 apples
        if score % 4 == 0:
            level += 1
            speed += 2
        apple_rect = generate_food()  # Place new apple
    else:
        snake_body.pop()  # Remove tail unless apple eaten

    # Draw everything
    screen.fill(black)  # Clear screen
    screen.blit(apple_img, apple_rect.topleft)  # Draw apple

    # Draw the snake block by block
    for block in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], cell_size, cell_size))

    # Display score and level
    score_text = font.render(f"Score: {score}", True, white)
    level_text = font.render(f"Level: {level}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (400, 10))

    # Refresh the screen
    pygame.display.flip()
    clock.tick(speed)  # Control game speed based on current level
