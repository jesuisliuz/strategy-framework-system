# Task 18: 横纵分析法 + 级联重算引擎

**Files:**
- Create: `app/engines/cross_validation.py`
- Modify: `app/engines/__init__.py`

## Step 1: 横纵分析法

```python
def analyze_cross_validation(fields, upstream, skill_interface):
    """横纵分析法 — 横向行业对齐 + 纵向时间推演"""
    # 横向: 将所有分析结果与行业benchmark对齐
    # 纵向: 按DSTE时间线推演各阶段可行性
    # 调用: sn-research-synthesis + mbb-strategist
```

## Step 2: 级联重算引擎

```python
class CascadeEngine:
    @staticmethod
    def get_downstream_steps(from_step_id: str) -> list:
        """获取所有下游步骤（跨层级）"""
        
    @staticmethod
    def recalculate_all(ctx, from_step_id: str) -> dict:
        """从指定步骤开始，重算所有stale下游"""
        downstream = CascadeEngine.get_downstream_steps(from_step_id)
        results = {}
        for step_id in downstream:
            if ctx.get_step(step_id)["output"]["status"] == "stale":
                result = AnalysisEngine.analyze(step_id, ctx, 
                         SkillRegistry.get_skills_for_step(step_id))
                ctx.set_step_result(step_id, result)
                results[step_id] = "done"
        return results
    
    @staticmethod
    def get_cascade_info(ctx, from_step_id: str) -> dict:
        """返回级联影响分析"""
```

## Step 3: 注册到 AnalysisEngine

将 cross_validation 加入 ANALYZERS 字典

## Step 4: Commit

```bash
git add -A && git commit -m "feat: cross-validation analysis + cascade recalculation engine"
```
