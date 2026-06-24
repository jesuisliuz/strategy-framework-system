# Task 23: 质量检查清单验证模块

> **对应文档**: 八、质量检查清单 — L1/L2/L3 各6/5/4项检查

**Files:**
- Create: `app/quality_check.py`
- Modify: `app/templates/report.html` → 添加检查清单展示

## Step 1: 质量检查逻辑

```python
QUALITY_CHECKLISTS = {
    "L1": [
        {"id": "cover_all_modules", "text": "是否覆盖了五看三定全部模块？", "check": lambda ctx: all_modules_covered(ctx, ["L1_industry","L2_customer","L3_competition","L4_internal","L5_opportunity","L6_objective","L7_strategy","L8_control"])},
        {"id": "use_mbb_frameworks", "text": "是否使用了mbb-strategist的至少2个框架？", "check": lambda ctx: mbb_framework_count(ctx) >= 2},
        {"id": "deep_research", "text": "是否有sn-deep-research的深度取证？", "check": lambda ctx: has_skill_used(ctx, "sn-deep-research")},
        {"id": "data_support", "text": "是否有数据支撑（Excel分析/可视化）？", "check": lambda ctx: has_skill_used(ctx, "excel-")},
        {"id": "word_count", "text": "字数是否达到10,000-30,000字？", "check": lambda ctx: 10000 <= word_count(ctx, "L1") <= 30000},
        {"id": "action_items", "text": "是否有明确的行动建议？", "check": lambda ctx: has_action_items(ctx, "L1")},
    ],
    "L2": [
        {"id": "csf_mapping", "text": "CSF是否与战略目标映射？", "check": lambda ctx: has_mapping(ctx, "B1_csf", "L6_objective")},
        {"id": "kpi_smart", "text": "KPI是否SMART化？", "check": lambda ctx: check_kpi_smart(ctx, "B2_kpi")},
        {"id": "key_tasks_assigned", "text": "重点工作是否分解到部门/责任人？", "check": lambda ctx: has_assignments(ctx, "B4_keytasks")},
        {"id": "pbc_template", "text": "是否有PBC模板？", "check": lambda ctx: has_output(ctx, "B5_pbc")},
        {"id": "word_count", "text": "字数是否达到5,000-10,000字？", "check": lambda ctx: 5000 <= word_count(ctx, "L2") <= 10000},
    ],
    "L3": [
        {"id": "action_plan", "text": "是否有季度/月度行动计划？", "check": lambda ctx: has_section(ctx, "D1_execution", "行动计划")},
        {"id": "monitoring", "text": "是否有监控机制（频率/指标/预警）？", "check": lambda ctx: has_monitoring(ctx, "D2_analysis")},
        {"id": "review", "text": "是否有复盘机制（频率/流程/迭代）？", "check": lambda ctx: has_section(ctx, "D3_review", "复盘")},
        {"id": "word_count", "text": "字数是否达到2,000-5,000字？", "check": lambda ctx: 2000 <= word_count(ctx, "L3") <= 5000},
    ],
}

class QualityChecker:
    @staticmethod
    def check_all(ctx) -> dict:
        """运行全部三个层级的质量检查"""
        return {
            "L1": QualityChecker.check_level(ctx, "L1"),
            "L2": QualityChecker.check_level(ctx, "L2"),
            "L3": QualityChecker.check_level(ctx, "L3"),
            "overall_score": QualityChecker.overall_score(ctx),
        }
    
    @staticmethod
    def check_level(ctx, level) -> dict:
        checklist = QUALITY_CHECKLISTS[level]
        results = []
        for item in checklist:
            passed = item["check"](ctx)
            results.append({"id": item["id"], "text": item["text"], "passed": passed})
        score = sum(1 for r in results if r["passed"])
        return {"items": results, "score": score, "total": len(checklist), "percentage": round(score/len(checklist)*100)}
```

## Step 2: API端点

```python
@app.route("/api/quality/check")
def quality_check():
    ctx = get_session(request.args.get("session_id"))
    return jsonify(QualityChecker.check_all(ctx))
```

## Step 3: 前端展示

在报告页面侧边栏或底部显示检查结果（✅/❌图标 + 进度条）

## Step 4: Commit

```bash
git add -A && git commit -m "feat: quality check system — L1/L2/L3 checklists per user spec section 8"
```
