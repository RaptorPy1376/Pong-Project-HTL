import pygame
import random
import os
import socket
import threading
import sys

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

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 5
BALL_INITIAL_SPEED_X = 3
BALL_INITIAL_SPEED_Y = 3

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

    def move(self):
        self.rect.x += self.direction_x * BALL_INITIAL_SPEED_X
        self.rect.y += self.direction_y * BALL_INITIAL_SPEED_Y

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

# Function to handle collisions with paddles
def check_paddle_collision(ball, paddles):
    for paddle in paddles:
        if ball.rect.colliderect(paddle.rect):
            ball.change_direction_x()

# Function to handle collisions with screen edges
def check_screen_collision(ball, scores):
    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball.change_direction_y()
    if ball.rect.left <= 0:
        scores[1] += 1
        ball.reset_position()
    if ball.rect.right >= WIDTH:
        scores[0] += 1
        ball.reset_position()
 
# Function to redraw the window
def redraw_window(paddles, ball, scores):
    WIN.fill(BLACK)
    for paddle in paddles:
        paddle.draw()
    ball.draw()
    draw_scores(scores)
    pygame.display.update()

# Function to draw scores
def draw_scores(scores):
    font = pygame.font.Font(None, 74)
    text = font.render(str(scores[0]), 1, WHITE)
    WIN.blit(text, (WIDTH // 4, 10))
    text = font.render(str(scores[1]), 1, WHITE)
    WIN.blit(text, (3 * WIDTH // 4, 10))

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5555))  # You can change the port number if needed
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    print("Connection from:", addr)
 
    while True:
        data = f"{ball.rect.x},{ball.rect.y},{ball.direction_x},{ball.direction_y},{paddles[0].rect.y},{scores[0]},{scores[1]}"
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
        ball.rect.x, ball.rect.y, ball.direction_x, ball.direction_y, paddles[0].rect.y, scores[0], scores[1] = map(int, data.split(","))
        send_data = f"{paddles[1].rect.y}"
        client_socket.send(send_data.encode())
 
    client_socket.close()
    
def main(role, server_ip=None):
    global ball, paddles, scores

    clock = pygame.time.Clock()
    paddles = [Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2), Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)]
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)

    scores = [0, 0]

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
        redraw_window(paddles, ball, scores)

if __name__ == "__main__":
    role = input("Choose Role (server/client): ").strip().lower()
    server_ip = None
    if role == "client":
        server_ip = input("Enter Server IP: ").strip()
    main(role, server_ip)
