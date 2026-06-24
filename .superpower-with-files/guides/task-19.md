# Task 19: L1 战略洞察报告生成器

> **对应文档**: 四、三级报告模板 — L1 战略洞察报告（10,000-30,000字）精确8章结构

**Files:**
- Create: `app/reports/l1_report.py`

## Step 1: 精确匹配8章模板

```python
def generate_L1_report(ctx):
    """L1 战略洞察报告 — 8章结构"""
    
    report = f"""# {ctx.project_name} 战略洞察报告（L1）

*五看三定 · 第一级产出 | 目标字数: 10,000-30,000字*

---

## 一、执行摘要（1,000字）
{generate_executive_summary(ctx)}

## 二、看行业/趋势（3,000-5,000字）
{section_from_step(ctx, 'L1_industry')}
### 宏观环境分析（PESTEL）
### 行业趋势分析（Industry Trends）
### 价值转移趋势
### 数据来源与证据

## 三、看客户（3,000-5,000字）
{section_from_step(ctx, 'L2_customer')}
### 客户细分（Personas）
### 客户购买行为分析（Customer Journey）
### 市场交易地图
### 需求层次分析（requirements/wants/pains）

## 四、看竞争（3,000-5,000字）
{section_from_step(ctx, 'L3_competition')}
### 竞争格局分析（Porter's Five Forces）
### 竞品对比（SWOT）
### 竞争策略建议

## 五、看自己（2,000-3,000字）
{section_from_step(ctx, 'L4_internal')}
### 自身优势分析（SWOT-S）
### 自身劣势分析（SWOT-W）
### 能力差距分析

## 六、看机会（2,000-3,000字）
{section_from_step(ctx, 'L5_opportunity')}
### 机会识别
### SPAN矩阵分析
### 机会优先级排序

## 七、三定（3,000-5,000字）
### 定目标
{section_from_step(ctx, 'L6_objective')}
### 定策略（GTM/Pricing）
{section_from_step(ctx, 'L7_strategy')}
### 定控制点
{section_from_step(ctx, 'L8_control')}

## 八、数据来源与证据
{generate_evidence_section(ctx)}
- 所有数据来源列表
- 证据强弱判断

---

*报告生成时间: {datetime.now().isoformat()}*
*技能调用: sn-deep-research + mbb-strategist + sn-search系列 + Excel分析系列*
"""
    return report
```

## Step 2: 各章节从步骤输出中提取

```python
def section_from_step(ctx, step_id):
    out = ctx.get_step(step_id)["output"]
    if out["status"] in ("done", "stale"):
        return out["content"]
    return f"*（该步骤尚未完成分析）*"
```

## Step 3: 字数统计与检查

```python
def check_L1_requirements(report: str) -> dict:
    word_count = len(report.replace(' ', '').replace('\n', ''))
    return {
        "total_chars": word_count,
        "meets_requirement": 10000 <= word_count <= 30000,
        "chapters_present": all_chapters_check(report),
    }
```

## Step 4: Commit

```bash
git add -A && git commit -m "feat: L1 strategic insight report — exact 8-chapter template matching spec"
```
