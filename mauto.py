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
            
            try:
                # 獲取當前活動視窗
                hwnd = self.user32.GetForegroundWindow()
                
                # 方法1: 使用 keybd_event (全域)
                self.user32.keybd_event(vk_code, 0, 0, 0)  # 按下
                time.sleep(hold_time)
                self.user32.keybd_event(vk_code, 0, 2, 0)  # 釋放
                
                # 方法2: 同時嘗試 SendInput (更現代的方法)
                # 定義 INPUT 結構
                PUL = ctypes.POINTER(ctypes.c_ulong)
                class KeyBdInput(ctypes.Structure):
                    _fields_ = [("wVk", ctypes.c_ushort),
                              ("wScan", ctypes.c_ushort),
                              ("dwFlags", ctypes.c_ulong),
                              ("time", ctypes.c_ulong),
                              ("dwExtraInfo", PUL)]

                class HardwareInput(ctypes.Structure):
                    _fields_ = [("uMsg", ctypes.c_ulong),
                              ("wParamL", ctypes.c_short),
                              ("wParamH", ctypes.c_ushort)]

                class MouseInput(ctypes.Structure):
                    _fields_ = [("dx", ctypes.c_long),
                              ("dy", ctypes.c_long),
                              ("mouseData", ctypes.c_ulong),
                              ("dwFlags", ctypes.c_ulong),
                              ("time", ctypes.c_ulong),
                              ("dwExtraInfo", PUL)]

                class Input_I(ctypes.Union):
                    _fields_ = [("ki", KeyBdInput),
                              ("mi", MouseInput),
                              ("hi", HardwareInput)]

                class Input(ctypes.Structure):
                    _fields_ = [("type", ctypes.c_ulong),
                              ("ii", Input_I)]
                
                # 備用方法：SendInput
                extra = ctypes.c_ulong(0)
                ii_ = Input_I()
                ii_.ki = KeyBdInput(vk_code, 0, 0, 0, ctypes.pointer(extra))
                x = Input(ctypes.c_ulong(1), ii_)
                self.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                
                time.sleep(hold_time)
                
                ii_.ki = KeyBdInput(vk_code, 0, 2, 0, ctypes.pointer(extra))
                x = Input(ctypes.c_ulong(1), ii_)
                self.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
                
                return True
                
            except Exception as e:
                print(f"按鍵發送失敗 {key}: {e}")
                return False
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
        success = self.send_key('1')
        print(f"初始1鍵結果: {success}")
        
        while self.running:
            wait_time = random.randint(10, 60)
            print(f"等待 {wait_time} 秒...")
            time.sleep(wait_time)
            
            if not self.running:
                break
            
            print("開始按鍵序列...")
            
            # 暫停空白鍵線程
            print("🔄 暫停空白鍵，執行按鍵序列")
            temp_running = self.running
            self.running = False  # 暫停空白鍵
            time.sleep(0.5)  # 等待空白鍵停止
            
            try:
                # 隨機選擇左鍵或右鍵
                direction = random.choice(['left', 'right'])
                presses = random.randint(1, 10)
                print(f"隨機選擇: {direction}鍵，按 {presses} 次")
                
                for i in range(presses):
                    result1 = self.send_key(direction)
                    print(f"{direction} -> {'✓' if result1 else '✗'}")
                    time.sleep(0.2)
                    
                    result2 = self.send_key('c')
                    print(f"c -> {'✓' if result2 else '✗'}")
                    time.sleep(random.uniform(0.3, 0.7))
                
                # 隨機決定是否按 Z
                time.sleep(0.5)
                if random.choice([True, False]):
                    result3 = self.send_key('z')
                    print(f"z -> {'✓' if result3 else '✗'}")
                    time.sleep(0.5)
                else:
                    print("跳過 z 鍵")
                
                # 按數字 1
                result4 = self.send_key('1')
                print(f"1 -> {'✓' if result4 else '✗'}")
                time.sleep(0.5)
                
                print("✅ 本輪按鍵完成\n" + "-"*30)
                
            finally:
                # 恢復空白鍵線程
                self.running = temp_running
                if self.running:
                    print("🔄 恢復空白鍵")
                    # 重新啟動空白鍵線程
                    space_thread = threading.Thread(target=self.hold_space_loop, daemon=True)
                    space_thread.start()
    
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