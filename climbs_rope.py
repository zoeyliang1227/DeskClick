   
def try_climb_rope(threshold=0.8):
    screenshot = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    result = cv2.matchTemplate(screen, rope_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    if max_val >= threshold:
        pyautogui.keyDown('up')
            time.sleep(2)
            pyautogui.keyUp('up')