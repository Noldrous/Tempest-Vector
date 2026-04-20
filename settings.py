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
print(f"Assets path: {BASE_IMG_PATH}")
print(f"Base path: {BASE_PATH}")

def load_image(path):
    img = pygame.image.load(os.path.join(BASE_IMG_PATH, path)).convert()
    img.set_colorkey((0,0,0))
    return img

def load_image_alpha(path):
    img = pygame.image.load(os.path.join(BASE_IMG_PATH, path)).convert_alpha()
    return img

def load_images(path):
    images = []
    folder = os.path.join(BASE_IMG_PATH, path)
    for img_name in sorted(os.listdir(folder)):
        images.append(load_image(os.path.join(path, img_name)))
    return images