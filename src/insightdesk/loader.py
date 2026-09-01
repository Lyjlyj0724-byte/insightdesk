"""loader.py —— 读取工单 CSV。

从 analyze.py 抽出的第一块职责：只负责把 CSV 读成 list[dict]。
"""
import csv


def load_tickets(path):
    """读取工单 CSV，返回字典列表（每行一个 dict）。"""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
