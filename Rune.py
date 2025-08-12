import os
import cv2
import numpy as np
import pyautogui
import time

from PIL import Image  # 或者是你用的影像處理函式庫

# 圖片模板
teleport_template = cv2.imread('Teleport.png', 0)
arrow_templates = {
    'up': cv2.imread('arrow_up.png', 0),
    'down': cv2.imread('arrow_down.png', 0),
    'left': cv2.imread('arrow_left.png', 0),
    'right': cv2.imread('arrow_right.png', 0)
}

# 基本參數
threshold = 0.8
arrow_area = (500, 800, 1000, 900)  # (left, top, right, bottom)：你要依照實際遊戲座標調整

def screen_gray():
    screen = ImageGrab.grab()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2GRAY)
    return screen

def find_template(template):
    gray_img = screen_gray()
    res = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        return pt  # 第一個匹配點
    return None

def wait_for_arrow_ui(timeout=10):
    print("⏳ 等待箭頭 UI 出現...")
    start = time.time()
    while time.time() - start < timeout:
        partial = ImageGrab.grab(bbox=arrow_area).convert('L')  # 裁切方向區域
        img = np.array(partial)
        for name, tmpl in arrow_templates.items():
            res = cv2.matchTemplate(img, tmpl, cv2.TM_CCOEFF_NORMED)
            if (res >= threshold).any():
                print("🟢 偵測到箭頭 UI")
                return True
        time.sleep(0.2)
    print("❌ 等待逾時，未出現箭頭")
    return False

def detect_arrow_sequence():
    partial = ImageGrab.grab(bbox=arrow_area).convert('L')
    img = np.array(partial)

    h, w = img.shape
    width_per_arrow = w // 4  # 分成四格
    sequence = []

    for i in range(4):
        segment = img[0:h, i*width_per_arrow:(i+1)*width_per_arrow]
        best_match = None
        best_val = 0

        for name, tmpl in arrow_templates.items():
            res = cv2.matchTemplate(segment, tmpl, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > best_val and max_val >= threshold:
                best_match = name
                best_val = max_val

        if best_match:
            sequence.append(best_match)
    return sequence

def press_arrow_sequence(seq):
    print(f"🔽 開始按方向鍵序列：{seq}")
    for direction in seq:
        pyautogui.press(direction)
        time.sleep(1)

    # 主迴圈
    while True:
        location = find_template(teleport_template)
        if location:
            print("📍 偵測到傳送裝置")
            pyautogui.press('up')  # 啟動傳送裝置
            time.sleep(1)
    
            if wait_for_arrow_ui():
                seq = detect_arrow_sequence()
                if seq:
                    press_arrow_sequence(seq)
                    print("✅ 完成一組傳送指令")
                else:
                    print("⚠️ 沒辨識到箭頭序列")
            else:
                print("⚠️ 箭頭 UI 沒出現")
    
            time.sleep(5)  # 傳送完等一下再開始下一輪
        else:
            time.sleep(1)
