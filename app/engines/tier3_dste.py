"""
Tier3 DSTE 三层引擎 — SP/BP执行监控 + 经营分析会 + 战略复盘

升级点（D3 战略复盘）：
- 芒格式逆向测试：战略有哪 5 种死法？
"""


def analyze_D1_execution(fields: dict, upstream: dict, skill_interface) -> dict:
    return {"content": "⚠️ D1 执行监控 — 待实现", "summary": "D1 待实现", "artifacts": ["执行进度报告"], "skills_used": ["planning-with-files", "excel-line-chart-visualization"], "data": {}}


def analyze_D2_analysis(fields: dict, upstream: dict, skill_interface) -> dict:
    return {"content": "⚠️ D2 经营分析会 — 待实现", "summary": "D2 待实现", "artifacts": ["偏差分析报告"], "skills_used": ["excel-trend-analysis", "statistical-distribution-and-outlier-analysis"], "data": {}}


def analyze_D3_review(fields: dict, upstream: dict, skill_interface) -> dict:
    """战略复盘 — 含芒格式逆向测试"""
    topic = fields.get("topic", "战略复盘")
    context = fields.get("context", "")

    result = skill_interface.call_skill(
        "sn-research-synthesis",
        prompt=f"复盘 {topic}，提炼关键结论和经验教训",
        context=context,
    )
    synthesis = result.get("content", "")

    # 逆向测试
    from .tier1_five_looks import _apply_reverse_testing
    synthesis += _apply_reverse_testing(synthesis, topic)

    return {
        "content": synthesis,
        "summary": f"{topic} 战略复盘完成（含逆向测试）",
        "artifacts": ["战略复盘报告"],
        "skills_used": ["sn-research-synthesis"],
        "data": {"reverse_testing": True},
    }