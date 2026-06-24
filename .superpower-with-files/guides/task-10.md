# Task 10: 三定阶段分析逻辑 (L6-L8)

**Files:**
- Modify: `app/steps.py` → 补全 L6-L8 分析模板

## Step 1: 三定分析Prompt模板

```python
ANALYSIS_PROMPTS.update({
    "L6_objective": {
        "system": "你是华为战略部目标管理专家，精通战略意图解码、BSC平衡计分卡和KPI体系设计。",
        "template": """基于前五步（五看）的战略洞察，请制定战略目标体系。

## 上游洞察摘要
{upstream_context}

## 输入信息
- 战略意图/愿景: {strategic_intent}
- 当前关键KPI基线: {kpi_baseline}
- 目标KPI值: {kpi_target}
- 差距描述: {gap_description}

## 分析要求
### 一、战略意图陈述
- 愿景使命提炼
- 3-5年战略目标画像

### 二、BSC目标体系
| 维度 | 战略目标 | KPI | 基线值 | 目标值 | 差距 |
|------|---------|-----|-------|-------|------|
| 财务 |         |     |       |       |      |
| 客户 |         |     |       |       |      |
| 流程 |         |     |       |       |      |
| 学习 |         |     |       |       |      |

### 三、差距分析
- 根因分析
- 关键瓶颈

### 四、目标可行性评估
- 资源匹配度
- 时间可达成性
- 风险提示""",
    },
    "L7_strategy": {
        "system": "你是华为战略部业务设计专家，精通BLM业务领先模型和创新焦点方法论。",
        "template": """...L7模板（业务设计+创新焦点+关键任务）..."""
    },
    "L8_control": {
        "system": "你是华为战略部风险管理专家，精通战略控制点设计和黑天鹅应对。",
        "template": """...L8模板（护城河+控制强度+风险预案）..."""
    },
})
```

## Step 2: 三定阶段需特殊处理的级联

三定（L6-L8）不仅依赖上游输出，还需要引用前序步骤的特定数据：
- L6定目标 → 需要L5看机会的SPAN数据
- L7定策略 → 需要L3看竞争的竞对地图
- L8定控制点 → 需要L4看自己的核心能力评估

在 `_gather_upstream` 中增加 `key_fields` 标记。

## Step 3: 实现 final_report 分析

最终报告是三级报告的聚合：
- L1 战略洞察 (10k-30k字) = L1-L5输出聚合
- L2 战略解码 (5k-10k字) = L6-L8输出聚合  
- L3 落地执行 (2k-5k字) = 从DSTE角度整合BEM解码

```python
"final_report": {
    "system": "你是华为战略部资深合伙人，精通DSTE端到端战略流程和BEM战略解码方法。",
    "template": """请基于前8步的战略分析结果，生成三级战略报告...

## 上游完整分析
{upstream_context}

## 报告要求
### 第一级：战略洞察报告（10k-30k字）
- 整合L1-L5输出
- 核心结论：该业务是否值得进入/加大投入

### 第二级：战略解码报告（5k-10k字）
- 整合L6-L8输出
- BEM解码：CSF→KPI→CTQ→年度措施→重点工作

### 第三级：落地执行报告（2k-5k字）
- DSTE年度日历
- 资源预算
- 战略仪表盘关键指标""",
}
```

## Step 4: 验证

```python
# 运行L6分析（需前5步有数据）
ctx = _build_mock_context_with_L1_L5()  # 创建mock上下文
result = StepEngine.analyze("L6_objective", ctx)
assert "BSC" in result or "平衡计分卡" in result or "KPI" in result
print("PASS")
```

## Step 5: Commit

```bash
git add -A
git commit -m "feat: three-sets (L6-L8) analysis prompts + final report template"
git push origin main
```
