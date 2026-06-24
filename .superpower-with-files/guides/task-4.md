# Task 4: 三层级数据模型

> **对应文档**: 框架全景图 → 第一/二/三层级数据建模

**Files:**
- Create: `app/models.py`

## Step 1: 三层级枚举定义

```python
TIER_DEFINITIONS = {
    "tier1": {
        "name": "五看三定",
        "subtitle": "战略洞察 + 战略制定",
        "timeframe": "4月-9月（7个月）",
        "core_skills": ["sn-deep-research", "mbb-strategist"],
        "aux_skills": ["sn-search系列", "Excel分析系列"],
        "output": "L1 战略洞察报告",
        "word_count": "10,000-30,000字",
    },
    "tier2": {
        "name": "BEM",
        "subtitle": "战略解码",
        "timeframe": "10月-12月（3个月）",
        "core_skills": ["Excel分析系列", "planning-with-files"],
        "aux_skills": [],
        "output": "L2 战略解码方案",
        "word_count": "5,000-10,000字",
    },
    "tier3": {
        "name": "DSTE",
        "subtitle": "全流程管理",
        "timeframe": "1月-12月（全年循环）",
        "core_skills": ["planning-with-files", "Excel分析系列"],
        "aux_skills": [],
        "output": "L3 落地执行方案",
        "word_count": "2,000-5,000字",
    },
}
```

## Step 2: 完整步骤定义 (19步)

包含: L1-L8(五看三定) + B1-B5(BEM六步法) + D1-D3(DSTE) + cross_validation + final_report

每个步骤定义包含: step_id, tier, number, name, method, core_task, skills(list), usage_method, outputs(list), input_fields(list), output_sections(list)

详细内容见 `app/data/step_definitions.json`（Task 6生成）。

## Step 3: AnalyzeContext 数据模型

```python
@dataclass
class AnalyzeContext:
    session_id: str
    project_name: str
    created_at: str
    current_tier: str  # tier1/tier2/tier3
    current_step: str
    
    # 三层级步骤数据
    tier1_steps: dict  # L1-L8
    tier2_steps: dict  # B1-B5
    tier3_steps: dict  # D1-D3
    cross_validation: dict
    final_report: dict
    
    # DSTE日历状态
    dste_calendar: dict  # {month: {phase, tasks, skills, outputs}}
    
    # 分析日志
    log: list
    
    def invalidate_downstream(self, from_step_id: str):
        """标记所有下游步骤为stale"""
        # 跨层级级联: tier1修改→tier2 stale, tier2修改→tier3 stale
```

## Step 4: Commit

```bash
git add -A && git commit -m "feat: three-tier data model + 19-step definitions + AnalyzeContext"
```
