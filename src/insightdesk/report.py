"""report.py —— 把统计结果渲染成文本报表。

从 analyze.py 抽出的第三块职责：只负责格式化输出。
渲染与打印分离，render_report() 返回字符串，方便测试断言。
"""


def render_report(metrics):
    """把 compute_metrics() 的结果渲染为多行文本（不含结尾换行）。"""
    lines = [
        "=== InsightDesk 工单统计报表 ===",
        "总工单数: " + str(metrics["total"]),
        "未解决工单数: " + str(metrics["unresolved"]),
        "平均解决时长(小时): " + str(round(metrics["avg_resolution_hours"], 2)),
        "按渠道分布:",
    ]
    for ch in metrics["channels"]:
        lines.append("  " + ch + ": " + str(metrics["channels"][ch]))
    lines.append("按优先级分布:")
    for p in metrics["priorities"]:
        lines.append("  " + p + ": " + str(metrics["priorities"][p]))
    return "\n".join(lines)


def print_report(metrics):
    """打印报表到 stdout。"""
    print(render_report(metrics))
