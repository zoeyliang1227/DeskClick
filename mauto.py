import time
import yaml
import ctypes
import random
import threading

from monsters_attacks import periodic_keys_loop
from presses_spacebar import hold_space_loop
from button import send_key
from listener import keyboard_listener_with_fallback, stop

start = 'F4'
pause = 'F2'


class WinKeyController():
    def __init__(self, config_path='config.yml'):
        self.runtime_str = ''
        self.config = self.load_config(config_path)
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        self.running = False
        self.paused = False
        self.space_running = False

    def load_config(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def send_key(self, key):
        send_key(self, key)
        if send_key(self, key):
            return True

    def hold_space_loop(self):
        hold_space_loop(self)

    def auto_mosters(self):
        auto_mosters(self)

    def periodic_keys_loop(self, buff_key, run_times, space_1, space_2, buff_time):
        periodic_keys_loop(self, buff_key, run_times, space_1, space_2, buff_time)

    def keyboard_listener_with_fallback(self):
        keyboard_listener_with_fallback(self)

    def stop(self):
        stop(self)

    def start(self):
        """開始執行"""
        self.space_running = True
        self.running = True

        buff_key = int(self.config.get('buff_key'))
        run_times = int(self.config.get('run_times'))
        space_1 = int(self.config.get('space_1'))
        space_2 = int(self.config.get('space_2'))
        buff_time = int(self.config.get('buff_time'))
        

        print(f"📌 按鍵: {buff_key} / 次數: {run_times} / 延遲: {space_1}-{space_2}秒 / buff時間: {buff_time} 秒")
        print("="*50)
        
        print("🚀 使用 Windows API 直接發送按鍵")
        print("開始執行，請切換到 Artale 視窗...")
        
        for i in range(5, 0, -1):
            print(f"倒數 {i} 秒...")
            time.sleep(2)
        
        print("✅ 開始執行！")
        
        # 啟動兩個線程
        # 初始按鍵
        print(f"按初始 {buff_key} 個 buff")
        for k in range(1, buff_key+1):
            success = self.send_key(str(k))
            time.sleep(random.uniform(0.7, 1.3))
        
        print(f"初始 {buff_key} 個 buff 結果: {success}")

        self.space_thread = threading.Thread(target=self.hold_space_loop, daemon=True)
        periodic_thread = threading.Thread(target=lambda: self.periodic_keys_loop(buff_key, run_times, space_1, space_2, buff_time), daemon=True, name="PeriodicThread")
        
        print("🔄 啟動空白鍵線程...")
        self.space_thread.start()
        
        print("🔄 啟動定期按鍵線程...")
        periodic_thread.start()

        print("🔄 啟動智能控制系統...")
        control_thread = threading.Thread(target=self.keyboard_listener_with_fallback, daemon=True, name="ControlThread")
        control_thread.start()
        
        print("✨ 所有系統已啟動！")
        print(f"💡 提示：按 {start} 可隨時暫停腳本，處理完事情後再按 {pause} 恢復")
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
                    status += f" | 尋怪: {'🟢' if periodic_thread else '🔴'}"
                    status += f" | 狀態: {'▶️運行中' if not self.paused else '⏸️暫停'}"
                    print(f"📊 {status}")
                
        except KeyboardInterrupt:
            print("\n⏹️ 收到停止信號...")
            self.stop()
            

if __name__ == '__main__':
    print("🎮 Artale 自動腳本")
    print(f"⚠️  注意：如果 {pause} 鍵無法使用，程式會自動切換到控制台輸入模式")

    controller = WinKeyController()
    controller.start()