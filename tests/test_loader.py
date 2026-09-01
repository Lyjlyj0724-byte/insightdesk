"""loader.py 的测试：用 tmp_path 写临时 CSV，不依赖仓库里的数据文件。"""
import pytest

from insightdesk.loader import load_tickets

HEADER = "id,title,body,priority,created_at,resolved_at,channel\n"


def test_load_tickets_reads_all_rows(tmp_path):
    csv_file = tmp_path / "tickets.csv"
    csv_file.write_text(
        HEADER
        + "1,标题一,内容,high,2026-08-01 09:00:00,2026-08-01 10:00:00,email\n"
        + "2,标题二,内容,low,2026-08-01 09:00:00,,web\n",
        encoding="utf-8",
    )
    rows = load_tickets(csv_file)
    assert len(rows) == 2
    assert rows[0]["id"] == "1"
    assert rows[1]["channel"] == "web"
    assert rows[1]["resolved_at"] == ""


def test_load_tickets_header_only_returns_empty(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text(HEADER, encoding="utf-8")
    assert load_tickets(csv_file) == []


def test_load_tickets_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_tickets(tmp_path / "not-exist.csv")
