import os
from PIL import Image
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "img")

def load_image(name):
    return Image.open(os.path.join(IMG_DIR, name))

def load_monster_templates(img):
    templates = []
    for f in os.listdir(IMG_DIR):
        if img in f.lower():
            pil_img = load_image(f).convert("RGB")
            open_cv_image = np.array(pil_img)
            template = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            templates.append(template)
    return templates
