import pygame
import random
import os
import customtkinter as ctk

# Define game variables
WIDTH, HEIGHT = 1600, 900
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 5
BALL_INITIAL_SPEED_X = 3
BALL_INITIAL_SPEED_Y = 3
SCORE_FONT = None
START_FONT = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define classes
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed_y = 0

    def move(self):
        self.rect.y += self.speed_y
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PADDLE_HEIGHT))

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)

    def center_paddle(self):
        self.rect.y = HEIGHT // 2 - PADDLE_HEIGHT // 2


class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.speed_x = BALL_INITIAL_SPEED_X
        self.speed_y = BALL_INITIAL_SPEED_Y
        self.speed_increase_factor = 0

    def move(self):
        self.rect.x += self.direction_x * (self.speed_x + self.speed_increase_factor)
        self.rect.y += self.direction_y * (self.speed_y + self.speed_increase_factor)

    def draw(self):
        pygame.draw.ellipse(WIN, WHITE, self.rect)

    def change_direction_y(self):
        self.direction_y *= -1

    def change_direction_x(self):
        self.direction_x *= -1

# AI Player class
class AIPlayer:
    def __init__(self, paddle, ball, difficulty):
        self.paddle = paddle
        self.ball = ball

    def move(self):
        # Simple AI logic: move paddle towards the ball's y-coordinate
        target_y = self.ball.rect.centery

        if target_y < self.paddle.rect.y + PADDLE_HEIGHT // 2:
            self.paddle.speed_y = -PADDLE_SPEED  # Move paddle up
        elif target_y > self.paddle.rect.y + PADDLE_HEIGHT // 2:
            self.paddle.speed_y = PADDLE_SPEED   # Move paddle down
        else:
            self.paddle.speed_y = 0              # Stop paddle

# Helpful Message for the Players
def draw_help_message():
    font = pygame.font.Font(None, 36)
    help_message = [
        "Player 1: W - Move Up, S - Move Down",
        "Player 2: UP - Move Up, DOWN - Move Down",
        "Press SPACE to start",
        ""
    ]
    y_offset = HEIGHT - (40 * len(help_message))
    for line in help_message:
        text = font.render(line, 1, WHITE)
        WIN.blit(text, (5, y_offset))
        y_offset += 40

# Function to handle collisions
def check_collision(ball, paddles, score):
    for paddle in paddles:
        if ball.rect.colliderect(paddle.rect):
            offset = (ball.rect.centery - paddle.rect.centery) / (PADDLE_HEIGHT / 2)
            
            # Adjust ball direction based on collision point on paddle
            ball.change_direction_x()
            ball.direction_y = offset
            
            # Increase ball speed after each hit, cap at maximum speed
            ball.speed_increase_factor = min(10, ball.speed_increase_factor + 1)

            # Determine if paddle is moving towards or against ball's direction
            if (paddle.speed_y < 0 and ball.direction_y < 0) or (paddle.speed_y > 0 and ball.direction_y > 0):
                ball.speed_increase_factor += 1  # Increase ball speed
            elif (paddle.speed_y < 0 and ball.direction_y > 0) or (paddle.speed_y > 0 and ball.direction_y < 0):
                ball.speed_increase_factor = max(0, ball.speed_increase_factor - 1)  # Decrease ball speed

            paddle_sound.play()  # Play paddle hit sound
            break

    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball.change_direction_y()
        paddle_sound.play()  # Play paddle hit sound

    if ball.rect.left <= 0:
        score[1] += 1
        reset_ball(ball)
        score_sound.play()  # Play score sound
        return True

    if ball.rect.right >= WIDTH:
        score[0] += 1
        reset_ball(ball)
        score_sound.play()  # Play score sound
        return True

    return False

def reset_ball(ball):
    ball.rect.x = WIDTH // 2 - BALL_SIZE // 2
    ball.rect.y = HEIGHT // 2 - BALL_SIZE // 2
    ball.direction_x = random.choice([-1, 1])
    ball.direction_y = random.choice([-1, 1])
    ball.speed_increase_factor = 0  # Reset ball speed increase

# Function to place Help Message
def draw_instructions():
    font = pygame.font.Font(None, 36)
    text = font.render("Press H for controls", True, WHITE)
    WIN.blit(text, (5, HEIGHT - 40))  # Place near bottom left corner

def redraw_window(paddles, ball, score, game_started, start_text, start_rect, show_help):
    WIN.fill(BLACK)
    for y in range(0, HEIGHT, 20):  # Draw dashed line
        pygame.draw.line(WIN, WHITE, (WIDTH // 2, y), (WIDTH // 2, y + 10), 2)
    for paddle in paddles:
        paddle.draw()
    ball.draw()
    score_text_1 = SCORE_FONT.render(str(score[0]), True, WHITE)
    score_text_2 = SCORE_FONT.render(str(score[1]), True, WHITE)
    WIN.blit(score_text_1, (WIDTH // 2 - score_text_1.get_width() - 50, 20))
    WIN.blit(score_text_2, (WIDTH // 2 + 50, 20))
    if not game_started:
        pygame.draw.rect(WIN, BLACK, start_rect)
        WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
    draw_instructions()
    if show_help:
        draw_help_message()  # Call the function to draw the help message
    pygame.display.update()

# Function to start the game
def start_game(player_mode, ai_difficulty):
    global WIN, SCORE_FONT, START_FONT, wall_paddle_sound, score_sound, paddle_sound

    # Initialize Pygame and set up the screen
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PONG-OFFLINE")

    # Load fonts
    SCORE_FONT = pygame.font.Font(None, 64)
    START_FONT = pygame.font.Font(None, 48)

    # Load sounds
    audio_path = os.path.join(os.path.dirname(__file__), "AUDIO")
    wall_paddle_sound = pygame.mixer.Sound(os.path.join(audio_path, "PADDLE_WALL_COLLISION_SOUND.mp3"))
    score_sound = pygame.mixer.Sound(os.path.join(audio_path, "SCORE_SOUND.mp3"))
    paddle_sound = pygame.mixer.Sound(os.path.join(audio_path, "PADDLE_WALL_COLLISION_SOUND.mp3"))

    # Load background music
    background_music = os.path.join(audio_path, "COOL_BACKROUND_MUSIC.mp3")
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.set_volume(0.75)  # Set the background music volume to 75%
    pygame.mixer.music.play(-1)  # Play music in a loop

    clock = pygame.time.Clock()
    paddles = [Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2), Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)]
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)
    ai_player = AIPlayer(paddles[1], ball, ai_difficulty)  # AI controls the second paddle if AI mode is selected
    score = [0, 0]

    running = True
    game_started = False
    show_help = False
    start_text = START_FONT.render("Press SPACE to Start", 1, WHITE)
    start_rect = pygame.Rect((WIDTH - start_text.get_width()) // 2 - 10, (HEIGHT - start_text.get_height()) // 2 - 10, start_text.get_width() + 20, start_text.get_height() + 20)
    
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_started:
                        game_started = True
                        for paddle in paddles:
                            paddle.center_paddle()
                        ball.rect.x = WIDTH // 2 - BALL_SIZE // 2
                        ball.rect.y = HEIGHT // 2 - BALL_SIZE // 2
                        ball.direction_x = random.choice([-1, 1])
                        ball.direction_y = random.choice([-1, 1])
                        ball.speed_increase_factor = 0  # Reset speed increase factor
                if event.key == pygame.K_h:
                    show_help = not show_help  # Toggle help message
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    paddles[0].speed_y = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    paddles[1].speed_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddles[0].rect.top > 0:
            paddles[0].speed_y = -PADDLE_SPEED
        elif keys[pygame.K_s] and paddles[0].rect.bottom < HEIGHT:
            paddles[0].speed_y = PADDLE_SPEED
        else:
            paddles[0].speed_y = 0

        if player_mode == "2P":
            if keys[pygame.K_UP] and paddles[1].rect.top > 0:
                paddles[1].speed_y = -PADDLE_SPEED
            elif keys[pygame.K_DOWN] and paddles[1].rect.bottom < HEIGHT:
                paddles[1].speed_y = PADDLE_SPEED
            else:
                paddles[1].speed_y = 0

        if game_started:
            ball.move()
            if check_collision(ball, paddles, score):
                game_started = False  # Stop the game when a point is scored
            if player_mode == "1P":
                ai_player.move()  # AI move only in single-player mode

            for paddle in paddles:
                paddle.move()

        redraw_window(paddles, ball, score, game_started, start_text, start_rect, show_help)

    pygame.quit()

# Function to show the selection screen
def show_selection_screen():
    root = ctk.CTk()
    root.title("PONG-OFFLINE: Select Mode")
    root.geometry("350x410")  # Set the window size
    root.resizable(False, False)  # Disable resizing

    def start_singleplayer():
        root.destroy()
        start_game("1P", ai_difficulty_var.get())

    def start_multiplayer():
        root.destroy()
        start_game("2P", None)

    ctk.CTkLabel(root, text="Play with Friends :-),\nor alone on your own :-(", font=("Arial", 20)).pack(pady=20)
    
    ctk.CTkButton(root, text="Single Player (vs AI)", command=start_singleplayer, width=250, height=75).pack(pady=10)
    ctk.CTkButton(root, text="Local-Multiplayer", command=start_multiplayer, width=250, height=75).pack(pady=10)
    
    ctk.CTkLabel(root, text="Select AI Difficulty", font=("Arial", 16)).pack(pady=10)
    
    ai_difficulty_var = ctk.IntVar(value=1)
    ctk.CTkRadioButton(root, text="Easy", variable=ai_difficulty_var, value=1).pack()
    ctk.CTkRadioButton(root, text="Medium", variable=ai_difficulty_var, value=2).pack()
    ctk.CTkRadioButton(root, text="Hard", variable=ai_difficulty_var, value=3).pack()

    root.mainloop()

if __name__ == "__main__":
    show_selection_screen()
