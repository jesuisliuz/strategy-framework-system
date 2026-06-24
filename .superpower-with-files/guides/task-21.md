# Task 21: L3 落地执行方案生成器

> **对应文档**: 四、三级报告模板 — L3 落地执行方案（2,000-5,000字）精确4章DSTE结构

**Files:**
- Create: `app/reports/l3_report.py`

## Step 1: 精确匹配4章模板

```python
def generate_L3_report(ctx):
    """L3 落地执行方案 — 4章DSTE结构"""
    
    report = f"""# {ctx.project_name} 落地执行方案（L3）

*DSTE端到端 · 第三级产出 | 目标字数: 2,000-5,000字*

---

## 一、执行计划（1,000字）
{section_from_step(ctx, 'D1_execution')}
- 季度/月度行动计划
- 里程碑节点
- 责任分工

## 二、监控机制（500字）
{section_from_step(ctx, 'D2_analysis')}
- 监控频率（月度/季度）
- 监控指标（KPI）
- 偏差预警机制

## 三、复盘机制（500字）
{section_from_step(ctx, 'D3_review')}
- 复盘频率（季度/半年度）
- 复盘流程
- 迭代机制

## 四、附件
{generate_attachments_section(ctx, 'L3')}
- 执行进度跟踪表（Excel）
- 偏差分析表（Excel）

---
"""
    return report
```

## Step 2: Commit

```bash
git add -A && git commit -m "feat: L3 execution plan report — 4-chapter DSTE template matching spec"
```
