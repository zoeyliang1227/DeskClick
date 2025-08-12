import time
import random
import threading

from button import send_key, send_combo_keys
from listener import pause_state
from presses_spacebar import start_space_thread, stop_space_thread


def periodic_keys_loop(self, buff_key, run_times, space_1, space_2, buff_time):
    """定期按鍵序列"""    
    cycle_count = 0
    while self.running:
        last_buff_time = time.time()
        time_wait = random.uniform(0.7, 1.3)
        wait_time = random.randint(space_1, space_2)
        while self.paused:
            pause_state(self)

        cycle_count += 1
        print(f"[週期 {cycle_count}] 等待 {wait_time} 秒...")
        # 分段等待，這樣可以及時響應停止信號
        for i in range(wait_time):
            time.sleep(time_wait)
            # 每10秒顯示一次進度
            if (i + 1) % 10 == 0:
                remaining = wait_time - i - 1
                print(f"   還有 {remaining} 秒...")

        print("⏹️ 暫停空白鍵線程...")
        stop_space_thread(self)
        time.sleep(time_wait)
        print(f"[週期 {cycle_count}] 開始按鍵序列...")
        # 隨機選擇左鍵或右鍵
        direction = random.choice(['left', 'right'])
        presses = random.randint(1, run_times)
        print(f"隨機選擇: {direction}鍵，按 {presses} 次")
        for i in range(presses): 
            success = send_combo_keys(self, direction, 'c')
            print(f"  {i+1}. {direction} + c -> {'✓' if success else '✗'}")
            time.sleep(time_wait)
        # 隨機決定是否按 Z
        time.sleep(time_wait)
        if random.choice([True, False]):
            result3 = send_key(self, 'z')
            print(f"  z -> {'✓' if result3 else '✗'}")
            time.sleep(time_wait)
        else:
            print("  跳過 z 鍵")
        time.sleep(time_wait)
        # 在 while self.running 裡替換 buff 部分
        if time.time() - last_buff_time >= buff_time:  # 間隔 >= 200 秒
            for k in range(1, buff_key + 1):
                result4 = send_key(self, str(k))
                print(f"  {k} -> {'✓' if result4 else '✗'}")
                time.sleep(time_wait)
            last_buff_time = time.time()  # 更新上次 buff 時間
        else:
            print(f"  跳過 Buff（未到 {buff_time} 秒）")
            
        time.sleep(time_wait)
        print(f"✅ [週期 {cycle_count}] 按鍵序列完成\n" + "-"*40)
        start_space_thread(self)
