import pyautogui
import time
import random
import threading

# for img import detect_arrow_sequence


def hold_space():
    while True:
        pyautogui.keyDown('space')
        time.sleep(random.uniform(0.1, 0.5))
        pyautogui.keyUp('space')
        time.sleep(random.uniform(0.1, 0.5))  # 按住與釋放之間加點間隔

def periodic_keys():
    pyautogui.press('1')
    print('1')
    time.sleep(random.uniform(0.1, 0.3))

    while True:
        wait_time = random.randint(60, 180)
        print(f"等待 {wait_time} 秒...")
        time.sleep(wait_time)

        print("開始按鍵序列...")
        # 隨機選擇左鍵或右鍵，按1～10次
        direction = random.choice(['left', 'right'])
        presses = random.randint(1, 10)
        print(f"隨機選擇: {direction}鍵，按 {presses} 次")
        
        for _ in range(presses):
            pyautogui.press(direction)
            print(direction)
            pyautogui.press('c')
            print('c')
            time.sleep(random.uniform(0.1, 0.5))
        
        # 隨機決定是否按下 Z
        time.sleep(random.uniform(0.1, 0.3))
        if random.choice([True, False]):
            pyautogui.press('z')
            print('z')
            time.sleep(random.uniform(0.1, 0.3))
        
        # 按一下數字 1
        pyautogui.press('1')
        print('1')
        time.sleep(random.uniform(0.1, 0.3))
        
        print("本輪按鍵完成\n" + "-"*30)

if __name__ == '__main__':
    print("開始執行，請切到目標視窗...")
    time.sleep(5)

    # 兩個功能都放到 thread 中執行
    threading.Thread(target=hold_space, daemon=True).start()
    threading.Thread(target=periodic_keys, daemon=True).start()

    # 主線程 idle，避免程式跑完自動結束
    while True:
        time.sleep(1)