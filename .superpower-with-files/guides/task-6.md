# Task 6: 19步完整定义与输入字段

> **对应文档**: 三、技能嵌入映射表 + 四、三级报告模板

**Files:**
- Create: `app/data/step_definitions.json`
- Modify: `app/models.py` → 补全 `ALL_STEPS` 定义

## Step 1: 19步定义JSON (step_definitions.json)

```json
{
  "steps": [
    {
      "step_id": "L1_industry",
      "tier": "tier1",
      "number": 1,
      "name": "看行业/趋势",
      "method": "五看 · 看行业",
      "core_task": "行业趋势分析、价值转移识别",
      "chapter_in_report": "二、看行业/趋势（3,000-5,000字）",
      "fields": [
        {"id": "industry_name", "label": "行业名称", "type": "text", "required": true},
        {"id": "market_size", "label": "当前市场规模（亿元）", "type": "number"},
        {"id": "growth_rate", "label": "年增长率（%）", "type": "number"},
        {"id": "tam", "label": "TAM（总可寻址市场）", "type": "text"},
        {"id": "key_trends", "label": "关键趋势驱动因素", "type": "textarea", "required": true},
        {"id": "technology_trends", "label": "关键技术趋势", "type": "textarea"},
        {"id": "additional_context", "label": "补充背景信息", "type": "textarea"}
      ]
    },
    // ... L2-L8 (五看三定全部8步)
    {
      "step_id": "B1_csf",
      "tier": "tier2",
      "number": 9,
      "name": "CSF导出",
      "method": "BEM · 关键成功因素",
      "core_task": "关键成功因素识别",
      "chapter_in_report": "二、CSF导出（1,000字）",
      "fields": [
        {"id": "strategic_objectives", "label": "战略目标（从L6导入）", "type": "imported", "source": "L6_objective"},
        {"id": "csf_candidates", "label": "候选CSF列表（每行一个）", "type": "textarea", "required": true},
        {"id": "mapping_note", "label": "CSF与战略目标映射说明", "type": "textarea"}
      ]
    },
    // ... B2-B5 (BEM六步法)
    // ... D1-D3 (DSTE)
    // ... cross_validation, final_report
  ]
}
```

## Step 2: 输入字段类型系统

支持的字段类型: text, number, textarea, imported(从上游自动填充), file(Excel上传), select(下拉)

## Step 3: 在models.py中加载定义

```python
import json, os

def load_step_definitions():
    path = os.path.join(os.path.dirname(__file__), "data", "step_definitions.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)["steps"]

ALL_STEPS = load_step_definitions()
```

## Step 4: Commit

```bash
git add -A && git commit -m "feat: complete 19-step definitions JSON with fields per spec"
```
