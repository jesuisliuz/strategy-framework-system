# Task 16: BEM六步法引擎

> **对应文档**: 三、技能嵌入映射表 — 第二层级：BEM → L2 战略解码方案

**Files:**
- Create: `app/engines/tier2_bem.py`

## Step 1: BEM六步法5个分析函数

```python
def analyze_B1_csf(fields, upstream, skill_interface):
    """B1: CSF导出 — Executive Synthesis"""
    # 从L6战略目标中推导关键成功因素
    # mbb-strategist(Executive Synthesis)
    # 输出: CSF清单 + CSF与战略目标的映射关系

def analyze_B2_kpi(fields, upstream, skill_interface):
    """B2: KPI导出 — Excel KPI体系设计"""
    # 1. excel-data-analysis 设计KPI体系
    # 2. excel-threshold-analysis-and-styling 设定KPI阈值
    # 输出: KPI清单 + 定义/计算公式/目标值/数据来源

def analyze_B3_ctq(fields, upstream, skill_interface):
    """B3: CTQ-Y导出 — 异常值检测"""
    # excel-outlier-detection-and-quality-assessment
    # 从KPI中识别关键品质点
    # 输出: CTQ-Y清单 + CTQ-Y与KPI的映射关系

def analyze_B4_keytasks(fields, upstream, skill_interface):
    """B4: 重点工作分解 — 文件化规划"""
    # planning-with-files (task_plan.md)
    # 将CSF/KPI分解为年度重点工作
    # 输出: 重点工作清单 + 映射关系 + 责任部门

def analyze_B5_pbc(fields, upstream, skill_interface):
    """B5: PBC签订 — Excel模板"""
    # excel-data-analysis 设计PBC模板
    # 输出: PBC模板 + 签订流程说明
```

## Step 2: BEM解码流程完整性验证

```python
def validate_bem_chain(ctx):
    """验证BEM六步法链路完整性"""
    checks = []
    # CSF是否与战略目标映射?
    # KPI是否SMART化?
    # 重点工作是否分解到部门/责任人?
    # 是否有PBC模板?
    return checks
```

## Step 3: Commit

```bash
git add -A && git commit -m "feat: BEM six-step engine — CSF→KPI→CTQ→KeyTasks→PBC"
```
