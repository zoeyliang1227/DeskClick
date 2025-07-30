import pyautogui
import time
import random
import threading


def hold_space():
    while True:
        pyautogui.keyDown('space')
        time.sleep(random.uniform(0.1, 0.5))
        pyautogui.keyUp('space')
        time.sleep(random.uniform(0.1, 0.5))  # 按住與釋放之間加點間隔

def periodic_keys():
    while True:
        time.sleep(random.randint(180, 300))    # 3～5分鐘
        for _ in range(random.randint(1, 10)):
            pyautogui.press('left')
            print('left')
            time.sleep(random.uniform(0.1, 0.5))
        for _ in range(random.randint(1, 10)):
            pyautogui.press('right')
            print('right')
            time.sleep(random.uniform(0.1, 0.5))
        
        # 隨機按下 C 和/或 Z
        if random.choice([True, False]):
            pyautogui.press('c')
            print('c')
            time.sleep(random.uniform(0.1, 0.3))
        if random.choice([True, False]):
            pyautogui.press('z')
            print('z')
            time.sleep(random.uniform(0.1, 0.3))

        # 按一下數字 1（Q 上面那個）
        pyautogui.press('1')
        print('1')
        time.sleep(random.uniform(0.1, 0.3))

if __name__ == '__main__':
    print("開始執行，請切到目標視窗...")
    time.sleep(5)

    # 兩個功能都放到 thread 中執行
    threading.Thread(target=hold_space, daemon=True).start()
    threading.Thread(target=periodic_keys, daemon=True).start()

    # 主線程 idle，避免程式跑完自動結束
    while True:
        time.sleep(1)