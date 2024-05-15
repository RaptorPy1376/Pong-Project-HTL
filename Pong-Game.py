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