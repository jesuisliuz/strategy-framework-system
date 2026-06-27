"""
Tier1 五看分析引擎 (L1-L5)

核心升级：
1. 多 Agent 并行（inspired by claude-code-best-practice Superpowers）
   - 每个五看步骤支持 2-3 个并行 subagent，各自独立搜索+独立结论
   - 通过 skill_interface.delegate_parallel 实现批量并行
2. 多视角冲突模式（inspired by ai-berkshire）
   - L3 看竞争：进攻方/防守方/中立观察者 三视角，结论有张力才暴露盲点
3. 反偏见机制（inspired by ai-berkshire）
   - 信息丰富度评级（A/B/C）
   - 快速否决清单（8 条红线）
   - 留白原则（不确定就说"不知道"）
"""

from typing import Optional


def _build_parallel_prompt(step_id: str, subagent_config: dict, topic: str, context: str) -> str:
    """构建并行 subagent 的 prompt。"""
    perspective = subagent_config.get("perspective", "")
    role_desc = subagent_config.get("role", "")
    skills = subagent_config.get("skills", [])
    frameworks = subagent_config.get("mbb_frameworks", [])

    prompt = f"""## 角色：{subagent_config['name']}

**视角**：{perspective or '独立分析'}
**职责**：{role_desc}

**分析主题**：{topic}

**背景信息**：
{context}

**可用框架**：{', '.join(frameworks) if frameworks else '无特定框架，自由分析'}

**分析要求**：
1. 基于你的视角进行独立分析，不参考其他视角的结论
2. 使用至少 2 个独立信息源交叉验证关键数据
3. 对信息丰富度进行评级（A=数据充分，B=数据有限，C=数据不足）
4. 如果数据不足，明确标注"信息不足，无法判断"，不要编造
5. 给出明确结论，不要模棱两可

**输出格式**：
### 分析结论
（你的核心判断，2-3 句话）

### 关键发现
（3-5 个要点，每个带信息丰富度评级 A/B/C）

### 数据支撑
（引用来源和数据）

### 不确定性
（哪些地方数据不足，需要进一步验证）
"""
    return prompt


def _apply_quick_veto_checklist(content: str, step_id: str) -> list:
    """快速否决清单（ai-berkshire 模式）。

    8 条红线，命中即标记。用于 L3 看竞争和 L5 看机会。
    """
    veto_items = [
        ("管理层诚信问题", ["诚信", "造假", "欺诈", "违规", "处罚"]),
        ("商业模式不可持续", ["亏损", "烧钱", "不可持续", "依赖补贴"]),
        ("护城河缺失", ["无壁垒", "同质化", "可替代", "无差异化"]),
        ("市场萎缩", ["衰退", "萎缩", "下降", "夕阳"]),
        ("政策风险", ["监管", "政策", "合规", "反垄断"]),
        ("技术替代风险", ["颠覆", "替代", "淘汰", "过时"]),
        ("财务造假嫌疑", ["财务", "审计", "异常", "质疑"]),
        ("行业集中度极低", ["分散", "碎片化", "无龙头"]),
    ]

    flagged = []
    content_lower = content.lower()
    for name, keywords in veto_items:
        if any(kw in content_lower for kw in keywords):
            flagged.append(name)

    return flagged


def _apply_reverse_testing(content: str, topic: str) -> str:
    """芒格式逆向测试（ai-berkshire 模式）。

    对分析结论进行"死法"分析：战略有哪 5 种死法？
    """
    return f"""
---
## 逆向测试：我们的战略有哪 5 种死法？

**分析主题**：{topic}

基于以上分析，用芒格式逆向思维思考：

1. **死法一**：（最可能的失败路径）
   - 概率：高/中/低
   - 触发条件：
   - 预防措施：

2. **死法二**：
   - 概率：高/中/低
   - 触发条件：
   - 预防措施：

3. **死法三**：
   - 概率：高/中/低
   - 触发条件：
   - 预防措施：

4. **死法四**：
   - 概率：高/中/低
   - 触发条件：
   - 预防措施：

5. **死法五**：
   - 概率：高/中/低
   - 触发条件：
   - 预防措施：

---
"""


def _synthesize_parallel_results(step_id: str, results: list, topic: str) -> str:
    """综合多 Agent 并行结果。

    对比各视角结论，识别共识与分歧，给出最终判断。
    """
    synthesis = f"""
---
## 多视角综合判断

**分析主题**：{topic}

### 各视角结论对比

"""
    for r in results:
        name = r.get("name", "未知")
        conclusion = r.get("conclusion", "无结论")
        confidence = r.get("confidence", "未知")
        synthesis += f"**{name}**：{conclusion}（置信度：{confidence}）\n\n"

    # 识别共识与分歧
    synthesis += """
### 共识与分歧

**共识**：（各视角一致的观点）
（待填充）

**分歧**：（各视角矛盾的观点——这些矛盾点值得深入调查）
（待填充）

**最终判断**：
（基于共识+分歧分析，给出明确结论）
（待填充）
"""
    return synthesis


# =============================================================================
# 五看分析函数
# =============================================================================


def analyze_L1_industry(fields: dict, upstream: dict, skill_interface) -> dict:
    """看行业/趋势 — Industry Trends + PESTEL + Deep Research

    升级点：3 个并行 subagent（宏观趋势/市场数据/技术演进）
    """
    topic = fields.get("topic", "行业趋势分析")
    context = fields.get("context", "")

    # 获取并行 subagent 配置
    from app.skill_registry import SkillRegistry
    subagents = SkillRegistry.get_parallel_subagents("L1_industry")

    # 并行调度
    if subagents:
        prompts = [
            _build_parallel_prompt("L1_industry", sa, topic, context)
            for sa in subagents
        ]
        results = skill_interface.delegate_parallel(
            prompts=prompts,
            agent_names=[sa["name"] for sa in subagents],
            context=context,
        )
        synthesis = _synthesize_parallel_results("L1_industry", results, topic)
    else:
        # 降级：单 agent
        result = skill_interface.call_skill(
            "sn-deep-research",
            prompt=f"分析 {topic} 的行业趋势，使用 PESTEL 和 Industry Trends 框架",
            context=context,
        )
        synthesis = result.get("content", "")

    return {
        "content": synthesis,
        "summary": f"{topic} 行业趋势分析完成",
        "artifacts": ["行业趋势报告", "价值转移分析图"],
        "skills_used": ["mbb-strategist(Industry Trends, PESTEL)", "sn-deep-research", "sn-search-academic"],
        "data": {"parallel_subagents": len(subagents) if subagents else 0},
    }


def analyze_L2_customer(fields: dict, upstream: dict, skill_interface) -> dict:
    """看客户 — Customer Journey + Personas + Social Search

    升级点：3 个并行 subagent（用户画像/客户旅程/口碑分析）
    """
    topic = fields.get("topic", "客户分析")
    context = fields.get("context", "")

    from app.skill_registry import SkillRegistry
    subagents = SkillRegistry.get_parallel_subagents("L2_customer")

    if subagents:
        prompts = [
            _build_parallel_prompt("L2_customer", sa, topic, context)
            for sa in subagents
        ]
        results = skill_interface.delegate_parallel(
            prompts=prompts,
            agent_names=[sa["name"] for sa in subagents],
            context=context,
        )
        synthesis = _synthesize_parallel_results("L2_customer", results, topic)
    else:
        result = skill_interface.call_skill(
            "sn-deep-research",
            prompt=f"分析 {topic} 的客户，使用 Customer Journey 和 Personas 框架",
            context=context,
        )
        synthesis = result.get("content", "")

    return {
        "content": synthesis,
        "summary": f"{topic} 客户分析完成",
        "artifacts": ["客户细分报告", "市场交易地图"],
        "skills_used": ["mbb-strategist(Customer Journey, Personas)", "sn-deep-research", "sn-search-social-cn", "sn-search-social-en"],
        "data": {"parallel_subagents": len(subagents) if subagents else 0},
    }


def analyze_L3_competition(fields: dict, upstream: dict, skill_interface) -> dict:
    """看竞争 — SWOT + Porter's Five Forces + Code Search

    升级点：
    1. 3 视角冲突模式（进攻方/防守方/中立观察者）
    2. 快速否决清单（8 条红线）
    3. 信息丰富度评级（A/B/C）
    """
    topic = fields.get("topic", "竞争分析")
    context = fields.get("context", "")

    from app.skill_registry import SkillRegistry
    subagents = SkillRegistry.get_parallel_subagents("L3_competition")

    # 并行调度三视角
    if subagents:
        prompts = [
            _build_parallel_prompt("L3_competition", sa, topic, context)
            for sa in subagents
        ]
        results = skill_interface.delegate_parallel(
            prompts=prompts,
            agent_names=[sa["name"] for sa in subagents],
            context=context,
        )
        synthesis = _synthesize_parallel_results("L3_competition", results, topic)
    else:
        result = skill_interface.call_skill(
            "sn-deep-research",
            prompt=f"分析 {topic} 的竞争格局，使用 SWOT 和 Porter's Five Forces 框架",
            context=context,
        )
        synthesis = result.get("content", "")

    # 快速否决清单检查
    veto_flags = _apply_quick_veto_checklist(synthesis, "L3_competition")
    if veto_flags:
        synthesis += f"\n\n⚠️ **快速否决清单触发**：{', '.join(veto_flags)}\n"

    return {
        "content": synthesis,
        "summary": f"{topic} 竞争分析完成",
        "artifacts": ["竞争格局报告", "竞品对比矩阵"],
        "skills_used": ["mbb-strategist(SWOT, Porter's)", "sn-deep-research", "sn-search-code"],
        "data": {
            "parallel_subagents": len(subagents) if subagents else 0,
            "veto_flags": veto_flags,
        },
    }


def analyze_L4_internal(fields: dict, upstream: dict, skill_interface) -> dict:
    """看自己 — SWOT + Excel数据分析"""
    topic = fields.get("topic", "内部能力评估")
    context = fields.get("context", "")

    result = skill_interface.call_skill(
        "mbb-strategist",
        prompt=f"分析 {topic}，使用 SWOT 框架评估内部能力",
        context=context,
    )

    return {
        "content": result.get("content", ""),
        "summary": f"{topic} 内部能力评估完成",
        "artifacts": ["能力评估报告"],
        "skills_used": ["mbb-strategist(SWOT)", "excel-data-analysis"],
        "data": {},
    }


def analyze_L5_opportunity(fields: dict, upstream: dict, skill_interface) -> dict:
    """看机会 — Risk & Scenario + SPAN矩阵可视化

    升级点：快速否决清单 + 留白原则
    """
    topic = fields.get("topic", "机会分析")
    context = fields.get("context", "")

    result = skill_interface.call_skill(
        "mbb-strategist",
        prompt=f"分析 {topic}，使用 Risk & Scenario 框架识别机会与风险",
        context=context,
    )
    synthesis = result.get("content", "")

    # 快速否决清单检查
    veto_flags = _apply_quick_veto_checklist(synthesis, "L5_opportunity")
    if veto_flags:
        synthesis += f"\n\n⚠️ **快速否决清单触发**：{', '.join(veto_flags)}\n"

    return {
        "content": synthesis,
        "summary": f"{topic} 机会分析完成",
        "artifacts": ["SPAN机会矩阵"],
        "skills_used": ["mbb-strategist(Risk & Scenario)", "excel-bar-chart-visualization"],
        "data": {"veto_flags": veto_flags},
    }