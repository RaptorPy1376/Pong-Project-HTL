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