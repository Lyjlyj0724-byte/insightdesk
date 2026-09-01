"""metrics.py —— 工单统计计算。

从 analyze.py 抽出的第二块职责：纯计算，不做 IO。
"""
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"  # 与工单 CSV 中的时间格式严格一致；TODO: 后续考虑支持 ISO 8601


def count_total(rows):
    """总工单数。"""
    return len(rows)


def count_by_channel(rows):
    """按渠道统计工单数，保持首次出现的顺序。"""
    channels = {}
    for r in rows:
        ch = r["channel"]
        channels[ch] = channels.get(ch, 0) + 1
    return channels


def count_by_priority(rows):
    """按优先级统计工单数，保持首次出现的顺序。"""
    priorities = {}
    for r in rows:
        p = r["priority"]
        priorities[p] = priorities.get(p, 0) + 1
    return priorities


def avg_resolution_hours(rows):
    """已解决工单的平均解决时长（小时）；没有已解决工单时返回 0。"""
    hours = []
    for r in rows:
        if r["resolved_at"] != "" and r["resolved_at"] is not None:
            t1 = datetime.strptime(r["created_at"], TIME_FORMAT)
            t2 = datetime.strptime(r["resolved_at"], TIME_FORMAT)
            hours.append((t2 - t1).total_seconds() / 3600)
    if len(hours) > 0:
        return sum(hours) / len(hours)
    return 0


def count_unresolved(rows):
    """未解决工单数（resolved_at 为空）。"""
    n = 0
    for r in rows:
        if r["resolved_at"] == "" or r["resolved_at"] is None:
            n += 1
    return n


def compute_metrics(rows):
    """计算全部指标，返回 dict。"""
    return {
        "total": count_total(rows),
        "channels": count_by_channel(rows),
        "priorities": count_by_priority(rows),
        "avg_resolution_hours": avg_resolution_hours(rows),
        "unresolved": count_unresolved(rows),
    }
