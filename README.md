># Windows

## Description
Use **ctypes** and **threading** to automate the mouse and keyboard

## Install

- Install Python 3.11
- pip install --user pipenv
- python -m pipenv sync
- python -m pipenv shell

## Run
- python mauto.py
- python pyinstaller_cmd.py > packaging pyinstaller

<!-- pyinstaller -F <python file>   # 打包成單執行檔，適合小檔
pyinstaller -D <python file>   # 打包成多個文件，適合框架類程式 
pyinstaller -F mauto.py --add-data "key_codes.py;button.py;climbs_rope.py;listener.py;monsters_attacks.py;presses_spacebar.py;rune.py;screen.py;"-->

## License
__init__.py > 類別初始化
button.py > 按鍵/組合鍵
climbs_rope.py > 爬繩
key_codes.py > VK_CODES
listener.py > 腳本暫停/恢復
monsters_attacks.py > 自動打怪
presses_spacebar.py > 空白鍵
rune.py > 符文
screen.py > 截圖
