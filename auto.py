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
        time.sleep(300)  # 每 5 分鐘
        for _ in range(random.randint(1, 5)):
            pyautogui.press('left')
            time.sleep(0.2)
        for _ in range(random.randint(1, 5)):
            pyautogui.press('right')
            time.sleep(0.2)
        pyautogui.press('1')  # 主鍵盤的數字 1

if __name__ == '__main__':
    print("開始執行，請切到目標視窗...")
    time.sleep(5)  # 給你切換視窗的時間

    # 用 thread 分開執行持續按空白 和 定時按其他鍵
    threading.Thread(target=hold_space, daemon=True).start()
    periodic_keys()  # 主線程執行定時動作