import pygame
import random
 
# Initialize Pygame
pygame.init()
 
# Get the display info
infoObject = pygame.display.Info()
 
# Set up the screen in borderless window mode
WIN = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.NOFRAME)
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
 
pygame.display.set_caption("PONG")

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