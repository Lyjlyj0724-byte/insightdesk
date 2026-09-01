"""analyze.py —— 实习生留下的"能跑但很乱"的工单统计脚本。

这是 Case 01 的起始代码。功能：
1. 读取工单 CSV（id, title, body, priority, created_at, resolved_at, channel）
2. 计算：总工单数、按渠道分布、平均解决时长（小时）、未解决工单数
3. 输出一个纯文本报表到 stdout

它故意写得很乱：全局变量、重复代码、没有函数边界、没有测试。
你的任务是重构它，但【保持输出不变】。
"""
import sys
from datetime import datetime
from pathlib import Path

# 让未安装包的情况下也能 import src/ 下的 insightdesk 包
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from insightdesk.loader import load_tickets
from insightdesk.metrics import compute_metrics

results = {}


def main(path):
    rows = load_tickets(path)

    results.update(compute_metrics(rows))

    # report
    print("=== InsightDesk 工单统计报表 ===")
    print("总工单数: " + str(results["total"]))
    print("未解决工单数: " + str(results["unresolved"]))
    print("平均解决时长(小时): " + str(round(results["avg_resolution_hours"], 2)))
    print("按渠道分布:")
    for ch in results["channels"]:
        print("  " + ch + ": " + str(results["channels"][ch]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze.py <tickets.csv>")
        sys.exit(1)
    main(sys.argv[1])
