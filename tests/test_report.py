"""report.py 的测试 + 端到端回归测试：锁定「重构不改行为」。"""
from pathlib import Path

from insightdesk.loader import load_tickets
from insightdesk.metrics import compute_metrics
from insightdesk.report import render_report

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_render_report_format():
    metrics = {
        "total": 2,
        "channels": {"email": 1, "web": 1},
        "avg_resolution_hours": 1.5,
        "unresolved": 1,
    }
    assert render_report(metrics).split("\n") == [
        "=== InsightDesk 工单统计报表 ===",
        "总工单数: 2",
        "未解决工单数: 1",
        "平均解决时长(小时): 1.5",
        "按渠道分布:",
        "  email: 1",
        "  web: 1",
    ]


def test_render_report_rounds_avg_hours():
    metrics = {"total": 1, "channels": {}, "avg_resolution_hours": 1.005, "unresolved": 0}
    assert "平均解决时长(小时): 1.0" in render_report(metrics)


def test_sample_csv_output_matches_baseline():
    """回归测试：样例数据跑完整流水线，输出必须和重构前基线一致。"""
    rows = load_tickets(REPO_ROOT / "data" / "tickets_sample.csv")
    output = render_report(compute_metrics(rows)) + "\n"
    baseline = (REPO_ROOT / "data" / "baseline_output.txt").read_text(encoding="utf-8")
    assert output == baseline
