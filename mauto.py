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
        self.space_running = False

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
    def send_combo_keys(self, key1, key2, hold_time=0.1):
        """模擬同時按下兩個鍵（例如方向鍵 + c）"""
        if key1 not in VK_CODES or key2 not in VK_CODES:
            return False

        vk1 = VK_CODES[key1]
        vk2 = VK_CODES[key2]

        try:
            # 按下 key1 和 key2
            self.user32.keybd_event(vk1, 0, 0, 0)
            self.user32.keybd_event(vk2, 0, 0, 0)
            time.sleep(hold_time)

            # 放開 key2 和 key1（反向順序）
            self.user32.keybd_event(vk2, 0, 2, 0)
            self.user32.keybd_event(vk1, 0, 2, 0)

            return True
        except Exception as e:
            print(f"組合鍵發送失敗: {e}")
            return False

    def hold_space_loop(self):
        while self.space_running:
            self.send_key('space', random.uniform(0.1, 0.3))
            time.sleep(random.uniform(0.1, 0.3))

    def start_space_thread(self):
        if not self.space_running:
            self.space_running = True
            self.space_thread = threading.Thread(target=self.hold_space_loop, daemon=True)
            self.space_thread.start()
            print("🟢 空白鍵線程已啟動")

    def stop_space_thread(self):
        if self.space_running:
            print("⏹️ 正在停止空白鍵線程...")
            self.space_running = False
            if self.space_thread.is_alive():
                self.space_thread.join()
            print("🔴 空白鍵線程已停止")

    def periodic_keys_loop(self):
        """定期按鍵序列"""
        time.sleep(2)  # 等待空白鍵先開始
        
        cycle_count = 0
        while self.running:
            cycle_count += 1
            wait_time = random.randint(10, 60)
            print(f"[週期 {cycle_count}] 等待 {wait_time} 秒...")
            
            # 分段等待，這樣可以及時響應停止信號
            for i in range(wait_time):
                time.sleep(1)
                
                # 每10秒顯示一次進度
                if (i + 1) % 10 == 0:
                    remaining = wait_time - i - 1
                    print(f"   還有 {remaining} 秒...")

            print("⏹️ 暫停空白鍵線程...")
            self.stop_space_thread()
            time.sleep(2)
            
            print(f"[週期 {cycle_count}] 開始按鍵序列...")
            
            # 隨機選擇左鍵或右鍵
            direction = random.choice(['left', 'right'])
            presses = random.randint(1, 10)
            print(f"隨機選擇: {direction}鍵，按 {presses} 次")
            
            # for i in range(presses):                    
            #     result1 = self.send_key(direction)
            #     time.sleep(random.uniform(0.7, 1.3))
            #     result2 = self.send_key('c')
            #     print(f"  {i+1}. {direction} 和 c -> {'✓' if result1 and result2 else '✗'}")
            #     time.sleep(random.uniform(0.7, 1.3))
            for i in range(presses):  
                success = self.send_combo_keys(direction, 'c', hold_time=random.uniform(0.2, 0.4))
                print(f"  {i+1}. {direction} + c -> {'✓' if success else '✗'}")
                time.sleep(random.uniform(0.7, 1.3))
                    
            # 隨機決定是否按 Z
            time.sleep(random.uniform(0.7, 1.3))
            if random.choice([True, False]):
                result3 = self.send_key('z')
                print(f"  z -> {'✓' if result3 else '✗'}")
                time.sleep(random.uniform(0.7, 1.3))
            else:
                print("  跳過 z 鍵")
            
            time.sleep(random.uniform(0.7, 1.3))
            # 按數字 1
            result4 = self.send_key('1')
            print(f"  1 -> {'✓' if result4 else '✗'}")
            time.sleep(random.uniform(0.7, 1.3))
            
            print(f"✅ [週期 {cycle_count}] 按鍵序列完成\n" + "-"*40)

            self.start_space_thread()

    def start(self):
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
        periodic_thread = threading.Thread(target=self.periodic_keys_loop, daemon=True, name="PeriodicThread")
        
        print("🔄 啟動空白鍵線程...")
        self.space_thread.start()
        
        print("🔄 啟動定期按鍵線程...")
        periodic_thread.start()
        
        print("✨ 腳本已啟動！按 Ctrl+C 停止")
        print("="*50)
        
        # 主線程監控
        start_time = time.time()
        while self.running:
            time.sleep(10)  # 每10秒檢查一次
            
            elapsed = time.time() - start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            

if __name__ == '__main__':
    controller = WinKeyController()
    controller.start()