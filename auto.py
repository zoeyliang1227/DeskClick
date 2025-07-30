import pyautogui
import time
import random
import threading

from threading import Lock
# for img import detect_arrow_sequence

def combined_keys():
    """調試版的合併按鍵功能"""
    print("=== 開始合併按鍵功能 (調試版) ===")
    
    # 初始按鍵 - 加強版
    print("準備按初始 '1' 鍵...")
    try:
        pyautogui.press('1')
        print("✓ 成功執行初始 '1' 鍵")
    except Exception as e:
        print(f"✗ 初始 '1' 鍵失敗: {e}")
    
    time.sleep(2)  # 給更多時間觀察
    
    last_periodic_time = time.time()
    next_periodic_interval = 15  # 縮短到15秒方便測試
    space_counter = 0
    
    print(f"進入主循環，下次定期按鍵將在 {next_periodic_interval} 秒後...")
    
    while True:
        current_time = time.time()
        
        # 檢查是否該執行定期按鍵
        if current_time - last_periodic_time >= next_periodic_interval:
            print("\n🔔 時間到！開始定期按鍵序列...")
            
            try:
                # 執行定期按鍵序列
                direction = random.choice(['left', 'right'])
                presses = random.randint(2, 5)  # 減少次數方便觀察
                print(f"📋 計劃: {direction}鍵 {presses} 次")
                
                for i in range(presses):
                    print(f"  第 {i+1} 次:")
                    print(f"    按 {direction}...")
                    pyautogui.press(direction)
                    time.sleep(0.1)
                    
                    print(f"    按 c...")
                    pyautogui.press('c')
                    time.sleep(0.2)
                
                # Z鍵
                if random.choice([True, False]):
                    print("  按 z...")
                    pyautogui.press('z')
                    time.sleep(0.2)
                else:
                    print("  跳過 z")
                
                # 數字1
                print("  按 1...")
                pyautogui.press('1')
                
                print("✓ 定期按鍵序列完成!")
                
            except Exception as e:
                print(f"✗ 定期按鍵序列出錯: {e}")
            
            # 更新時間
            last_periodic_time = current_time
            next_periodic_interval = random.randint(15, 30)  # 縮短間隔
            print(f"⏰ 下次定期按鍵將在 {next_periodic_interval} 秒後\n" + "-"*50)
        
        # 執行空白鍵
        try:
            pyautogui.keyDown('space')
            time.sleep(random.uniform(0.1, 0.2))
            pyautogui.keyUp('space')
            space_counter += 1
            
            # 每執行50次空白鍵報告一次
            if space_counter % 50 == 0:
                remaining_time = next_periodic_interval - (current_time - last_periodic_time)
                print(f"🔄 空白鍵執行 {space_counter} 次，距下次定期按鍵還有 {remaining_time:.1f} 秒")
                
        except Exception as e:
            print(f"✗ 空白鍵出錯: {e}")
        
        time.sleep(random.uniform(0.1, 0.3))

if __name__ == '__main__':
    print("開始執行，請切到目標視窗...")
    time.sleep(5)
    
    threading.Thread(target=combined_keys, daemon=True).start()

    # 主線程保持運行
    while True:
        time.sleep(1)