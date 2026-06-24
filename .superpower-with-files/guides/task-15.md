# Task 15: 三定分析引擎 (L6-L8)

**Files:**
- Create: `app/engines/tier1_three_sets.py`

## Step 1: 3步分析函数

```python
def analyze_L6_objective(fields, upstream, skill_interface):
    """定目标 — Executive Synthesis"""
    # mbb-strategist(Executive Synthesis) 提炼战略目标
    # 输入: L1-L5输出中的关键数据
    # 输出: 战略目标清单

def analyze_L7_strategy(fields, upstream, skill_interface):
    """定策略 — GTM Strategy + Pricing Strategy"""
    # 1. mbb-strategist(GTM Strategy) 市场进入策略
    # 2. mbb-strategist(Pricing Strategy) 定价策略
    # 输出: 策略路线图

def analyze_L8_control(fields, upstream, skill_interface):
    """定控制点 — SWOT + Porter's 护城河分析"""
    # 1. mbb-strategist(SWOT) 
    # 2. mbb-strategist(Porter's)
    # 输出: 战略控制点清单
```

## Step 2: L6-L8 需要特殊处理的级联

三定需要引用特定上游数据:
- L6定目标 → L5看机会的SPAN数据
- L7定策略 → L3看竞争的竞对地图  
- L8定控制点 → L4看自己的核心能力评估

在 `_gather_upstream` 中增加 `key_fields` 标记。

## Step 3: Commit

```bash
git add -A && git commit -m "feat: three-sets analysis engine (L6-L8) with Executive Synthesis + GTM"
```
