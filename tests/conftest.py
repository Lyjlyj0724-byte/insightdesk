"""pytest 公共夹具：测试数据准备集中在这里，测试函数只写断言。"""
import sys
from pathlib import Path

import pytest

# 让测试在未安装包的情况下也能 import insightdesk
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


def make_row(id="1", channel="email", priority="medium",
             created_at="2026-08-01 09:00:00",
             resolved_at="2026-08-01 10:30:00"):
    """构造一行工单 dict，默认是一条 1.5 小时解决的 email 工单。"""
    return {
        "id": id,
        "title": "测试工单",
        "body": "测试内容",
        "priority": priority,
        "created_at": created_at,
        "resolved_at": resolved_at,
        "channel": channel,
    }


@pytest.fixture
def row():
    return make_row


@pytest.fixture
def five_rows():
    """手算好的 5 行小数据集：

    - 3 条已解决：1.5h、2.5h、2.0h → 平均 2.0h
    - 2 条未解决
    - 渠道：email×2、web×2、api×1
    """
    return [
        make_row(id="1", channel="email",
                 created_at="2026-08-01 09:00:00", resolved_at="2026-08-01 10:30:00"),  # 1.5h
        make_row(id="2", channel="web",
                 created_at="2026-08-01 09:00:00", resolved_at="2026-08-01 11:30:00"),  # 2.5h
        make_row(id="3", channel="email",
                 created_at="2026-08-01 09:00:00", resolved_at="2026-08-01 11:00:00"),  # 2.0h
        make_row(id="4", channel="web", resolved_at=""),
        make_row(id="5", channel="api", resolved_at=""),
    ]
