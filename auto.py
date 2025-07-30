import pyautogui
import time
import random
import threading


def hold_space():
    while True:
        pyautogui.keyDown('space')
        time.sleep(0.1)
        pyautogui.keyUp('space')
        time.sleep(0.1)  # 按住與釋放之間加點間隔

def periodic_keys():
    while True:
        time.sleep(180)  # 每 3 分鐘
        for _ in range(random.randint(1, 5)):
            pyautogui.press('left')
            time.sleep(0.2)
        for _ in range(random.randint(1, 5)):
            pyautogui.press('right')
            time.sleep(0.2)
        pyautogui.press('1')  # 主鍵盤的數字 1

if __name__ == '__main__':
    print("開始執行，請切到目標視窗...")
    time.sleep(5)

    # 兩個功能都放到 thread 中執行
    threading.Thread(target=hold_space, daemon=True).start()
    threading.Thread(target=periodic_keys, daemon=True).start()

    # 主線程 idle，避免程式跑完自動結束
    while True:
        time.sleep(1)