import os
import time
import random
import cv2
import numpy as np

from key_codes import VK_CODES
from PIL import Image
from get_img import load_monster_templates
from screen import grab_screen_and_save
from button import send_key, send_combo_keys
from listener import pause_state

threshold = 0.2
time_wait = random.uniform(0.7, 1.3)

def periodic_keys_loop(self, buff_key, run_times, space_1, space_2, buff_time):
    """主要循環，定期掃描螢幕尋找怪物並攻擊"""
    templates = load_monster_templates('monster')
    cycle_count = 0
    last_buff_time = time.time()  # 記錄上次補buff時間
    while self.running:
        cycle_count += 1
        print(f"[週期 {cycle_count}] 開始掃描螢幕...")
        
        # 暫停檢查
        while self.paused:
            pause_state(self)
        
        # 截取螢幕並轉灰階
        screen_gray = grab_screen_and_save()
        
        # 尋找並攻擊怪物
        monster_found = find_and_attack(self, screen_gray, templates, run_times, buff_key)
        
        # 檢查是否需要補buff
        if time.time() - last_buff_time >= buff_time:
            cast_buffs(self, buff_key)
            last_buff_time = time.time()

        else:
            remaining = int(time.time() - last_buff_time)
            print(f"  buff 持續了 {remaining} 秒")
            print(f"  跳過 Buff（未到 {buff_time} 秒）")
        
        # 如果沒找到怪物，等待一段時間
        if not monster_found:
            wait_time = random.randint(space_1, space_2)
            print(f"未找到怪物，等待 {wait_time} 秒...")
            
            # 分段等待，可以及時響應停止信號
            for i in range(wait_time):
                if not self.running:
                    break
                time.sleep(time_wait)
                if (i + 1) % 10 == 0:
                    remaining = wait_time - i - 1
                    print(f"   還有 {remaining} 秒...")
        else:
            time.sleep(time_wait)  # 找到怪物後短暫等待

def find_and_attack(self, screen_gray, templates, run_times, buff_key):
    """在螢幕上尋找怪物並進行攻擊"""
    print(f"開始掃描，共 {len(templates)} 個怪物模板")
    
    # 遍歷所有怪物模板
    for template_idx, template in enumerate(templates):
        # 確保都是灰階圖片
        if not (is_gray(screen_gray) and is_gray(template)):
            print(f"模板 {template_idx + 1} 格式不符，跳過")
            continue
        
        # cv2.imshow('screen_gray', screen_gray)
        # cv2.imshow('template', template)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # 模板匹配
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        max_val = np.max(res)
        
        print(f"模板 {template_idx + 1} 最大相似度: {max_val:.3f}")
        
        # 如果相似度超過閾值，表示找到怪物
        if max_val >= threshold:
            # 找到所有符合條件的位置
            loc = np.where(res >= threshold)
            
            # 處理找到的怪物位置
            for pt in zip(*loc[::-1]):
                print(f"找到怪物 (模板{template_idx + 1}) 在位置 {pt}，準備攻擊")
                attack_at_position(self, pt, screen_gray.shape, run_times, buff_key)
                return True  # 找到一個怪物就先攻擊，不繼續搜尋其他模板
    
    print("所有模板掃描完畢，未找到怪物")
    return False

def attack_at_position(self, pt, screen_shape, run_times, buff_key):
    """根據怪物位置移動並攻擊"""
    screen_height, screen_width = screen_shape[:2]
    x, y = pt
    
    # 計算螢幕中心點
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    # 判斷怪物位置並決定移動方向
    direction_h = 'left' if x < center_x else 'right'
    is_upper = y < center_y  # 判斷是否在上半部
    
    print(f"怪物位置: ({x}, {y})")
    print(f"螢幕中心: ({center_x}, {center_y})")
    print(f"怪物在螢幕{'上半部' if is_upper else '下半部'}的{'左側' if direction_h == 'left' else '右側'}")
    
    # 移動到怪物位置（不限步數）
    move_to_monster(self, direction_h, is_upper)
    
    # 執行攻擊
    attack_by_keyboard(self, direction_h, is_upper, run_times, buff_key)

def move_to_monster(self, direction_h, is_upper, max_steps=50):
    """移動到怪物位置，不限步數直到到達"""
    steps = 0
    print(f"開始移動，方向: {direction_h}，{'需要跳躍' if is_upper else '平移'}")
    
    while steps < max_steps:
        if not self.running:
            break
            
        # 如果怪物在上方，需要跳躍
        if is_upper:
            # 按住方向鍵 + 跳躍鍵（假設跳躍鍵是 'space' 或 'up'）
            success1 = send_key(self, direction_h)
            success2 = send_key(self, 'space')  # 或使用 'up' 鍵
            print(f"第 {steps+1} 步 -> {direction_h} + 跳躍 -> {'✓' if success1 and success2 else '✗'}")
        else:
            # 只按方向鍵移動
            success = send_key(self, direction_h)
            print(f"第 {steps+1} 步 -> {direction_h} 移動 -> {'✓' if success else '✗'}")
        
        time.sleep(time_wait)
        steps += 1
        
        # 每5步檢查一次是否還需要繼續移動
        if steps % 5 == 0:
            print(f"已移動 {steps} 步，繼續移動中...")
    
    print(f"移動完成，共移動 {steps} 步")

def attack_by_keyboard(self, direction_h, is_upper, run_times, buff_key):
    """執行鍵盤攻擊序列"""
    print(f"開始攻擊 - 方向: {direction_h}, 位置: {'上方' if is_upper else '下方'}, 攻擊次數: {run_times}")
    
    # 主要攻擊序列：方向鍵 + c
    presses = random.randint(1, run_times)
    for i in range(presses):
        if not self.running:
            break
            
        # 如果怪物在上方，攻擊時也要跳躍
        if is_upper:
            success = send_combo_keys(self, direction_h, 'space', 'c')  # 方向+跳+攻擊
            print(f"  {i+1}. {direction_h} + 跳躍 + c -> {'✓' if success else '✗'}")
        else:
            success = send_combo_keys(self, direction_h, 'c')
            print(f"  {i+1}. {direction_h} + c -> {'✓' if success else '✗'}")
        
        time.sleep(time_wait)
    
    # 隨機使用特殊技能 (z鍵)
    if random.choice([True, False]):
        result = send_key(self, 'z')
        print(f"  特殊技能 z -> {'✓' if result else '✗'}")
        time.sleep(time_wait)
    else:
        print("  跳過特殊技能")
    
    print("攻擊完成\n" + "-"*50)

def cast_buffs(self, buff_key):
    """施放buff技能"""
    print("開始補buff...")
    
    for k in range(1, buff_key + 1):
        if not self.running:
            break
            
        result = send_key(self, str(k))
        print(f"  {k} -> {'✓' if result else '✗'}")
        time.sleep(time_wait)
    
    print("buff補充完成")

def is_gray(img):
    """判斷圖片是否為灰階"""
    if len(img.shape) == 2:
        return True

    else:
        return False

def pause_state(self):
    """處理暫停狀態"""
    print("程式已暫停...")
    time.sleep(time_wait)

# 如果需要測試
# if __name__ == "__main__":
#     # 這裡需要一個mock的self對象來測試
#     pass