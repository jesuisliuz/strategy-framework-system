# Task 20: L2 战略解码方案生成器

> **对应文档**: 四、三级报告模板 — L2 战略解码方案（5,000-10,000字）精确7章BEM结构

**Files:**
- Create: `app/reports/l2_report.py`

## Step 1: 精确匹配7章模板

```python
def generate_L2_report(ctx):
    """L2 战略解码方案 — 7章BEM结构"""
    
    report = f"""# {ctx.project_name} 战略解码方案（L2）

*BEM战略解码 · 第二级产出 | 目标字数: 5,000-10,000字*

---

## 一、战略回顾（500字）
{section_from_step(ctx, 'L6_objective', summary_only=True)}

## 二、CSF导出（1,000字）
{section_from_step(ctx, 'B1_csf')}
- 关键成功因素清单
- CSF与战略目标的映射关系

## 三、KPI体系设计（1,500字）
{section_from_step(ctx, 'B2_kpi')}
- KPI清单
- KPI定义与计算公式
- KPI目标值
- KPI数据来源

## 四、CTQ-Y导出（1,000字）
{section_from_step(ctx, 'B3_ctq')}
- 关键品质点清单
- CTQ-Y与KPI的映射关系

## 五、重点工作分解（1,500字）
{section_from_step(ctx, 'B4_keytasks')}
- 年度重点工作清单
- 重点工作与CSF/KPI的映射关系
- 责任部门/责任人

## 六、PBC模板（500字）
{section_from_step(ctx, 'B5_pbc')}
- PBC模板设计
- PBC签订流程

## 七、附件
{generate_attachments_section(ctx, 'L2')}
- KPI体系表（Excel）
- 重点工作分解表（Excel）

---
"""
    return report
```

## Step 2: BEM完整性验证

```python
def validate_L2_bem_chain(ctx) -> dict:
    """验证BEM解码链路: 战略目标→CSF→KPI→CTQ→重点工作→PBC"""
```

## Step 3: Commit

```bash
git add -A && git commit -m "feat: L2 strategic decoding report — 7-chapter BEM template matching spec"
```
