import pygame
import random
import os
import socket
import threading
import sys
import math
 
# Initialize Pygame
pygame.init()
 
# Get the display info
infoObject = pygame.display.Info()
 
# Set the window size to 1600x900 (16:9 Aspect Ratio)
WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
 
# Set window caption
pygame.display.set_caption("PONG")
 
# Set window icon
icon_path = os.path.join("icon.png")  # Change this to the path of your icon image
pygame.display.set_icon(pygame.image.load(icon_path))
 
# Load sounds
wall_paddle_sound = pygame.mixer.Sound("paddle_wall_hit.mp3")
score_sound = pygame.mixer.Sound("score.mp3")
background_music = "background_music.mp3"
 
# Load music
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # Play music in a loop
 
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
 
# Game variables
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 6
BALL_INITIAL_SPEED = 5
BALL_MAX_SPEED = 15
SCORE_FONT = pygame.font.Font(None, 64)
 
# Define classes
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
 
    def move_up(self):
        self.rect.y -= PADDLE_SPEED
 
    def move_down(self):
        self.rect.y += PADDLE_SPEED
 
    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)
 
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.speed = BALL_INITIAL_SPEED  # Initial speed
 
    def move(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
 
    def draw(self):
        pygame.draw.ellipse(WIN, WHITE, self.rect)
 
    def change_direction_y(self):
        self.direction_y *= -1
 
    def change_direction_x(self):
        self.direction_x *= -1
 
    def reset_position(self):
        self.rect.x = WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = HEIGHT // 2 - BALL_SIZE // 2
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.speed = BALL_INITIAL_SPEED  # Reset speed to initial speed
 
# Function to handle collisions with paddles
def check_paddle_collision(ball, paddles):
    for paddle in paddles:
        if ball.rect.colliderect(paddle.rect):
            # Calculate the position of the ball relative to the paddle's center
            relative_intersect_y = (paddle.rect.centery - ball.rect.centery) / (paddle.rect.height / 2)
 
            # Define the maximum reflection angle (in radians)
            max_angle = math.radians(60)  # Maximum reflection angle (60 degrees)
 
            # Calculate the reflection angle based on the relative intersection position
            reflection_angle = relative_intersect_y * max_angle
 
            # Invert the reflection angle for paddles on the right side of the screen
            if paddle.rect.x > WIDTH / 2:
                reflection_angle *= -1
 
            # Calculate the new direction based on the reflection angle
            direction_x = math.cos(reflection_angle)
            direction_y = math.sin(reflection_angle)
 
            # Normalize direction to maintain speed consistency
            magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
            ball.direction_x = direction_x / magnitude
            ball.direction_y = direction_y / magnitude
 
            # Make sure the direction points in the correct direction based on the paddle's side
            if paddle.rect.x > WIDTH / 2:
                ball.direction_x *= -1
 
            # Increment ball speed, but cap it at BALL_MAX_SPEED
            ball.speed = min(ball.speed + 0.5, BALL_MAX_SPEED)
 
            # Play the wall/paddle collision sound
            wall_paddle_sound.play()
 
# Function to handle collisions with screen edges
def check_screen_collision(ball, scores):
    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball.change_direction_y()
        wall_paddle_sound.play()  # Play the wall/paddle collision sound
    if ball.rect.left <= 0:
        scores[1] += 1
        ball.reset_position()
        score_sound.play()  # Play the score sound
    if ball.rect.right >= WIDTH:
        scores[0] += 1
        ball.reset_position()
        score_sound.play()  # Play the score sound
 
# Function to redraw the window
def redraw_window(paddles, ball, scores, show_controls):
    WIN.fill(BLACK)
    for y in range(0, HEIGHT, 20):  # Draw dashed line
        pygame.draw.line(WIN, WHITE, (WIDTH // 2, y), (WIDTH // 2, y + 10), 2)
    for paddle in paddles:
        paddle.draw()
    ball.draw()
    scores_text_1 = SCORE_FONT.render(str(scores[0]), 1, WHITE)
    scores_text_2 = SCORE_FONT.render(str(scores[1]), 1, WHITE)
    WIN.blit(scores_text_1, (WIDTH // 2 - scores_text_1.get_width() - 50, 20))
    WIN.blit(scores_text_2, (WIDTH // 2 + 50, 20))
    draw_instructions()
    if show_controls:
        draw_controls()
    pygame.display.update()
 
# Function to draw controls in the bottom left corner
def draw_controls():
    font = pygame.font.Font(None, 36)
    controls = [
        "Player 1 (Server): W - Move Up, S - Move Down",
        "Player 2 (Client): UP - Move Up, DOWN - Move Down",
        "Press ENTER to reset ball position",
        "Press SPACE to reset scores"
    ]
    y_offset = HEIGHT - (47 * len(controls))
    for control in controls:
        text = font.render(control, 1, WHITE)
        WIN.blit(text, (5, y_offset))
        y_offset += 40
 
# Function to draw instructions in the bottom left corner
def draw_instructions():
    font = pygame.font.Font(None, 36)
    text = font.render("Press H for controls", 1, WHITE)
    WIN.blit(text, (5, HEIGHT - 30))  # Place near bottom left corner
 
def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5555))  # You can change the port number if needed
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    print("Connection from:", addr)
 
    while True:
        data = f"{ball.rect.x},{ball.rect.y},{ball.direction_x},{ball.direction_y},{ball.speed},{paddles[0].rect.y},{scores[0]},{scores[1]}"
        conn.send(data.encode())
        recv_data = conn.recv(1024).decode()
        if not recv_data:
            break
        paddles[1].rect.y = int(recv_data)
 
    conn.close()
 
def client_program(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 5555))  # Use the server's IP address
 
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        ball.rect.x, ball.rect.y, ball.direction_x, ball.direction_y, ball.speed, paddles[0].rect.y, scores[0], scores[1] = map(float, data.split(","))
        ball.direction_x = int(ball.direction_x)
        ball.direction_y = int(ball.direction_y)
        ball.speed = float(ball.speed)
        paddles[0].rect.y = int(paddles[0].rect.y)
        scores[0] = int(scores[0])
        scores[1] = int(scores[1])
        send_data = f"{paddles[1].rect.y}"
        client_socket.send(send_data.encode())
 
    client_socket.close()
 
def main(role, server_ip=None):
    global ball, paddles, scores
 
    clock = pygame.time.Clock()
    paddles = [Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2), Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)]
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)
 
    scores = [0, 0]
    show_controls = False  # Variable to track whether to show controls
 
    if role == "server":
        threading.Thread(target=server_program).start()
    elif role == "client":
        threading.Thread(target=client_program, args=(server_ip,)).start()
 
    running = True
    while running:
        clock.tick(60)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()  # Beenden von Pygame
                sys.exit()    # Beenden des Python-Skripts
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ball.reset_position()
                if event.key == pygame.K_SPACE:
                    scores = [0, 0]
                if event.key == pygame.K_h:
                    show_controls = not show_controls  # Toggle control display
 
        keys = pygame.key.get_pressed()
 
        if role == "server":
            if keys[pygame.K_w] and paddles[0].rect.top > 0:
                paddles[0].move_up()
            if keys[pygame.K_s] and paddles[0].rect.bottom < HEIGHT:
                paddles[0].move_down()
        elif role == "client":
            if keys[pygame.K_UP] and paddles[1].rect.top > 0:
                paddles[1].move_up()
            if keys[pygame.K_DOWN] and paddles[1].rect.bottom < HEIGHT:
                paddles[1].move_down()
 
        ball.move()
        check_paddle_collision(ball, paddles)
        check_screen_collision(ball, scores)
        redraw_window(paddles, ball, scores, show_controls)
 
if __name__ == "__main__":
    role = input("Choose Role (server/client): ").strip().lower()
    server_ip = None
    if role == "client":
        server_ip = input("Enter Server IP: ").strip()
    main(role, server_ip)