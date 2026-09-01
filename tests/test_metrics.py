"""metrics.py 的单元测试：正常路径、边界情况、异常输入。"""
import pytest

from insightdesk.metrics import (
    avg_resolution_hours,
    compute_metrics,
    count_by_channel,
    count_by_priority,
    count_total,
    count_unresolved,
)

# ---------- 正常路径：已知输入 → 断言已知输出 ----------

@pytest.mark.parametrize("n", [0, 1, 5])
def test_count_total(row, n):
    rows = [row(id=str(i)) for i in range(n)]
    assert count_total(rows) == n


def test_count_by_channel(five_rows):
    assert count_by_channel(five_rows) == {"email": 2, "web": 2, "api": 1}


def test_count_by_channel_keeps_first_seen_order(five_rows):
    # dict 保持插入顺序，报表按渠道首次出现顺序输出
    assert list(count_by_channel(five_rows)) == ["email", "web", "api"]


def test_avg_resolution_hours_hand_computed(five_rows):
    # (1.5 + 2.5 + 2.0) / 3 = 2.0
    assert avg_resolution_hours(five_rows) == pytest.approx(2.0)


def test_count_unresolved(five_rows):
    assert count_unresolved(five_rows) == 2


def test_compute_metrics_returns_all_keys(five_rows):
    metrics = compute_metrics(five_rows)
    assert set(metrics) == {
        "total", "channels", "priorities", "avg_resolution_hours", "unresolved",
    }
    assert metrics["total"] == 5


# ---------- 边界情况 ----------

def test_empty_rows():
    metrics = compute_metrics([])
    assert metrics["total"] == 0
    assert metrics["channels"] == {}
    assert metrics["avg_resolution_hours"] == 0
    assert metrics["unresolved"] == 0


def test_avg_resolution_hours_none_resolved(row):
    rows = [row(resolved_at=""), row(id="2", resolved_at="")]
    assert avg_resolution_hours(rows) == 0


def test_avg_resolution_hours_ignores_unresolved(row):
    rows = [
        row(resolved_at="2026-08-01 12:00:00"),  # 3.0h
        row(id="2", resolved_at=""),             # 未解决，不参与平均
    ]
    assert avg_resolution_hours(rows) == pytest.approx(3.0)


@pytest.mark.parametrize("resolved_at,expected", [
    ("", 1),                          # 空字符串 = 未解决
    (None, 1),                        # None = 未解决
    ("2026-08-01 10:30:00", 0),       # 有时间 = 已解决
])
def test_count_unresolved_semantics(row, resolved_at, expected):
    assert count_unresolved([row(resolved_at=resolved_at)]) == expected


# ---------- 异常输入：当前行为是直接抛错，用测试把这个行为钉住 ----------

def test_avg_resolution_hours_bad_time_string_raises(row):
    rows = [row(resolved_at="not-a-time")]
    with pytest.raises(ValueError):
        avg_resolution_hours(rows)


def test_count_by_channel_missing_column_raises(row):
    r = row()
    del r["channel"]
    with pytest.raises(KeyError):
        count_by_channel([r])


# ---------- 按优先级分组（issue #6）----------

def test_count_by_priority(five_rows):
    # five_rows 全部是默认 priority="medium"
    assert count_by_priority(five_rows) == {"medium": 5}


def test_count_by_priority_mixed(row):
    rows = [row(priority="high"), row(id="2", priority="low"), row(id="3", priority="high")]
    assert count_by_priority(rows) == {"high": 2, "low": 1}
    assert list(count_by_priority(rows)) == ["high", "low"]  # 保持首次出现顺序
