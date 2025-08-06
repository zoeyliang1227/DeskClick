import os
import subprocess

# 1. 找出所有 .py 檔（排除主程式 mauto.py 與自己）
current_file = os.path.basename(__file__)
all_py_files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'mauto.py' and f != current_file]

# 2. 寫入 files.txt
with open("files.txt", "w") as f:
    for py in all_py_files:
        f.write(py + '\n')

# 3. 生成 PyInstaller 指令
with open("files.txt", "r") as f:
    files = [line.strip() for line in f if line.strip()]

cmd = ['pyinstaller', '-F', 'mauto.py']

for file in files:
    cmd += ['--add-data', f'{file};.']

# 4. 執行打包指令
print("🚀 正在打包...")
subprocess.run(cmd)
print("✅ 打包完成！")
