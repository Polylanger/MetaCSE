# 在入口文件（main.py）开头添加：
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.app import MetaCSEApp

if __name__ == "__main__":
    app = MetaCSEApp()
    app.mainloop()
