import os
import cv2
import ctypes
import numpy as np

from PIL import ImageGrab

def grab_screen_and_save():
    screen_monster = grab_dynamic_region(0.5, 1) #截取螢幕中間 50% 範圍
    # screen = ImageGrab.grab()
    # screen = screen.convert("RGB")  # PIL 圖片轉 RGB
    np_screen = np.array(screen_monster)    # 轉 numpy 陣列 (H, W, 3)，格式是 RGB
    screen_bgr = cv2.cvtColor(np_screen, cv2.COLOR_RGB2BGR)  # 轉成 OpenCV BGR 格式
    screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)  # 轉灰階
    check_forder(screen_monster)

    return screen_gray

def get_screen_size():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()  # 避免 DPI 縮放干擾
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height

def grab_dynamic_region(width_ratio, height_ratio):
    screen_w, screen_h = get_screen_size()
    print(f"螢幕解析度：{screen_w} x {screen_h}")
    bbox = (screen_w // 2, 0, screen_w, screen_h)  # 右半邊範圍 (left, top, right, bottom)
    print(f"截圖右半邊範圍: {bbox}")
    return ImageGrab.grab(bbox=bbox)

def check_forder(screen):
    # 確認 screen 資料夾是否存在，沒有就建立
    screen_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screen")
    if not os.path.exists(screen_dir):
        os.makedirs(screen_dir)

    file_path = os.path.join(screen_dir, "monster.png")
    screen.save(file_path)
    print(f"螢幕截圖已存成 {file_path}")