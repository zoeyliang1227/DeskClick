import pyautogui
import time
import random
import threading

from threading import Lock
# for img import detect_arrow_sequence

def combined_keys():
    """將兩個功能合併到一個線程中執行"""
    print("使用合併模式執行...")
    
    # 初始按鍵
    pyautogui.press('1')
    print('初始 1')
    
    last_periodic_time = time.time()
    next_periodic_interval = random.randint(10, 60)
    
    while True:
        current_time = time.time()
        
        # 檢查是否該執行定期按鍵
        if current_time - last_periodic_time >= next_periodic_interval:
            print("\n開始定期按鍵序列...")
            
            # 執行定期按鍵序列
            direction = random.choice(['left', 'right'])
            presses = random.randint(1, 10)
            print(f"隨機選擇: {direction}鍵，按 {presses} 次")
            
            for _ in range(presses):
                pyautogui.press(direction)
                print(direction)
                time.sleep(0.05)
                pyautogui.press('c')
                print('c')
                time.sleep(random.uniform(0.1, 0.3))
            
            # Z鍵
            if random.choice([True, False]):
                pyautogui.press('z')
                print('z')
                time.sleep(random.uniform(0.1, 0.3))
            
            # 數字1
            pyautogui.press('1')
            print('1')
            
            # 更新時間
            last_periodic_time = current_time
            next_periodic_interval = random.randint(10, 60)
            print(f"定期按鍵完成，下次將在 {next_periodic_interval} 秒後執行\n" + "-"*30)
        
        # 執行空白鍵
        pyautogui.keyDown('space')
        time.sleep(random.uniform(0.1, 0.3))
        pyautogui.keyUp('space')
        time.sleep(random.uniform(0.1, 0.3))

if __name__ == '__main__':
    print("開始執行，請切到目標視窗...")
    time.sleep(5)
    
    threading.Thread(target=combined_keys, daemon=True).start()
    
    # 主線程保持運行
    while True:
        time.sleep(1)