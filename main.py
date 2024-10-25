import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load background image
background_image = pygame.image.load("images/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load bird image
bird_image = pygame.image.load("images/bird.png")
bird_image = pygame.transform.scale(bird_image, (40, 30))

# Laod pipe image
pipe_image = pygame.image.load("images/pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (70, 500))

# Bird
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
gravity = 0.5
flap_strength = -10

# Pipe
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 200
pipe_velocity = -2
pipes = []

# Game variables
score = 0
clock = pygame.time.Clock()
flap_cooldown = 0

# Game states
game_state = "ready"
waiting_for_space = False

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

# Button properties
button_width = 200
button_height = 50

# Function to reset the game
def reset_game():
    global bird_y, bird_velocity, pipes, score, flap_cooldown, waiting_for_space
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes.clear()
    score = 0
    flap_cooldown = 0
    waiting_for_space = True
    pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
    pipes.append(
        {
            "top": pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height),
            "bottom": pygame.Rect(
                SCREEN_WIDTH,
                pipe_height + PIPE_GAP,
                PIPE_WIDTH,
                SCREEN_HEIGHT - pipe_height - PIPE_GAP,
            ),
        }
    )

# Function to draw the bird (now with the image)
def draw_bird():
    screen.blit(bird_image, (bird_x, bird_y))

def draw_pipes():
    for pipe in pipes:
        flipped_pipe = pygame.transform.flip(pipe_image, False, True)

        screen.blit(flipped_pipe, (pipe["top"].x, pipe["top"].y + pipe["top"].height - PIPE_HEIGHT))
        screen.blit(pipe_image, (pipe["bottom"].x, pipe["bottom"].y))

# Function to check for collisions
def check_collision():
    bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
    for pipe in pipes:
        top_pipe_rect = pygame.Rect(pipe["top"].x, pipe["top"].y, PIPE_WIDTH, pipe["top"].height)
        bottom_pipe_rect = pygame.Rect(pipe["bottom"].x, pipe["bottom"].y, PIPE_WIDTH, pipe["bottom"].height)
        
        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            return True
    
    if bird_y < 0 or bird_y > SCREEN_HEIGHT - BIRD_HEIGHT:
        return True
    
    return False


# Function to update the pipes
def update_pipes():
    global score
    for pipe in pipes:
        pipe["top"].x += pipe_velocity
        pipe["bottom"].x += pipe_velocity
        if pipe["top"].x + PIPE_WIDTH < 0:
            pipes.remove(pipe)
            score += 1
    if len(pipes) == 0 or pipes[-1]["top"].x < SCREEN_WIDTH - 200:
        pipe_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        pipes.append(
            {
                "top": pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, pipe_height),
                "bottom": pygame.Rect(
                    SCREEN_WIDTH,
                    pipe_height + PIPE_GAP,
                    PIPE_WIDTH,
                    SCREEN_HEIGHT - pipe_height - PIPE_GAP,
                ),
            }
        )

# Function to draw buttons
def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surf = small_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

# Function to check if button is clicked
def is_button_clicked(x, y, width, height, mouse_pos):
    return x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height

# Main game loop
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if game_state == "game_over":
                    game_state = "ready"
                    reset_game()
            elif event.key == pygame.K_SPACE:
                if game_state == "ready": 
                    game_state = "playing"
                    reset_game()
                elif game_state == "playing" and flap_cooldown <= 0:
                    bird_velocity = flap_strength
                    flap_cooldown = 10
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "game_over":
                if is_button_clicked(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 50, button_width, button_height, mouse_pos):
                    game_state = "ready"
                    reset_game()

    if game_state == "playing":
        # Update bird position
        bird_velocity += gravity
        bird_y += bird_velocity

        # Update pipes
        update_pipes()

        # Check for collision
        if check_collision():
            game_state = "game_over"

        # Manage flap cooldown
        if flap_cooldown > 0:
            flap_cooldown -= 1

    # Draw everything
    screen.blit(background_image, (0, 0))

    if game_state == "ready":
        draw_bird()
        instruction_text = small_font.render("Press Space to Flap", True, BLACK)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

    elif game_state == "playing":
        draw_bird()
        draw_pipes()

        # Display the score
        score_text = font.render(f"{score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))

    elif game_state == "game_over":
        # Draw the game over text
        draw_bird()
        draw_pipes()
        game_over_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # Draw the Try Again button
        draw_button("Try Again", SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 50, button_width, button_height, BLUE, WHITE)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
