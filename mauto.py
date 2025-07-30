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
        space_count = 0
        try:
            while self.running:
                space_count += 1
                self.send_key('space', random.uniform(0.1, 0.3))
                
                # 每100次顯示一次狀態
                if space_count % 100 == 0:
                    print(f"🔄 空白鍵已執行 {space_count} 次，狀態: {'運行中' if self.running else '已停止'}")
                
                time.sleep(random.uniform(0.1, 0.3))
        except Exception as e:
            print(f"❌ hold_space_loop 出錯: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print(f"🔚 hold_space_loop 線程結束 (總共執行 {space_count} 次)")
    
    def periodic_keys_loop(self):
        """定期按鍵序列"""
        try:
            time.sleep(2)  # 等待空白鍵先開始
            
            # 初始按鍵
            print("按初始 1 鍵")
            success = self.send_key('1')
            print(f"初始1鍵結果: {success}")
            
            cycle_count = 0
            while self.running:
                cycle_count += 1
                wait_time = random.randint(10, 60)
                print(f"[週期 {cycle_count}] 等待 {wait_time} 秒...")
                
                # 分段等待，這樣可以及時響應停止信號
                for i in range(wait_time):
                    if not self.running:
                        print("⏹️ 收到停止信號，退出等待")
                        return
                    time.sleep(1)
                    
                    # 每10秒顯示一次進度
                    if (i + 1) % 10 == 0:
                        remaining = wait_time - i - 1
                        print(f"   還有 {remaining} 秒...")
                
                if not self.running:
                    break
                
                print(f"[週期 {cycle_count}] 開始按鍵序列...")
                
                try:
                    # 隨機選擇左鍵或右鍵
                    direction = random.choice(['left', 'right'])
                    presses = random.randint(1, 10)
                    print(f"隨機選擇: {direction}鍵，按 {presses} 次")
                    
                    for i in range(presses):
                        if not self.running:
                            print("⏹️ 收到停止信號，中斷按鍵序列")
                            return
                            
                        result1 = self.send_key(direction)
                        print(f"  {i+1}. {direction} -> {'✓' if result1 else '✗'}")
                        time.sleep(0.2)
                        
                        result2 = self.send_key('c')
                        print(f"     c -> {'✓' if result2 else '✗'}")
                        time.sleep(random.uniform(0.3, 0.7))
                    
                    # 隨機決定是否按 Z
                    time.sleep(0.5)
                    if random.choice([True, False]):
                        result3 = self.send_key('z')
                        print(f"  z -> {'✓' if result3 else '✗'}")
                        time.sleep(0.5)
                    else:
                        print("  跳過 z 鍵")
                    
                    # 按數字 1
                    result4 = self.send_key('1')
                    print(f"  1 -> {'✓' if result4 else '✗'}")
                    time.sleep(0.5)
                    
                    print(f"✅ [週期 {cycle_count}] 按鍵序列完成\n" + "-"*40)
                    
                except Exception as e:
                    print(f"❌ [週期 {cycle_count}] 按鍵序列出錯: {e}")
                    import traceback
                    traceback.print_exc()
                    continue  # 繼續下一輪，不要停止
                    
        except Exception as e:
            print(f"❌ periodic_keys_loop 出現嚴重錯誤: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("🔚 periodic_keys_loop 線程結束")
    
    def start(self):
        """開始執行"""
        self.running = True
        
        print("🚀 使用 Windows API 直接發送按鍵")
        print("開始執行，請切換到 Artale 視窗...")
        
        for i in range(5, 0, -1):
            print(f"倒數 {i} 秒...")
            time.sleep(1)
        
        print("✅ 開始執行！")
        
        # 啟動兩個線程
        try:
            space_thread = threading.Thread(target=self.hold_space_loop, daemon=True, name="SpaceThread")
            periodic_thread = threading.Thread(target=self.periodic_keys_loop, daemon=True, name="PeriodicThread")
            
            print("🔄 啟動空白鍵線程...")
            space_thread.start()
            
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
                
                # 檢查線程狀態
                space_alive = space_thread.is_alive()
                periodic_alive = periodic_thread.is_alive()
                
                print(f"📊 運行時間: {hours:02d}:{minutes:02d}:{seconds:02d} | "
                      f"空白鍵線程: {'✅' if space_alive else '❌'} | "
                      f"定期按鍵線程: {'✅' if periodic_alive else '❌'}")
                
                # 如果有線程死亡，重新啟動
                if not space_alive and self.running:
                    print("⚠️  空白鍵線程已死亡，重新啟動...")
                    space_thread = threading.Thread(target=self.hold_space_loop, daemon=True, name="SpaceThread")
                    space_thread.start()
                
                if not periodic_alive and self.running:
                    print("⚠️  定期按鍵線程已死亡，重新啟動...")
                    periodic_thread = threading.Thread(target=self.periodic_keys_loop, daemon=True, name="PeriodicThread")
                    periodic_thread.start()
                    
        except KeyboardInterrupt:
            print("\n⏹️  收到中斷信號 (Ctrl+C)")
        except Exception as e:
            print(f"❌ 主程式出錯: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("🔄 正在停止所有線程...")
            self.running = False
            time.sleep(2)  # 給線程時間結束
            print("✅ 程式已完全停止")

if __name__ == '__main__':
    controller = WinKeyController()
    controller.start()