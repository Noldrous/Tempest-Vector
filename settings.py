import pygame
import sys
import math
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
info = pygame.display.Info()

width,height = info.current_w, info.current_h