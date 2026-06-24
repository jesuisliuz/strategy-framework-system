# Task 14: 五看分析引擎 (L1-L5)

> **对应文档**: 三、技能嵌入映射表 — 第一层级：五看三定

**Files:**
- Create: `app/engines/tier1_five_looks.py`

## Step 1: 5步分析函数

```python
def analyze_L1_industry(fields, upstream, skill_interface):
    """看行业/趋势 — Industry Trends + PESTEL + Deep Research"""
    # 1. 调用 mbb-strategist(Industry Trends)
    # 2. 调用 mbb-strategist(PESTEL)
    # 3. 调用 sn-deep-research (行业维度)
    # 4. 调用 sn-search-academic (学术验证)
    # 输出: 行业趋势报告 + 价值转移分析图

def analyze_L2_customer(fields, upstream, skill_interface):
    """看客户 — Customer Journey + Personas + Social Search"""
    # 1. mbb-strategist(Customer Journey)
    # 2. mbb-strategist(Personas)
    # 3. sn-deep-research (客户维度)
    # 4. sn-search-social-cn/en (用户口碑)
    # 输出: 客户细分报告 + 市场交易地图

def analyze_L3_competition(fields, upstream, skill_interface):
    """看竞争 — SWOT + Porter's Five Forces + Code Search"""
    # 1. mbb-strategist(SWOT)
    # 2. mbb-strategist(Porter's Five Forces)
    # 3. sn-deep-research (竞品维度)
    # 4. sn-search-code (竞品技术)
    # 输出: 竞争格局报告 + 竞品对比矩阵

def analyze_L4_internal(fields, upstream, skill_interface):
    """看自己 — SWOT + Excel数据分析"""
    # 1. mbb-strategist(SWOT)
    # 2. excel-data-analysis (内部数据)
    # 输出: 能力评估报告

def analyze_L5_opportunity(fields, upstream, skill_interface):
    """看机会 — Risk & Scenario + SPAN矩阵可视化"""
    # 1. mbb-strategist(Risk & Scenario)
    # 2. excel-bar-chart-visualization (SPAN矩阵)
    # 输出: SPAN机会矩阵
```

## Step 2: 每个函数返回结构化结果

```python
{
    "content": "# Markdown分析内容...",
    "summary": "一句话摘要",
    "artifacts": ["行业趋势报告", "价值转移分析图"],
    "skills_used": ["mbb-strategist(Industry Trends)", "sn-deep-research"],
    "data": {}  # 结构化数据供下游使用
}
```

## Step 3: 注册到AnalysisEngine

```python
# app/engines/__init__.py
ANALYZERS = {
    "L1_industry": analyze_L1_industry,
    "L2_customer": analyze_L2_customer,
    # ...
}

class AnalysisEngine:
    @staticmethod
    def analyze(step_id, ctx, skills):
        analyzer = ANALYZERS.get(step_id)
        if not analyzer:
            return mock_analyze(step_id, ctx)
        return analyzer(ctx.get_step_input(step_id), upstream_data, SkillInterface)
```

## Step 4: Commit

```bash
git add -A && git commit -m "feat: five-looks analysis engine (L1-L5) with skill integration"
```
