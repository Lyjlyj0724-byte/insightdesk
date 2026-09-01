"""analyze.py —— 兼容入口（重构后只剩这个壳）。

业务逻辑已全部拆到 src/insightdesk/ 包：
- loader.py  读 CSV、数据校验
- metrics.py 统计计算
- report.py  输出报表

本文件保持旧用法可用，等价于 `python -m insightdesk`：
    python analyze.py data/tickets_sample.csv
"""
import sys
from pathlib import Path

# 让未安装包的情况下也能 import src/ 下的 insightdesk 包
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from insightdesk.__main__ import main

if __name__ == "__main__":
    main()
