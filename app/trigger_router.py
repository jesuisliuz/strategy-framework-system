"""
触发词引擎与优先级路由

核心设计：
- TRIGGER_MAP: 场景→触发词→技能→层级映射
- SKILL_PRIORITY: 技能调用优先级（1-4）
- TriggerRouter: 匹配触发词、获取技能链、建议入口步骤
"""

from typing import Optional


# =============================================================================
# 1. 触发词映射表
# =============================================================================

TRIGGER_MAP = {
    "战略洞察": {
        "triggers": [
            "做战略洞察", "五看分析", "看行业", "看客户", "看竞争",
            "战略分析", "行业洞察", "五看三定", "战略制定",
        ],
        "skills": ["sn-deep-research", "mbb-strategist"],
        "tier": "tier1",
        "entry_steps": ["L1_industry", "L2_customer", "L3_competition"],
    },
    "战略解码": {
        "triggers": [
            "做战略解码", "BEM解码", "设计KPI", "分解重点工作",
            "战略解码", "BEM", "CSF", "KPI设计", "PBC",
        ],
        "skills": ["excel-data-analysis", "planning-with-files"],
        "tier": "tier2",
        "entry_steps": ["B1_csf", "B2_kpi"],
    },
    "执行监控": {
        "triggers": [
            "跟踪执行进度", "经营分析", "战略复盘", "执行监控",
            "进度跟踪", "DSTE", "执行跟踪",
        ],
        "skills": ["planning-with-files", "excel-data-analysis"],
        "tier": "tier3",
        "entry_steps": ["D1_execution", "D2_analysis", "D3_review"],
    },
    "竞品分析": {
        "triggers": ["竞品分析", "竞争格局", "竞争对手", "竞争分析"],
        "skills": ["mbb-strategist", "sn-search-code"],
        "tier": "tier1",
        "entry_steps": ["L3_competition"],
    },
    "行业研究": {
        "triggers": ["行业研究", "深度研究", "行业分析", "市场研究"],
        "skills": ["sn-deep-research"],
        "tier": "tier1",
        "entry_steps": ["L1_industry"],
    },
    "能力评估": {
        "triggers": ["看自己", "能力评估", "内部分析", "SWOT分析"],
        "skills": ["mbb-strategist", "excel-data-analysis"],
        "tier": "tier1",
        "entry_steps": ["L4_internal"],
    },
    "机会分析": {
        "triggers": ["看机会", "机会分析", "SPAN矩阵", "机会识别"],
        "skills": ["mbb-strategist", "excel-bar-chart-visualization"],
        "tier": "tier1",
        "entry_steps": ["L5_opportunity"],
    },
    "战略制定": {
        "triggers": ["定目标", "定策略", "定控制点", "三定", "战略制定"],
        "skills": ["mbb-strategist"],
        "tier": "tier1",
        "entry_steps": ["L6_objective", "L7_strategy", "L8_control"],
    },
}


# =============================================================================
# 2. 技能优先级系统
# =============================================================================

SKILL_PRIORITY = {
    "sn-deep-research": {
        "priority": 1,
        "label": "第一优先级",
        "trigger_condition": "用户要求深度研究/行业研究/竞品分析",
        "description": "深度研究编排器 — 规划→取证→综合→成稿全流程",
    },
    "mbb-strategist": {
        "priority": 2,
        "label": "第二优先级",
        "trigger_condition": "用户要求战略分析/SWOT/PESTEL/波特五力",
        "description": "MBB战略框架 — SWOT/PESTEL/波特五力/GTM/定价/风险",
    },
    "excel-data-analysis": {
        "priority": 3,
        "label": "第三优先级",
        "trigger_condition": "用户要求数据分析/KPI设计/可视化",
        "description": "Excel数据分析系列 — 30+分析技能",
    },
    "planning-with-files": {
        "priority": 4,
        "label": "第四优先级",
        "trigger_condition": "多步骤任务/需要进度跟踪",
        "description": "文件化规划 — task_plan.md / findings.md / progress.md",
    },
}


# =============================================================================
# 3. TriggerRouter 类
# =============================================================================

class TriggerRouter:
    """触发词路由引擎。

    根据用户输入匹配场景，返回推荐技能链和入口步骤。
    """

    @staticmethod
    def match_triggers(user_input: str) -> list:
        """匹配触发词，返回匹配的场景列表（按匹配度排序）。

        匹配规则：
        1. 精确匹配（触发词完全包含在用户输入中）→ 最高优先级
        2. 部分匹配（用户输入包含触发词的一部分）→ 次优先级
        3. 关键词匹配（用户输入包含触发词中的关键词）→ 最低优先级
        """
        if not user_input:
            return []

        user_lower = user_input.lower()
        matches = []

        for scenario, config in TRIGGER_MAP.items():
            triggers = config.get("triggers", [])
            best_score = 0
            best_trigger = ""

            for trigger in triggers:
                trigger_lower = trigger.lower()
                if trigger_lower in user_lower:
                    # 精确匹配：触发词完全包含在用户输入中
                    score = len(trigger_lower) * 2
                    if score > best_score:
                        best_score = score
                        best_trigger = trigger
                elif any(word in user_lower for word in trigger_lower.split()):
                    # 部分匹配：用户输入包含触发词的一部分
                    score = len(trigger_lower)
                    if score > best_score:
                        best_score = score
                        best_trigger = trigger

            if best_score > 0:
                matches.append({
                    "scenario": scenario,
                    "matched_trigger": best_trigger,
                    "score": best_score,
                    "skills": config.get("skills", []),
                    "tier": config.get("tier", ""),
                    "entry_steps": config.get("entry_steps", []),
                })

        # 按匹配度排序
        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches

    @staticmethod
    def get_skills_for_scenario(scenario: str) -> list:
        """获取场景对应的技能调用列表。"""
        config = TRIGGER_MAP.get(scenario, {})
        return config.get("skills", [])

    @staticmethod
    def get_priority_chain(scenario: str) -> list:
        """获取按优先级排序的技能调用链。

        返回 [(skill_name, priority, description), ...]
        """
        skills = TriggerRouter.get_skills_for_scenario(scenario)
        chain = []
        for skill in skills:
            priority_info = SKILL_PRIORITY.get(skill, {})
            chain.append({
                "skill": skill,
                "priority": priority_info.get("priority", 99),
                "label": priority_info.get("label", ""),
                "description": priority_info.get("description", ""),
            })
        chain.sort(key=lambda x: x["priority"])
        return chain

    @staticmethod
    def suggest_entry_point(user_input: str) -> Optional[str]:
        """根据触发词建议最佳入口步骤ID。

        返回第一个匹配场景的第一个入口步骤。
        """
        matches = TriggerRouter.match_triggers(user_input)
        if matches:
            entry_steps = matches[0].get("entry_steps", [])
            if entry_steps:
                return entry_steps[0]
        return None

    @staticmethod
    def get_all_scenarios() -> dict:
        """获取所有场景配置（用于前端展示）。"""
        return TRIGGER_MAP

    @staticmethod
    def get_all_skills_with_priority() -> dict:
        """获取所有技能及其优先级（用于前端展示）。"""
        return SKILL_PRIORITY

    @staticmethod
    def get_scenario_for_step(step_id: str) -> Optional[str]:
        """根据步骤ID反查所属场景。"""
        for scenario, config in TRIGGER_MAP.items():
            if step_id in config.get("entry_steps", []):
                return scenario
        return None


# =============================================================================
# 4. API 辅助函数
# =============================================================================

def match_trigger_api(user_input: str) -> dict:
    """API 端点辅助函数。

    POST {user_input} → 返回匹配场景+推荐技能+入口步骤
    """
    matches = TriggerRouter.match_triggers(user_input)
    entry_point = TriggerRouter.suggest_entry_point(user_input)

    return {
        "user_input": user_input,
        "matches": matches,
        "recommended_entry_point": entry_point,
        "recommended_scenario": matches[0]["scenario"] if matches else None,
        "recommended_skills": matches[0]["skills"] if matches else [],
        "recommended_tier": matches[0]["tier"] if matches else None,
    }