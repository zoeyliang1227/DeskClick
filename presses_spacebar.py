import time
import random
import threading

from button import send_key

time_wait = random.uniform(0.1, 0.3)


def hold_space_loop(self):
    while self.space_running:
        if self.paused:
            stop_space_thread(self)
            time.sleep(time_wait)
            
        else:
            self.send_key('space')
            time.sleep(time_wait)

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
        if self.space_thread.is_alive() and threading.current_thread() != self.space_thread:
            self.space_thread.join()
        print("🔴 空白鍵線程已停止")
