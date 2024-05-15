import pygame
import random
 
# Initialize Pygame
pygame.init()
 
# Get the display info
infoObject = pygame.display.Info()
 
# Set up the screen in borderless window mode
WIN = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.NOFRAME)
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
 
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


# Function to handle collisions with paddles
def check_paddle_collision(ball, paddles):
    for paddle in paddles:
        if ball.rect.colliderect(paddle.rect):
            ball.change_direction_x()
 
 # Function to handle collisions with screen edges
def check_screen_collision(ball):
    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball.change_direction_y()

# Function to redraw the window
def redraw_window(paddles, ball):
    WIN.fill(BLACK)
    for paddle in paddles:
        paddle.draw()
    ball.draw()
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    paddles = [Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2), Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)]
    ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2)
 
    running = True
    while running:
        clock.tick(60)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddles[0].rect.top > 0:
            paddles[0].move_up()
        if keys[pygame.K_s] and paddles[0].rect.bottom < HEIGHT:
            paddles[0].move_down()
        if keys[pygame.K_UP] and paddles[1].rect.top > 0:
            paddles[1].move_up()
        if keys[pygame.K_DOWN] and paddles[1].rect.bottom < HEIGHT:
            paddles[1].move_down()
 
        ball.move()
        check_paddle_collision(ball, paddles)
        check_screen_collision(ball)
        redraw_window(paddles, ball)
 
    pygame.quit()
 
if __name__ == "__main__":
    main()