import ctypes
import ctypes.wintypes
import time
import random
import threading

# Windows API 常數
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

# 虛擬鍵碼
VK_CODES = {
    'space': 0x20,
    'left': 0x25,
    'right': 0x27,
    'c': 0x43,
    'z': 0x5A,
    '1': 0x31,
}

class WinKeyController:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        self.running = False
        
    def send_key(self, key, hold_time=0.05):
        """使用Windows API發送按鍵"""
        if key in VK_CODES:
            vk_code = VK_CODES[key]
            
            # 發送按鍵
            self.user32.keybd_event(vk_code, 0, 0, 0)  # 按下
            time.sleep(hold_time)
            self.user32.keybd_event(vk_code, 0, 2, 0)  # 釋放 (KEYEVENTF_KEYUP = 2)
            return True
        return False
    
    def hold_space_loop(self):
        """持續按空白鍵"""
        while self.running:
            self.send_key('space', random.uniform(0.1, 0.3))
            time.sleep(random.uniform(0.1, 0.3))
    
    def periodic_keys_loop(self):
        """定期按鍵序列"""
        time.sleep(2)  # 等待空白鍵先開始
        
        # 初始按鍵
        print("按初始 1 鍵")
        self.send_key('1')
        
        while self.running:
            wait_time = random.randint(10, 60)
            print(f"等待 {wait_time} 秒...")
            time.sleep(wait_time)
            
            if not self.running:
                break
            
            print("開始按鍵序列...")
            
            # 隨機選擇左鍵或右鍵
            direction = random.choice(['left', 'right'])
            presses = random.randint(1, 10)
            print(f"隨機選擇: {direction}鍵，按 {presses} 次")
            
            for i in range(presses):
                if not self.running:
                    break
                self.send_key(direction)
                print(f"{direction}")
                time.sleep(0.1)
                self.send_key('c')
                print("c")
                time.sleep(random.uniform(0.2, 0.6))
            
            # 隨機決定是否按 Z
            time.sleep(random.uniform(0.3, 0.5))
            if random.choice([True, False]):
                self.send_key('z')
                print("z")
                time.sleep(random.uniform(0.3, 0.5))
            
            # 按數字 1
            self.send_key('1')
            print("1")
            time.sleep(random.uniform(0.3, 0.5))
            
            print("本輪按鍵完成\n" + "-"*30)
    
    def start(self):
        """開始執行"""
        self.running = True
        
        print("使用 Windows API 直接發送按鍵")
        print("開始執行，請切換到 Artale 視窗...")
        time.sleep(5)
        
        # 啟動兩個線程
        space_thread = threading.Thread(target=self.hold_space_loop, daemon=True)
        periodic_thread = threading.Thread(target=self.periodic_keys_loop, daemon=True)
        
        space_thread.start()
        periodic_thread.start()
        
        print("腳本已啟動！按 Ctrl+C 停止")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n正在停止...")
            self.running = False
            time.sleep(1)
            print("已停止")

if __name__ == '__main__':
    controller = WinKeyController()
    controller.start()