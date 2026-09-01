"""analyze.py —— 实习生留下的"能跑但很乱"的工单统计脚本。

这是 Case 01 的起始代码。功能：
1. 读取工单 CSV（id, title, body, priority, created_at, resolved_at, channel）
2. 计算：总工单数、按渠道分布、平均解决时长（小时）、未解决工单数
3. 输出一个纯文本报表到 stdout

它故意写得很乱：全局变量、重复代码、没有函数边界、没有测试。
你的任务是重构它，但【保持输出不变】。
"""
import csv
import sys
from datetime import datetime

results = {}


def main(path):
    f = open(path, newline="", encoding="utf-8")
    reader = csv.DictReader(f)
    rows = []
    for r in reader:
        rows.append(r)
    f.close()

    # total
    total = 0
    for r in rows:
        total += 1
    results["total"] = total

    # by channel
    channels = {}
    for r in rows:
        ch = r["channel"]
        if ch not in channels:
            channels[ch] = 0
        channels[ch] = channels[ch] + 1
    results["channels"] = channels

    # avg resolution hours
    hours = []
    for r in rows:
        if r["resolved_at"] != "" and r["resolved_at"] is not None:
            t1 = datetime.strptime(r["created_at"], "%Y-%m-%d %H:%M:%S")
            t2 = datetime.strptime(r["resolved_at"], "%Y-%m-%d %H:%M:%S")
            delta = t2 - t1
            h = delta.total_seconds() / 3600
            hours.append(h)
    if len(hours) > 0:
        s = 0
        for h in hours:
            s = s + h
        results["avg_resolution_hours"] = s / len(hours)
    else:
        results["avg_resolution_hours"] = 0

    # unresolved
    n = 0
    for r in rows:
        if r["resolved_at"] == "" or r["resolved_at"] is None:
            n += 1
    results["unresolved"] = n

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
