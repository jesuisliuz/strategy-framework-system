# Task 7: 触发词引擎与优先级路由

> **对应文档**: 七、使用指南 — 触发词 + 技能调用优先级

**Files:**
- Create: `app/trigger_router.py`

## Step 1: 触发词映射表

```python
TRIGGER_MAP = {
    "战略洞察": {
        "triggers": ["做战略洞察", "五看分析", "看行业", "看客户", "看竞争", "战略分析", "行业洞察"],
        "skills": ["sn-deep-research", "mbb-strategist"],
        "tier": "tier1",
    },
    "战略解码": {
        "triggers": ["做战略解码", "BEM解码", "设计KPI", "分解重点工作", "战略解码", "BEM"],
        "skills": ["excel-data-analysis", "planning-with-files"],
        "tier": "tier2",
    },
    "执行监控": {
        "triggers": ["跟踪执行进度", "经营分析", "战略复盘", "执行监控", "进度跟踪"],
        "skills": ["planning-with-files", "excel-data-analysis"],
        "tier": "tier3",
    },
    "竞品分析": {
        "triggers": ["竞品分析", "竞争格局", "竞争对手"],
        "skills": ["mbb-strategist", "sn-search-code"],
        "tier": "tier1",
    },
    "行业研究": {
        "triggers": ["行业研究", "深度研究", "行业分析"],
        "skills": ["sn-deep-research"],
        "tier": "tier1",
    },
}
```

## Step 2: 技能优先级系统

```python
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
    "excel-analysis": {
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
```

## Step 3: TriggerRouter 类

```python
class TriggerRouter:
    @staticmethod
    def match_triggers(user_input: str) -> list:
        """匹配触发词，返回匹配的场景列表"""
        
    @staticmethod
    def get_skills_for_scenario(scenario: str) -> list:
        """获取场景对应的技能调用列表"""
        
    @staticmethod
    def get_priority_chain(scenario: str) -> list:
        """获取按优先级排序的技能调用链"""
        
    @staticmethod
    def suggest_entry_point(user_input: str) -> str:
        """根据触发词建议最佳入口步骤ID"""
```

## Step 4: API端点

```python
@app.route("/api/trigger/match", methods=["POST"])
def match_trigger():
    """POST {user_input} → 返回匹配场景+推荐技能+入口步骤"""
```

## Step 5: Commit

```bash
git add -A && git commit -m "feat: trigger router + priority system (matching user spec section 7)"
```
