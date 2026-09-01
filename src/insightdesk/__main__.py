"""__main__.py —— 命令行入口：python -m insightdesk <tickets.csv>。

串联 loader → metrics → report 三层。
"""
import sys

from .loader import load_tickets
from .metrics import compute_metrics
from .report import print_report


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 1:
        print("用法: python analyze.py <tickets.csv>")
        sys.exit(1)
    rows = load_tickets(argv[0])
    metrics = compute_metrics(rows)
    print_report(metrics)


if __name__ == "__main__":
    main()
