"""
L1 战略洞察报告生成器

核心升级（inspired by google-labs-code/design.md）：
- 双层结构：YAML front matter（机器可读战略 token）+ Markdown prose（人可读战略意图）
- Token 层供 Tier2 BEM 直接读取（CSF/KPI 导出无需重新解析文本）
- Prose 层供人类阅读（完整分析报告）

报告结构：8 章，10,000-30,000 字
"""

from datetime import datetime
from typing import Any


# =============================================================================
# 1. Token Schema（机器可读战略 token）
# =============================================================================

def _extract_tokens(ctx: dict) -> dict:
    """从各步骤输出中提取结构化战略 token。

    类似 DESIGN.md 的 token 层，供下游（Tier2 BEM）直接消费。
    """
    tokens = {
        "report": {
            "title": ctx.get("project_name", "战略洞察报告"),
            "generated_at": datetime.now().isoformat(),
            "word_count": 0,  # 填充后更新
        },
        "industry": {
            "market_size": _safe_get(ctx, "L1_industry", "market_size"),
            "growth_rate": _safe_get(ctx, "L1_industry", "growth_rate"),
            "key_trends": _safe_get_list(ctx, "L1_industry", "key_trends"),
            "pestel_scores": _safe_get_dict(ctx, "L1_industry", "pestel_scores"),
        },
        "customer": {
            "personas": _safe_get_list(ctx, "L2_customer", "personas"),
            "key_segments": _safe_get_list(ctx, "L2_customer", "key_segments"),
            "journey_stages": _safe_get_list(ctx, "L2_customer", "journey_stages"),
        },
        "competition": {
            "competitors": _safe_get_list(ctx, "L3_competition", "competitors"),
            "moat_assessment": _safe_get_dict(ctx, "L3_competition", "moat_assessment"),
            "porter_scores": _safe_get_dict(ctx, "L3_competition", "porter_scores"),
            "veto_flags": _safe_get_list(ctx, "L3_competition", "veto_flags"),
        },
        "internal": {
            "strengths": _safe_get_list(ctx, "L4_internal", "strengths"),
            "weaknesses": _safe_get_list(ctx, "L4_internal", "weaknesses"),
            "capability_gaps": _safe_get_list(ctx, "L4_internal", "capability_gaps"),
        },
        "opportunity": {
            "opportunities": _safe_get_list(ctx, "L5_opportunity", "opportunities"),
            "span_matrix": _safe_get_dict(ctx, "L5_opportunity", "span_matrix"),
            "veto_flags": _safe_get_list(ctx, "L5_opportunity", "veto_flags"),
        },
        "strategy": {
            "objectives": _safe_get_list(ctx, "L6_objective", "objectives"),
            "positioning": _safe_get(ctx, "L7_strategy", "positioning"),
            "gtm_strategy": _safe_get(ctx, "L7_strategy", "gtm_strategy"),
            "pricing_strategy": _safe_get(ctx, "L7_strategy", "pricing_strategy"),
            "control_points": _safe_get_list(ctx, "L8_control", "control_points"),
        },
    }
    return tokens


def _safe_get(ctx: dict, step_id: str, key: str, default: Any = None) -> Any:
    """安全获取步骤输出中的字段。"""
    step_data = ctx.get("steps", {}).get(step_id, {}).get("data", {})
    return step_data.get(key, default)


def _safe_get_list(ctx: dict, step_id: str, key: str, default: list = None) -> list:
    """安全获取列表字段。"""
    val = _safe_get(ctx, step_id, key)
    if isinstance(val, list):
        return val
    if val is not None:
        return [val]
    return default or []


def _safe_get_dict(ctx: dict, step_id: str, key: str, default: dict = None) -> dict:
    """安全获取字典字段。"""
    val = _safe_get(ctx, step_id, key)
    if isinstance(val, dict):
        return val
    return default or {}


# =============================================================================
# 2. YAML Front Matter 生成
# =============================================================================

def _generate_yaml_frontmatter(tokens: dict) -> str:
    """生成 YAML front matter（机器可读 token 层）。

    类似 DESIGN.md 的 YAML front matter，供 agent 直接解析。
    """
    import yaml

    # 只输出非空字段，减少噪音
    clean_tokens = {}
    for section_name, section_data in tokens.items():
        if isinstance(section_data, dict):
            clean_section = {k: v for k, v in section_data.items() if v is not None}
            if clean_section:
                clean_tokens[section_name] = clean_section
        elif section_data is not None:
            clean_tokens[section_name] = section_data

    yaml_str = yaml.dump(
        clean_tokens,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )
    return f"---\n{yaml_str}---"


# =============================================================================
# 3. Markdown Prose 生成（人可读战略意图）
# =============================================================================

def _generate_markdown_prose(ctx: dict, tokens: dict) -> str:
    """生成 Markdown prose（人可读战略意图层）。

    类似 DESIGN.md 的 Markdown prose，解释 token 背后的战略意图。
    """
    project_name = ctx.get("project_name", "战略洞察报告")
    steps = ctx.get("steps", {})

    lines = [
        f"# {project_name} 战略洞察报告（L1）",
        "",
        "*五看三定 · 第一级产出 | 目标字数: 10,000-30,000字*",
        "",
        "---",
        "",
    ]

    # 一、执行摘要
    lines += [
        "## 一、执行摘要",
        "",
        _generate_executive_summary(ctx, tokens),
        "",
    ]

    # 二、看行业/趋势
    lines += [
        "## 二、看行业/趋势",
        "",
        _section_from_step(ctx, steps, "L1_industry"),
        "",
        "### 宏观环境分析（PESTEL）",
        _pestel_section(tokens.get("industry", {}).get("pestel_scores", {})),
        "",
        "### 行业趋势分析（Industry Trends）",
        _trends_section(tokens.get("industry", {}).get("key_trends", [])),
        "",
        "### 价值转移趋势",
        _value_transfer_section(tokens.get("industry", {})),
        "",
        "### 数据来源与证据",
        _evidence_section(ctx, "L1_industry"),
        "",
    ]

    # 三、看客户
    lines += [
        "## 三、看客户",
        "",
        _section_from_step(ctx, steps, "L2_customer"),
        "",
        "### 客户细分（Personas）",
        _personas_section(tokens.get("customer", {}).get("personas", [])),
        "",
        "### 客户购买行为分析（Customer Journey）",
        _journey_section(tokens.get("customer", {}).get("journey_stages", [])),
        "",
        "### 市场交易地图",
        _market_map_section(tokens.get("customer", {})),
        "",
        "### 需求层次分析（requirements/wants/pains）",
        _needs_section(tokens.get("customer", {})),
        "",
    ]

    # 四、看竞争
    lines += [
        "## 四、看竞争",
        "",
        _section_from_step(ctx, steps, "L3_competition"),
        "",
        "### 竞争格局分析（Porter's Five Forces）",
        _porter_section(tokens.get("competition", {}).get("porter_scores", {})),
        "",
        "### 竞品对比（SWOT）",
        _competitors_section(tokens.get("competition", {}).get("competitors", [])),
        "",
        "### 竞争策略建议",
        _competition_strategy_section(tokens.get("competition", {})),
        "",
        "### 快速否决清单",
        _veto_section(tokens.get("competition", {}).get("veto_flags", [])),
        "",
    ]

    # 五、看自己
    lines += [
        "## 五、看自己",
        "",
        _section_from_step(ctx, steps, "L4_internal"),
        "",
        "### 自身优势分析（SWOT-S）",
        _strengths_section(tokens.get("internal", {}).get("strengths", [])),
        "",
        "### 自身劣势分析（SWOT-W）",
        _weaknesses_section(tokens.get("internal", {}).get("weaknesses", [])),
        "",
        "### 能力差距分析",
        _gaps_section(tokens.get("internal", {}).get("capability_gaps", [])),
        "",
    ]

    # 六、看机会
    lines += [
        "## 六、看机会",
        "",
        _section_from_step(ctx, steps, "L5_opportunity"),
        "",
        "### 机会识别",
        _opportunities_section(tokens.get("opportunity", {}).get("opportunities", [])),
        "",
        "### SPAN矩阵分析",
        _span_section(tokens.get("opportunity", {}).get("span_matrix", {})),
        "",
        "### 机会优先级排序",
        _priority_section(tokens.get("opportunity", {})),
        "",
        "### 快速否决清单",
        _veto_section(tokens.get("opportunity", {}).get("veto_flags", [])),
        "",
    ]

    # 七、三定
    lines += [
        "## 七、三定",
        "",
        "### 定目标",
        _section_from_step(ctx, steps, "L6_objective"),
        _objectives_section(tokens.get("strategy", {}).get("objectives", [])),
        "",
        "### 定策略（GTM/Pricing）",
        _section_from_step(ctx, steps, "L7_strategy"),
        _strategy_section(tokens.get("strategy", {})),
        "",
        "### 定控制点",
        _section_from_step(ctx, steps, "L8_control"),
        _control_points_section(tokens.get("strategy", {}).get("control_points", [])),
        "",
    ]

    # 八、数据来源与证据
    lines += [
        "## 八、数据来源与证据",
        "",
        _generate_evidence_section(ctx),
        "",
        "---",
        "",
        f"*报告生成时间: {datetime.now().isoformat()}*",
        "",
        "*技能调用: sn-deep-research + mbb-strategist + sn-search系列 + Excel分析系列*",
        "",
    ]

    return "\n".join(lines)


# =============================================================================
# 4. 章节辅助函数
# =============================================================================

def _section_from_step(ctx: dict, steps: dict, step_id: str) -> str:
    """从步骤输出中提取内容。"""
    step = steps.get(step_id, {})
    output = step.get("output", {})
    if output.get("status") in ("done", "stale"):
        return output.get("content", "*（该步骤尚未完成分析）*")
    return "*（该步骤尚未完成分析）*"


def _generate_executive_summary(ctx: dict, tokens: dict) -> str:
    """生成执行摘要。"""
    industry = tokens.get("industry", {})
    strategy = tokens.get("strategy", {})
    competition = tokens.get("competition", {})

    market_size = industry.get("market_size", "待分析")
    growth_rate = industry.get("growth_rate", "待分析")
    positioning = strategy.get("positioning", "待确定")
    veto_flags = competition.get("veto_flags", [])

    summary = f"""
**核心判断**：{ctx.get('project_name', '该项目')} 处于一个 {market_size}、年增长率 {growth_rate} 的市场中。

**战略定位**：{positioning}。

**关键机会**：
{chr(10).join(f'- {o}' for o in tokens.get('opportunity', {}).get('opportunities', ['待分析']))}

**主要风险**：
{chr(10).join(f'- {v}' for v in (veto_flags if veto_flags else ['待分析']))}

**建议行动**：
1. 优先验证 {positioning} 定位的市场接受度
2. 建立 {strategy.get('control_points', ['待确定'])[0] if strategy.get('control_points') else '待确定'} 作为核心控制点
3. 持续监控竞争格局变化
"""
    return summary.strip()


def _pestel_section(scores: dict) -> str:
    """PESTEL 分析章节。"""
    if not scores:
        return "*（数据不足，无法生成 PESTEL 分析）*"

    labels = {
        "political": "政治（Political）",
        "economic": "经济（Economic）",
        "social": "社会（Social）",
        "technological": "技术（Technological）",
        "environmental": "环境（Environmental）",
        "legal": "法律（Legal）",
    }

    lines = []
    for key, label in labels.items():
        score = scores.get(key)
        if score is not None:
            impact = "高" if score >= 4 else "中" if score >= 2 else "低"
            lines.append(f"- **{label}**：影响度 {score}/5（{impact}）")

    return "\n".join(lines) if lines else "*（数据不足，无法生成 PESTEL 分析）*"


def _trends_section(trends: list) -> str:
    """行业趋势章节。"""
    if not trends:
        return "*（数据不足，无法生成趋势分析）*"
    return "\n".join(f"- {t}" for t in trends)


def _value_transfer_section(industry: dict) -> str:
    """价值转移趋势章节。"""
    return "*（需基于行业分析数据生成价值转移趋势）*"


def _evidence_section(ctx: dict, step_id: str) -> str:
    """数据来源与证据章节。"""
    step = ctx.get("steps", {}).get(step_id, {})
    skills_used = step.get("output", {}).get("skills_used", [])
    if skills_used:
        return "\n".join(f"- {s}" for s in skills_used)
    return "*（数据来源待补充）*"


def _personas_section(personas: list) -> str:
    """客户画像章节。"""
    if not personas:
        return "*（数据不足，无法生成客户画像）*"
    return "\n".join(f"- {p}" for p in personas)


def _journey_section(stages: list) -> str:
    """客户旅程章节。"""
    if not stages:
        return "*（数据不足，无法生成客户旅程分析）*"
    return "\n".join(f"- {s}" for s in stages)


def _market_map_section(customer: dict) -> str:
    """市场交易地图章节。"""
    segments = customer.get("key_segments", [])
    if segments:
        return "\n".join(f"- {s}" for s in segments)
    return "*（需基于客户分析数据生成市场交易地图）*"


def _needs_section(customer: dict) -> str:
    """需求层次分析章节。"""
    return "*（需基于客户分析数据生成需求层次分析）*"


def _porter_section(scores: dict) -> str:
    """波特五力分析章节。"""
    if not scores:
        return "*（数据不足，无法生成波特五力分析）*"

    labels = {
        "rivalry": "同业竞争",
        "suppliers": "供应商议价能力",
        "buyers": "买方议价能力",
        "substitutes": "替代品威胁",
        "new_entries": "新进入者威胁",
    }

    lines = []
    for key, label in labels.items():
        score = scores.get(key)
        if score is not None:
            intensity = "高" if score >= 4 else "中" if score >= 2 else "低"
            lines.append(f"- **{label}**：{score}/5（{intensity}）")

    return "\n".join(lines) if lines else "*（数据不足，无法生成波特五力分析）*"


def _competitors_section(competitors: list) -> str:
    """竞品对比章节。"""
    if not competitors:
        return "*（数据不足，无法生成竞品对比）*"
    return "\n".join(f"- {c}" for c in competitors)


def _competition_strategy_section(competition: dict) -> str:
    """竞争策略建议章节。"""
    return "*（需基于竞争分析数据生成策略建议）*"


def _veto_section(veto_flags: list) -> str:
    """快速否决清单章节。"""
    if not veto_flags:
        return "*（无否决项触发）*"
    return "\n".join(f"⚠️ {v}" for v in veto_flags)


def _strengths_section(strengths: list) -> str:
    """优势分析章节。"""
    if not strengths:
        return "*（数据不足，无法生成优势分析）*"
    return "\n".join(f"- {s}" for s in strengths)


def _weaknesses_section(weaknesses: list) -> str:
    """劣势分析章节。"""
    if not weaknesses:
        return "*（数据不足，无法生成劣势分析）*"
    return "\n".join(f"- {w}" for w in weaknesses)


def _gaps_section(gaps: list) -> str:
    """能力差距章节。"""
    if not gaps:
        return "*（数据不足，无法生成能力差距分析）*"
    return "\n".join(f"- {g}" for g in gaps)


def _opportunities_section(opportunities: list) -> str:
    """机会识别章节。"""
    if not opportunities:
        return "*（数据不足，无法生成机会识别）*"
    return "\n".join(f"- {o}" for o in opportunities)


def _span_section(span: dict) -> str:
    """SPAN 矩阵章节。"""
    if not span:
        return "*（数据不足，无法生成 SPAN 矩阵）*"
    return f"SPAN 矩阵数据：{span}"


def _priority_section(opportunity: dict) -> str:
    """机会优先级章节。"""
    return "*（需基于机会分析数据生成优先级排序）*"


def _objectives_section(objectives: list) -> str:
    """战略目标章节。"""
    if not objectives:
        return "*（数据不足，无法生成战略目标）*"
    return "\n".join(f"- {o}" for o in objectives)


def _strategy_section(strategy: dict) -> str:
    """策略章节。"""
    lines = []
    if strategy.get("gtm_strategy"):
        lines.append(f"**GTM 策略**：{strategy['gtm_strategy']}")
    if strategy.get("pricing_strategy"):
        lines.append(f"**定价策略**：{strategy['pricing_strategy']}")
    return "\n".join(lines) if lines else "*（数据不足，无法生成策略）*"


def _control_points_section(control_points: list) -> str:
    """控制点章节。"""
    if not control_points:
        return "*（数据不足，无法生成控制点）*"
    return "\n".join(f"- {cp}" for cp in control_points)


def _generate_evidence_section(ctx: dict) -> str:
    """数据来源与证据章节。"""
    steps = ctx.get("steps", {})
    lines = ["**所有数据来源列表**："]
    for step_id, step in steps.items():
        skills = step.get("output", {}).get("skills_used", [])
        if skills:
            lines.append(f"- {step_id}: {', '.join(skills)}")
    lines.append("")
    lines.append("**证据强弱判断**：")
    lines.append("- A 级（强证据）：多源交叉验证，数据一致")
    lines.append("- B 级（中等证据）：单一来源，需进一步验证")
    lines.append("- C 级（弱证据）：数据不足，仅供参考")
    return "\n".join(lines)


# =============================================================================
# 5. 主函数
# =============================================================================

def generate_L1_report(ctx: dict) -> str:
    """L1 战略洞察报告生成器 — 双层结构（token + prose）。

    类似 DESIGN.md 的格式：
    - YAML front matter：机器可读战略 token
    - Markdown prose：人可读战略意图

    Token 层供 Tier2 BEM 直接读取，无需重新解析文本。
    """
    tokens = _extract_tokens(ctx)
    frontmatter = _generate_yaml_frontmatter(tokens)
    prose = _generate_markdown_prose(ctx, tokens)

    # 更新字数统计
    total_chars = len(prose.replace(" ", "").replace("\n", ""))
    tokens["report"]["word_count"] = total_chars

    # 重新生成 frontmatter（含字数）
    frontmatter = _generate_yaml_frontmatter(tokens)

    return f"{frontmatter}\n\n{prose}"


def check_L1_requirements(report: str) -> dict:
    """L1 报告质量检查。"""
    # 分离 frontmatter 和 prose
    if report.startswith("---"):
        parts = report.split("---", 2)
        if len(parts) >= 3:
            prose = parts[2].strip()
        else:
            prose = report
    else:
        prose = report

    word_count = len(prose.replace(" ", "").replace("\n", ""))

    # 检查章节完整性
    required_chapters = [
        "执行摘要",
        "看行业",
        "看客户",
        "看竞争",
        "看自己",
        "看机会",
        "三定",
        "数据来源",
    ]
    chapters_present = [ch for ch in required_chapters if ch in prose]

    return {
        "total_chars": word_count,
        "meets_requirement": 10000 <= word_count <= 30000,
        "chapters_present": chapters_present,
        "chapters_missing": [ch for ch in required_chapters if ch not in prose],
        "has_yaml_frontmatter": report.startswith("---"),
    }