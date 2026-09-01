# InsightDesk

[![CI](https://github.com/Lyjlyj0724-byte/insightdesk/actions/workflows/ci.yml/badge.svg)](https://github.com/Lyjlyj0724-byte/insightdesk/actions/workflows/ci.yml)

工单统计报表工具：读取工单 CSV，输出总量、未解决数、平均解决时长和渠道分布的纯文本报表。

本项目是工程纪律练习仓库（Git / pytest / CI），从一份"能跑但很乱"的单文件脚本起步，逐步重构成可协作的工程仓库。

## 安装

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -e ".[dev]"   # M2 引入 pyproject.toml 后可用
```

M1 阶段脚本无第三方依赖，Python 3.10+ 直接可跑。

## 运行

```bash
python analyze.py data/tickets_sample.csv
```

输出示例：

```
=== InsightDesk 工单统计报表 ===
总工单数: 8
未解决工单数: 3
平均解决时长(小时): 15.99
按渠道分布:
  email: 2
  web: 3
  api: 2
  phone: 1
```

## CSV 格式

必须包含列：`id, title, body, priority, created_at, resolved_at, channel`。
时间格式 `%Y-%m-%d %H:%M:%S`；`resolved_at` 为空表示工单未解决。

## 数据文件

`data/` 目录与 `*.csv` 已被 `.gitignore` 忽略，不会进入版本库。
`data/baseline_output.txt` 是重构前的输出基线，用于回归测试。

## 路线图

- [x] M1：仓库初始化
- [ ] M2：拆分模块（loader / metrics / report）
- [ ] M3：pytest 测试覆盖
- [ ] M4：GitHub Actions CI + 分支保护
- [ ] M5：issue → PR 全流程协作演练
