import pygame
import sys
import math
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
info = pygame.display.Info()

width,height = info.current_w, info.current_h

BASE_PATH = os.path.dirname(__file__)
BASE_IMG_PATH = os.path.join(BASE_PATH, "assets/img")

def load_image_alpha(path):
    img = pygame.image.load(os.path.join(BASE_IMG_PATH, path)).convert_alpha()
    return img