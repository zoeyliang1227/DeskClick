import ctypes
import time

from key_codes import VK_CODES

hold_time=0.1

def send_combo_keys(self, key1, key2):
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

def send_key(self, key):
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