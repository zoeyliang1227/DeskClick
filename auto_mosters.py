import os
import time
import random
import threading
import ctypes
import cv2
import numpy as np
import win32api
import win32con
import time 

from key_codes import VK_CODES
from PIL import Image
from get_img import load_monster_templates
from screen import grab_screen_and_save
from button import send_key, send_combo_keys

threshold = 0.85
space_1 = 1
space_2 = 5
run_times = 4
buff_key = 1

def periodic_keys_loop(self):
    templates = load_monster_templates('monster')
    cycle_count = 0
    while self.running:
        time_wait = random.uniform(0.7, 1.3)
        wait_time = random.randint(space_1, space_2)
        while self.paused:
            pause_state(self)

        cycle_count += 1
        print(f"[週期 {cycle_count}] 等待 {wait_time} 秒...")
        # 分段等待，這樣可以及時響應停止信號
        for i in range(wait_time):
            time.sleep(time_wait)
            # 每10秒顯示一次進度
            if (i + 1) % 10 == 0:
                remaining = wait_time - i - 1
                print(f"   還有 {remaining} 秒...")
        time.sleep(time_wait)
        print(f"[週期 {cycle_count}] 開始按鍵序列...")
        screen_gray = grab_screen_and_save()
        # img_rgb = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)  # 先轉成 RGB
        # pil_img = Image.fromarray(img_rgb)
        # pil_img.show()
        find_and_attack(self, screen_gray, templates)
        time.sleep(0.5)  # 半秒掃一次螢幕
        break

def find_and_attack(self, screen_gray, templates):
    for template in templates:
        if gray(screen_gray) == gray(template):     # 判斷是否都是灰階圖片
            res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        
        # print(f"最大相似度: {res.max()}")
        loc = np.where(res >= res.max())
        w, h = template.shape[1], template.shape[0]
        for pt in zip(*loc[::-1]):
            print(f"找到怪物在 {pt}，準備攻擊")
            attack_at_position(self, pt, screen_gray.shape[1], run_times, buff_key)
            break  # 找到一個先攻擊再說

def attack_at_position(self, pt, screen_width, run_times, buff_key):
    x = pt[0]
    # 判斷怪物相對於螢幕中心位置，決定移動方向
    center_x = screen_width // 2
    if x < center_x:
        direction = 'left'

    else:
        direction = 'right'

    print(f"怪物在螢幕{x}，角色向 {direction} 移動並攻擊")

    # 先用方向鍵「移動」角色（這裡假設只按1次方向鍵移動到怪物附近）
    success = send_key(self, direction)
    print(f"按 {direction} 鍵移動 -> {'✓' if success else '✗'}")
    time.sleep(0.5)  # 等待角色移動

    # 執行鍵盤攻擊序列
    attack_by_keyboard(self, direction, run_times, buff_key)

def attack_by_keyboard(self, direction, run_times, buff_key):
    print(f"開始用鍵盤攻擊，方向: {direction}, 攻擊次數: {run_times}, buff: {buff_key}")

    # 按左右方向鍵 + c 組合鍵攻擊
    presses = random.randint(1, run_times)
    for i in range(presses):
        success = send_combo_keys(self, direction, 'c')
        print(f"  {i+1}. {direction} + c -> {'✓' if success else '✗'}")
        time.sleep(random.uniform(0.7, 1.3))

    # 隨機按 z 或跳過
    if random.choice([True, False]):
        result3 = send_key(self, 'z')
        print(f"  z -> {'✓' if result3 else '✗'}")
        time.sleep(random.uniform(0.7, 1.3))
    else:
        print("  跳過 z 鍵")

    # 按 buff key (1 到 buff_key)
    for k in range(1, buff_key+1):
        result4 = send_key(self, str(k))
        print(f"  buff {k} -> {'✓' if result4 else '✗'}")
        time.sleep(random.uniform(0.7, 1.3))

    print("攻擊完成\n" + "-"*40)


def gray(img):
    if len(img.shape) == 2:
        # print("灰階圖片")
        return True

    elif len(img.shape) == 3 and img.shape[2] == 3:
        # print("彩色圖片")
        return False

    else:
        print("其他格式")

# if __name__ == "__main__":
#     periodic_keys_loop(self)