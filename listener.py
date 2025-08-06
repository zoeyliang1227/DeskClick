import time
import keyboard

from key_codes import VK_CODES
from presses_spacebar import stop_space_thread

time_wait = 0.3
start = 'F4'
pause = 'F2'

try:
    KEYBOARD_AVAILABLE = True

except ImportError:
    KEYBOARD_AVAILABLE = False
    print("⚠️  keyboard 庫未安裝，將使用替代控制方案")

def toggle_pause(self):
        """切換暫停/繼續狀態"""
        self.paused = not self.paused
        if self.paused:
            print("\n" + "="*50)
            print("⏸️  腳本已暫停")
            print("📋 所有自動功能已停止:")
            print("   🔸 自動尋怪已暫停")
            print("   🔸 自動按空白鍵已暫停") 
            print("   🔸 自動攀爬已暫停")
            print("   🔸 自動Buff已暫停")
            print(f"📌 按 {start} 鍵恢復運行")
            print("📌 按 ESC 鍵完全退出程式")
            print("="*50)
        else:
            print("\n" + "="*50)
            print("▶️  腳本已恢復運行")
            print("📋 所有自動功能已重啟:")
            print("   🔸 自動尋怪已恢復")
            print("   🔸 自動按空白鍵已恢復")
            print("   🔸 自動攀爬已恢復") 
            print("   🔸 自動Buff已恢復")
            print(f"📌 按 {pause} 鍵可隨時暫停")
            print("="*50)

def windows_key_listener(self):
    """使用 Windows API 監聽按鍵（不需要管理員權限）"""
    print("🎮 Windows API 按鍵監聽已啟動")
    print("📋 控制方式:")
    print("   🔹 滑鼠中鍵（滾輪按下）: 暫停/恢復")
    print("   🔹 滑鼠右鍵長按3秒: 退出程式")
    print("   🔹 或在控制台輸入命令")
    
    # 使用 Windows API 監聽滑鼠
    last_right_press = 0
    
    while self.running:
        try:
            # 檢查滑鼠中鍵（滾輪按下）- VK_MBUTTON = 0x04
            if self.user32.GetAsyncKeyState(VK_CODES['mouse_middle']) & 0x8000:
                toggle_pause(self)
                time.sleep(time_wait)  # 防止重複觸發
            
            # 檢查滑鼠右鍵長按 - VK_RBUTTON = 0x02
            if self.user32.GetAsyncKeyState(VK_CODES['mouse_right']) & 0x8000:
                if last_right_press == 0:
                    last_right_press = time.time()
                elif time.time() - last_right_press > 3:  # 長按3秒
                    print("\n🛑 滑鼠右鍵長按3秒，正在退出...")
                    stop(self)
                    break
            else:
                last_right_press = 0
            
            # 檢查數字鍵盤的 0 鍵作為暫停鍵 - VK_NUMPAD0 = 0x60
            if self.user32.GetAsyncKeyState(VK_CODES['numpad_0']) & 0x8000:
                toggle_pause(self)
                time.sleep(time_wait)
            
            time.sleep(time_wait)
            
        except Exception as e:
            print(f"⚠️  Windows API 監聽錯誤: {e}")
            print("🔄 切換到控制台輸入模式...")
            console_input_listener(self)
            break

def keyboard_listener_with_fallback(self):
    """智能按鍵監聽（優先使用 keyboard 庫，失敗則使用替代方案）"""
    if KEYBOARD_AVAILABLE:
        try:
            print("🔑 嘗試全局按鍵監聽...")
            success = False
            test_count = 0
            
            while self.running and test_count < 10:  
                try:
                    if keyboard.is_pressed(start):
                        pass
                    success = True
                    break
                except Exception as e:
                    test_count += 1
                    time.sleep(time_wait)
            
            if success:
                print(f"✅ 全局按鍵監聽成功！使用 {pause} 控制")
                global_keyboard_listener(self)

            else:
                raise Exception("按鍵監聽測試失敗")
                
        except Exception as e:
            print(f"⚠️  全局按鍵監聽失敗: {e}")
            print("🔄 切換到 Windows API 方案...")
            windows_key_listener(self)
    else:
        print("📝 keyboard 庫不可用，使用 Windows API...")
        windows_key_listener(self)

def global_keyboard_listener(self):
    """全局鍵盤監聽"""
    while self.running:
        try:
            # 暫停
            if keyboard.is_pressed(pause):
                print(f"🔑 檢測到 {pause} 鍵...")
                toggle_pause(self)
                self.paused = True
                time.sleep(time_wait)
            
            #開始
            elif keyboard.is_pressed(start): 
                print(f"🔑 檢測到 {start} 鍵...")
                toggle_pause(self)
                self.paused = False
                time.sleep(time_wait)

            elif keyboard.is_pressed('esc'):
                print("\n🛑 ESC鍵被按下，正在退出...")
                stop(self)
                break

            time.sleep(time_wait)

        except Exception as e:
            print(f"⚠️  全局監聽中斷: {e}")
            print("🔄 切換到備用方案...")
            windows_key_listener(self)
            break

def console_input_listener(self):
    """控制台輸入監聽"""
    print("\n" + "="*50)
    print("📝 控制台控制模式")
    print("   輸入指令後按 Enter:")
    print("   'p' = 暫停/恢復腳本")  
    print("   's' = 顯示當前狀態")
    print("   'q' = 退出程式")
    print("   直接按 Enter = 暫停/恢復（快捷方式）")
    print("="*50)
    
    while self.running:
        try:
            prompt = "⏸️暫停中" if self.paused else "▶️運行中"
            cmd = input(f"[{prompt}] 請輸入命令: ").strip().lower()
            
            if cmd == 'p' or cmd == '':  # 空輸入也當作暫停/恢復
                toggle_pause(self)
            elif cmd == 's':
                show_status(self)
            elif cmd == 'q':
                print("正在退出程式...")
                stop(self)
                break
            elif cmd == 'help' or cmd == 'h':
                print("可用命令: p(暫停), s(狀態), q(退出), Enter(快速暫停)")
            else:
                print(f"未知命令: '{cmd}'，輸入 'help' 查看說明")
                
        except (EOFError, KeyboardInterrupt):
            print("\n收到中斷信號，正在退出...")
            stop(self)
            break
        except Exception as e:
            print(f"輸入錯誤: {e}")
            time.sleep(time_wait)

def stop(self):
    """停止所有功能"""
    if not self.running:
        return
        
    print("🛑 正在停止所有功能...")
    self.running = False
    self.paused = False
    # stop_space_thread(self)
    # stop_periodic_thread(self)
    print("✅ 所有功能已停止")
    print("👋 程式即將退出...")
    
    # 給一點時間讓線程清理
    time.sleep(1)

def pause_state(self):
    if self.paused:
        time.sleep(time_wait)
    else:
        print("🔑 檢測到 F4 鍵...")
        print('🔄 啟動定期按鍵線程...')