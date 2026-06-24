# Task 12: 场景化向导页面

> **对应文档**: 六、技能调用流程 — 4个场景的详细调用序列

**Files:**
- Create: `app/templates/guide.html`
- Create: `app/templates/_scenario_card.html`

## Step 1: 4场景定义

```python
SCENARIOS = {
    "industry_research": {
        "name": "场景1：行业研究",
        "icon": "🔬",
        "description": "做行业深度研究（看行业/趋势）",
        "triggers": ["做战略洞察", "行业研究", "看行业"],
        "flow": [
            {"step": 1, "action": "初始化研究", "skill": "sn-deep-research"},
            {"step": 2, "action": "生成研究计划", "skill": "sn-research-planning", "output": "plan.json"},
            {"step": 3, "action": "行业维度取证", "skill": "sn-dimension-research"},
            {"step": 3.1, "action": "搜索学术论文", "skill": "sn-search-academic", "indent": True},
            {"step": 3.2, "action": "搜索用户口碑", "skill": "sn-search-social-cn/en", "indent": True},
            {"step": 4, "action": "行业趋势框架分析", "skill": "mbb-strategist(Industry Trends)"},
            {"step": 5, "action": "综合判断", "skill": "sn-research-synthesis"},
            {"step": 6, "action": "生成子报告", "skill": "sn-research-report"},
        ],
        "entry_step": "L1_industry",
    },
    "competition_analysis": {
        "name": "场景2：竞品分析",
        "icon": "⚔️",
        "description": "做竞品分析（看竞争）",
        "triggers": ["竞品分析", "竞争格局"],
        "flow": [
            {"step": 1, "action": "SWOT分析", "skill": "mbb-strategist(SWOT)"},
            {"step": 2, "action": "波特五力分析", "skill": "mbb-strategist(Porter's)"},
            {"step": 3, "action": "搜索竞品技术信息", "skill": "sn-search-code"},
            {"step": 4, "action": "绘制竞品对比图", "skill": "excel-bar-chart-visualization"},
            {"step": 5, "action": "输出竞争格局报告", "skill": None},
        ],
        "entry_step": "L3_competition",
    },
    "kpi_design": {
        "name": "场景3：KPI设计",
        "icon": "📊",
        "description": "做KPI设计（BEM解码）",
        "triggers": ["设计KPI", "BEM解码", "KPI体系"],
        "flow": [
            {"step": 1, "action": "设计KPI体系", "skill": "excel-data-analysis"},
            {"step": 2, "action": "设定KPI阈值", "skill": "excel-threshold-analysis-and-styling"},
            {"step": 3, "action": "识别异常值", "skill": "excel-outlier-detection-and-quality-assessment"},
            {"step": 4, "action": "输出KPI体系表", "skill": None},
        ],
        "entry_step": "B2_kpi",
    },
    "execution_tracking": {
        "name": "场景4：执行跟踪",
        "icon": "📈",
        "description": "做执行跟踪（DSTE执行）",
        "triggers": ["跟踪执行进度", "经营分析", "战略复盘"],
        "flow": [
            {"step": 1, "action": "跟踪执行进度", "skill": "planning-with-files(progress.md)"},
            {"step": 2, "action": "绘制进度图", "skill": "excel-line-chart-visualization"},
            {"step": 3, "action": "分析趋势偏差", "skill": "excel-trend-analysis"},
            {"step": 4, "action": "检测异常", "skill": "statistical-distribution-and-outlier-analysis"},
            {"step": 5, "action": "输出执行进度报告", "skill": None},
        ],
        "entry_step": "D1_execution",
    },
}
```

## Step 2: 向导页面 (guide.html)

- 4张场景卡片，点击展开调用流程图（带缩进、箭头、技能标签）
- "快速开始"按钮 → 直接跳转到对应步骤
- 搜索框 → 输入触发词 → 自动匹配场景

## Step 3: 触发词搜索API集成

输入框绑定 `/api/trigger/match`，实时返回匹配场景

## Step 4: Commit

```bash
git add -A && git commit -m "feat: 4-scenario guided workflows with skill call sequences"
```
