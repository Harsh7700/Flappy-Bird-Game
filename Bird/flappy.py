# Importing the libraries
import pygame                                                            # Library for game development
import sys                                                               # System-specific parameters and functions
import time                                                              # For time-related functions
import random                                                            # For generating random numbers

# Initializing pygame
pygame.init()

# Setting the Frames Per Second (FPS)
clock = pygame.time.Clock()

# Function to draw the moving floor
def draw_floor():
    screen.blit(floor_img, (floor_x, 520))                              # Draw the first floor image
    screen.blit(floor_img, (floor_x + 448, 520))                        # Draw the second floor image for seamless movement

# Function to create pipes with random heights
def create_pipes():
    pipe_y = random.choice(pipe_height)                                 # Randomly choose a height for the pipes
    top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 300))         # Create the top pipe
    bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))               # Create the bottom pipe
    return top_pipe, bottom_pipe                                        # Return the pair of pipes

# Function to animate pipes and check for collisions
def pipe_animation():
    global game_over, score_time                                                # Access global variables for game state and scoring
    for pipe in pipes:                                                          # Loop through all pipes
        if pipe.top < 0:                                                        # If the pipe is a top pipe
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)         # Flip the pipe image
            screen.blit(flipped_pipe, pipe)                                     # Draw the flipped pipe
        else:
            screen.blit(pipe_img, pipe)                                         # Draw the bottom pipe

        pipe.centerx -= 3                                                       # Move the pipes to the left
        if pipe.right < 0:                                                      # If the pipe moves out of the screen
            pipes.remove(pipe)                                                  # Remove the pipe from the list

        if bird_rect.colliderect(pipe):                                         # Check for collision with the bird
            game_over = True                                                    # Set game over state to True

# Function to display the score
def draw_score(game_state):
    if game_state == "game_on":                                                 # When the game is running
        score_text = score_font.render(str(score), True, (255, 255, 255))       # Render the current score
        score_rect = score_text.get_rect(center=(width // 2, 66))               # Position the score at the top center
        screen.blit(score_text, score_rect)                                     # Draw the score on the screen
    elif game_state == "game_over":                                                # When the game is over
        score_text = score_font.render(f" Score: {score}", True, (255, 255, 255))  # Render the final score
        score_rect = score_text.get_rect(center=(width // 2, 66))                  # Position the final score
        screen.blit(score_text, score_rect)                                        # Draw the final score

        high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))  # Render the high score
        high_score_rect = high_score_text.get_rect(center=(width // 2, 506))       # Position the high score
        screen.blit(high_score_text, high_score_rect)                              # Draw the high score

# Function to update the score
def score_update():
    global score, score_time, high_score                                           # Access global variables
    if pipes:                                                                      # If there are pipes on the screen
        for pipe in pipes:                                                         # Loop through all pipes
            if 65 < pipe.centerx < 69 and score_time:                              # Check if bird crosses a pipe
                score += 1                                                         # Increment the score
                score_time = False                                                 # Prevent multiple increments for the same pipe
            if pipe.left <= 0:                                                     # Reset score_time when pipe moves off-screen
                score_time = True

    if score > high_score:                                                         # Update high score if the current score is higher
        high_score = score

# Game window dimensions
width, height = 350, 622
clock = pygame.time.Clock()                                                        # Create a clock object to control FPS
screen = pygame.display.set_mode((width, height))                                  # Set up the game screen
pygame.display.set_caption("Flappy Bird")                                          # Set the title of the game window

# Load background and floor images
back_img = pygame.image.load("img_46.png")                                         # Background image
floor_img = pygame.image.load("img_50.png")                                        # Floor image
floor_x = 0                                                                        # Initial position of the floor

# Load different bird stages
bird_up = pygame.image.load("img_47.png")                                          # Bird with wings up
bird_down = pygame.image.load("img_48.png")                                        # Bird with wings down
bird_mid = pygame.image.load("img_49.png")                                         # Bird with wings mid
birds = [bird_up, bird_mid, bird_down]                                             # List of bird stages for animation
bird_index = 0                                                                     # Current bird stage index
bird_flap = pygame.USEREVENT                                                       # Custom event for bird flap animation
pygame.time.set_timer(bird_flap, 200)                                              # Set a timer to trigger the event every 200 ms
bird_img = birds[bird_index]                                                       # Set initial bird image
bird_rect = bird_img.get_rect(center=(67, 622 // 2))                               # Position the bird at the center
bird_movement = 0                                                                  # Initial bird movement
gravity = 0.17                                                                     # Gravity effect on bird

# Load pipe image and set possible pipe heights
pipe_img = pygame.image.load("greenpipe.png")                                      # Pipe image
pipe_height = [400, 350, 533, 490]                                                 # List of possible pipe heights

# Create list to store pipes
pipes = []                                                                         # List to store pipes
create_pipe = pygame.USEREVENT + 1                                                 # Custom event for creating pipes
pygame.time.set_timer(create_pipe, 1200)                                           # Set a timer to trigger the event every 1200 ms

# Load game over image
game_over = False                                                                  # Game state
over_img = pygame.image.load("img_45.png").convert_alpha()                         # Game over image
over_rect = over_img.get_rect(center=(width // 2, height // 2))                    # Position of the game over image

# Initialize score-related variables
score = 0                                                                          # Current score
high_score = 0                                                                     # High score
score_time = True                                                                  # Flag to track scoring
score_font = pygame.font.Font("freesansbold.ttf", 27)                              # Font for displaying score

# Game loop
running = True
while running:
    clock.tick(120)                                                                # Set the game loop to run at 120 FPS

    # Handle game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                              # Quit event
            running = False
            sys.exit()                                                             # Exit the program

        if event.type == pygame.KEYDOWN:                                           # Key press event
            if event.key == pygame.K_SPACE and not game_over:                      # Space key pressed during gameplay
                bird_movement = 0                                                  # Reset bird movement
                bird_movement = -7                                                 # Make the bird jump

            if event.key == pygame.K_SPACE and game_over:                          # Space key pressed after game over
                game_over = False                                                  # Reset game over state
                pipes = []  # Clear pipes
                bird_movement = 0                                                  # Reset bird movement
                bird_rect = bird_img.get_rect(center=(67, 622 // 2))               # Reset bird position
                score_time = True                                                  # Reset scoring flag
                score = 0                                                          # Reset score

        if event.type == bird_flap:                                                # Custom event for bird flap animation
            bird_index += 1                                                        # Move to the next bird stage
            if bird_index > 2:                                                     # Reset index if it exceeds the last stage
                bird_index = 0
            bird_img = birds[bird_index]                                           # Update the bird image
            bird_rect = bird_up.get_rect(center=bird_rect.center)                  # Maintain the bird position

        if event.type == create_pipe:                                              # Custom event for creating pipes
            pipes.extend(create_pipes())                                           # Add new pipes to the list

    screen.blit(floor_img, (floor_x, 550))                                         # Draw the floor
    screen.blit(back_img, (0, 0))                                                  # Draw the background

    # Check game state
    if not game_over:                                                              # During gameplay
        bird_movement += gravity                                                   # Apply gravity
        bird_rect.centery += bird_movement                                         # Move the bird vertically
        rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)  # Rotate bird based on movement

        if bird_rect.top < 5 or bird_rect.bottom >= 550:                           # Check if bird hits the top or bottom
            game_over = True                                                       # Set game over state

        screen.blit(rotated_bird, bird_rect)                                       # Draw the rotated bird
        pipe_animation()                                                           # Animate pipes
        score_update()                                                             # Update the score
        draw_score("game_on")                                                      # Display the current score
    elif game_over:                                                                # After game over
        screen.blit(over_img, over_rect)                                           # Display game over image
        draw_score("game_over")                                                    # Display final and high scores

    floor_x -= 1                                                                   # Move the floor to the left
    if floor_x < -448:                                                             # Reset floor position for seamless movement
        floor_x = 0

    draw_floor()                                                                   # Draw the moving floor
    pygame.display.update()                                                        # Update the display

# Quit pygame and exit
pygame.quit()
sys.exit()
