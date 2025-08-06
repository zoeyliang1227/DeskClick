import time
import random
import threading
import pyautogui
import cv2
import numpy as np

from __init__ import __init__
from monsters_attacks import periodic_keys_loop
from presses_spacebar import hold_space_loop
from button import send_key
from listener import keyboard_listener_with_fallback, stop
# from climbs_rope import try_climb_rope
# from Rune import press_arrow_sequence

start = 'F4'
pause = 'F2'


class WinKeyController():
    def __init__(self):
        __init__(self)

    def send_key(self, key):
        send_key(self, key)
        if send_key(self, key):
            return True

    # def send_combo_keys(self, key1, key2):
    #     send_combo_keys(self, key1, key2)

    def hold_space_loop(self):
        hold_space_loop(self)

    # def start_space_thread(self):
    #     start_space_thread(self)

    # def stop_space_thread(self):
    #     stop_space_thread(self)

    def periodic_keys_loop(self, run_times):
        periodic_keys_loop(self, run_times)

    # def toggle_pause(self):
    #     toggle_pause(self)

    def keyboard_listener_with_fallback(self):
        keyboard_listener_with_fallback(self)

    # def simple_key_listener(self):
    #     simple_key_listener(self)

    def stop(self):
        stop(self)

    def start(self, run_times):
        """開始執行"""
        self.space_running = True
        self.running = True
        
        print("🚀 使用 Windows API 直接發送按鍵")
        print("開始執行，請切換到 Artale 視窗...")
        
        for i in range(5, 0, -1):
            print(f"倒數 {i} 秒...")
            time.sleep(1)
        
        print("✅ 開始執行！")
        
        # 啟動兩個線程
        # 初始按鍵
        print("按初始 1 鍵")
        success = self.send_key('1')
        print(f"初始1鍵結果: {success}")
        self.space_thread = threading.Thread(target=self.hold_space_loop, daemon=True)
        periodic_thread = threading.Thread(target=lambda: self.periodic_keys_loop(run_times), daemon=True, name="PeriodicThread")
        
        print("🔄 啟動空白鍵線程...")
        self.space_thread.start()
        
        print("🔄 啟動定期按鍵線程...")
        periodic_thread.start()

        print("🔄 啟動智能控制系統...")
        control_thread = threading.Thread(target=self.keyboard_listener_with_fallback, daemon=True, name="ControlThread")
        control_thread.start()
        
        print("✨ 所有系統已啟動！")
        print("💡 提示：按 F2 可隨時暫停腳本，處理完事情後再按 F4 恢復")
        print("="*60)
        
        # 主線程監控
        start_time = time.time()
        try:
            while self.running:
                time.sleep(10)  # 每10秒檢查一次
                
                elapsed = time.time() - start_time
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)
                
                # 顯示狀態
                if self.paused:
                    status = f"⏸️  暫停中 | 運行時間: {hours:02d}:{minutes:02d}:{seconds:02d}"
                    print(f"📊 {status} | 按 {start} 恢復")

                else:
                    status = f"運行時間: {hours:02d}:{minutes:02d}:{seconds:02d}"
                    status += f" | 空白鍵: {'🟢' if self.space_thread else '🔴'}"
                    # status += f" | 尋怪: {'🟢' if self.monster_hunting else '🔴'}"
                    status += f" | 狀態: {'▶️運行中' if not self.paused else '⏸️暫停'}"
                    print(f"📊 {status}")
                
        except KeyboardInterrupt:
            print("\n⏹️ 收到停止信號...")
            self.stop()
            

if __name__ == '__main__':
    print("🎮 Artale 自動腳本")
    print(f"⚠️  注意：如果 {pause} 鍵無法使用，程式會自動切換到控制台輸入模式")
    
    controller = WinKeyController()
    run_times = int(input("✨ 輸入 隨機選擇左鍵或右鍵 要執行幾次...\n"))
    controller.start(run_times)