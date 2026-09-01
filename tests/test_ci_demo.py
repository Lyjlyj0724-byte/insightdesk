"""CI 教学用：这个测试故意失败，用来演示「CI 红了 → 读日志 → 修复 → 变绿」。

下一个 commit 会修掉它。
"""


def test_deliberately_broken_for_ci_demo():
    assert 1 + 1 == 3, "故意写错的断言：演示 CI 失败时长什么样"
