import ctypes

def __init__(self):
    self.user32 = ctypes.windll.user32
    self.kernel32 = ctypes.windll.kernel32
    self.running = False
    self.paused = False  # 新增暫停狀態
    self.space_running = False