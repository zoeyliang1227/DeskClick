import os
import sys
import json
import subprocess

from pathlib import Path

if len(sys.argv) < 2:
    print("請輸入要打包的主程式檔名，例如： python pyinstaller_cmd.py mauto.py")
    sys.exit(1)

main_script = sys.argv[1]
if not os.path.isfile(main_script):
    print(f"找不到主程式檔案：{main_script}")
    sys.exit(1)

current_file = os.path.basename(__file__)
main_script_name = os.path.basename(main_script)

# 找出所有 .py 檔，排除主程式和本打包腳本
all_py_files = [f for f in os.listdir('.') if f.endswith('.py') and f != main_script_name and f != current_file]

# 寫入 files.txt
with open("files.txt", "w") as f:
    for py in all_py_files:
        f.write(py + '\n')

# 從 files.txt 讀取
with open("files.txt", "r") as f:
    files = [line.strip() for line in f if line.strip()]

# 建立 PyInstaller 指令
cmd = ['pipenv', 'run', 'pyinstaller', '-F', main_script]

for file in files:
    # 注意 Windows 用分號 ;，Linux/mac 用冒號 :
    # 這裡假設 Windows
    cmd += ['--add-data', f'{file};.']

hidden_imports = []
lockfile = Path("Pipfile.lock")
if lockfile.exists():
    data = json.loads(lockfile.read_text())
    hidden_imports = list(data.get("default", {}).keys())

for pkg in hidden_imports:
    cmd += ["--hidden-import", pkg]

print("🚀 正在打包...")
subprocess.run(cmd)
print("✅ 打包完成！")