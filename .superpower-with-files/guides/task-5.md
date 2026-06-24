# Task 5: 技能注册表与映射引擎

> **对应文档**: 三、技能嵌入映射表（核心） — 每步→技能→使用方法→输出物

**Files:**
- Create: `app/skill_registry.py`

## Step 1: 技能清单定义 (完整技能目录)

```python
SKILL_INVENTORY = {
    # === 战略框架 ===
    "mbb-strategist": {
        "category": "战略框架",
        "capabilities": ["SWOT", "PESTEL", "Porter's Five Forces", "Value Chain", 
                        "Blue Ocean", "GTM Strategy", "Pricing Strategy", "Risk & Scenario",
                        "Financial Modeling", "Executive Synthesis", "Industry Trends",
                        "Customer Journey", "Personas"],
        "priority": 2,
    },
    # === 深度研究 ===
    "sn-deep-research": {
        "category": "深度研究",
        "capabilities": ["规划→取证→综合→成稿全流程编排"],
        "sub_skills": ["sn-research-planning", "sn-dimension-research", 
                       "sn-research-synthesis", "sn-research-report", 
                       "sn-report-format-discovery"],
        "priority": 1,
    },
    # === 搜索系列 ===
    "sn-search-academic": {"category": "研究子技能", "capabilities": ["ArXiv", "Semantic Scholar", "PubMed"], "priority": 1},
    "sn-search-code": {"category": "研究子技能", "capabilities": ["GitHub", "Stack Overflow"], "priority": 1},
    "sn-search-social-cn": {"category": "研究子技能", "capabilities": ["B站", "知乎", "抖音"], "priority": 1},
    "sn-search-social-en": {"category": "研究子技能", "capabilities": ["Reddit", "Twitter", "YouTube"], "priority": 1},
    # === 文件规划 ===
    "planning-with-files": {
        "category": "文件规划",
        "capabilities": ["task_plan.md", "findings.md", "progress.md"],
        "priority": 4,
    },
    # === Excel分析 (30+技能) ===
    "excel-data-analysis": {"category": "Excel分析", "capabilities": ["数据清洗", "分类统计", "条件过滤", "KPI体系设计"], "priority": 3},
    "excel-bar-chart-visualization": {"category": "Excel分析", "capabilities": ["柱状图"], "priority": 3},
    "excel-line-chart-visualization": {"category": "Excel分析", "capabilities": ["折线图"], "priority": 3},
    "excel-pie-chart-data-analysis": {"category": "Excel分析", "capabilities": ["饼图"], "priority": 3},
    "pivot-table-cross-analysis": {"category": "Excel分析", "capabilities": ["透视表"], "priority": 3},
    "trend-analysis": {"category": "Excel分析", "capabilities": ["趋势分析"], "priority": 3},
    "outlier-detection-and-quality-assessment": {"category": "Excel分析", "capabilities": ["异常值检测"], "priority": 3},
    "statistical-distribution-and-outlier-analysis": {"category": "Excel分析", "capabilities": ["统计分布"], "priority": 3},
    "time-series-and-categorical-analysis": {"category": "Excel分析", "capabilities": ["时间序列"], "priority": 3},
    # (及其他30+ Excel技能)
}
```

## Step 2: 技能映射表

```python
STEP_SKILL_MAP = {
    # Tier1: 五看三定
    "L1_industry": {
        "skills": ["mbb-strategist", "sn-deep-research", "sn-search-academic"],
        "mbb_frameworks": ["Industry Trends", "PESTEL"],
        "usage": "用MBB的Industry Trends框架分析行业趋势；用sn-deep-research做深度行业研究；用sn-search-academic搜索学术论文验证趋势",
        "outputs": ["行业趋势报告", "价值转移分析图"],
    },
    "L2_customer": {
        "skills": ["mbb-strategist", "sn-deep-research", "sn-search-social-cn", "sn-search-social-en"],
        "mbb_frameworks": ["Customer Journey", "Personas"],
        "usage": "用MBB的Customer Journey分析客户购买行为；用Personas做用户画像；用sn-search-social搜索用户口碑",
        "outputs": ["客户细分报告", "市场交易地图"],
    },
    "L3_competition": {
        "skills": ["mbb-strategist", "sn-deep-research", "sn-search-code"],
        "mbb_frameworks": ["SWOT", "Porter's Five Forces"],
        "usage": "用SWOT分析自身与竞品；用Porter's Five Forces分析竞争格局；用sn-search-code搜索竞品技术信息",
        "outputs": ["竞争格局报告", "竞品对比矩阵"],
    },
    "L4_internal": {
        "skills": ["mbb-strategist", "excel-data-analysis"],
        "mbb_frameworks": ["SWOT"],
        "usage": "用SWOT分析自身优势劣势；用Excel分析内部运营数据",
        "outputs": ["能力评估报告"],
    },
    "L5_opportunity": {
        "skills": ["mbb-strategist", "excel-bar-chart-visualization"],
        "mbb_frameworks": ["Risk & Scenario"],
        "usage": "用Risk & Scenario分析机会风险；用Excel绘制SPAN矩阵",
        "outputs": ["SPAN机会矩阵"],
    },
    "L6_objective": {
        "skills": ["mbb-strategist"],
        "mbb_frameworks": ["Executive Synthesis"],
        "usage": "用Executive Synthesis提炼战略目标",
        "outputs": ["战略目标清单"],
    },
    "L7_strategy": {
        "skills": ["mbb-strategist"],
        "mbb_frameworks": ["GTM Strategy", "Pricing Strategy"],
        "usage": "用GTM设计市场进入策略；用Pricing Strategy设计定价策略",
        "outputs": ["策略路线图"],
    },
    "L8_control": {
        "skills": ["mbb-strategist"],
        "mbb_frameworks": ["SWOT", "Porter's"],
        "usage": "用SWOT和Porter's分析护城河",
        "outputs": ["战略控制点清单"],
    },
    # Tier2: BEM六步法
    "B1_csf": {
        "skills": ["mbb-strategist"],
        "mbb_frameworks": ["Executive Synthesis"],
        "usage": "用Executive Synthesis提炼CSF",
        "outputs": ["CSF清单"],
    },
    "B2_kpi": {
        "skills": ["excel-data-analysis", "excel-threshold-analysis-and-styling"],
        "usage": "用Excel设计KPI体系；用阈值分析设定KPI目标值",
        "outputs": ["KPI体系表"],
    },
    "B3_ctq": {
        "skills": ["excel-outlier-detection-and-quality-assessment"],
        "usage": "用异常值检测识别关键品质点",
        "outputs": ["CTQ-Y清单"],
    },
    "B4_keytasks": {
        "skills": ["planning-with-files"],
        "usage": "用文件化规划分解重点工作",
        "outputs": ["重点工作分解表"],
    },
    "B5_pbc": {
        "skills": ["excel-data-analysis"],
        "usage": "用Excel设计PBC模板",
        "outputs": ["PBC模板"],
    },
    # Tier3: DSTE
    "D1_execution": {
        "skills": ["planning-with-files", "excel-line-chart-visualization"],
        "usage": "用文件化规划跟踪进度；用折线图可视化进度",
        "outputs": ["执行进度报告"],
    },
    "D2_analysis": {
        "skills": ["excel-trend-analysis", "statistical-distribution-and-outlier-analysis"],
        "usage": "用趋势分析识别偏差；用异常检测发现异常",
        "outputs": ["偏差分析报告"],
    },
    "D3_review": {
        "skills": ["sn-research-synthesis"],
        "usage": "用综合判断提炼复盘结论",
        "outputs": ["战略复盘报告"],
    },
    # 验证
    "cross_validation": {
        "skills": ["sn-research-synthesis", "mbb-strategist"],
        "usage": "横向行业对齐+纵向时间推演验证",
        "outputs": ["验证报告"],
    },
}
```

## Step 3: SkillRegistry 类

```python
class SkillRegistry:
    @staticmethod
    def get_skills_for_step(step_id: str) -> list:
        """获取步骤需要的技能列表"""
        
    @staticmethod
    def get_priority(skill_name: str) -> int:
        """获取技能调用优先级"""
        
    @staticmethod
    def get_all_skills_by_category() -> dict:
        """按类别分组获取所有技能——用于前端可视化"""
```

## Step 4: Commit

```bash
git add -A && git commit -m "feat: skill registry + step-skill mapping (matching user spec)"
```
