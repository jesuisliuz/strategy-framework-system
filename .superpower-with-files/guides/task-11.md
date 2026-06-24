# Task 11: 级联重算引擎

**Files:**
- Modify: `app/models.py` → 增强 invalidate_downstream
- Modify: `app/app.py` → 添加级联重算API

## Step 1: 增强级联标记逻辑 (models.py)

当前的 `invalidate_downstream` 只标记为 stale，需要增加：
- 级联深度计数
- 触发原因记录
- 可选自动重算模式

```python
def invalidate_downstream(self, from_step_id: str, reason: str = "", auto_recalc: bool = False):
    step_order = ["L1_industry", "L2_customer", "L3_competition",
                  "L4_internal", "L5_opportunity", "L6_objective",
                  "L7_strategy", "L8_control", "final_report"]
    
    stale_count = 0
    start = step_order.index(from_step_id) + 1
    for sid in step_order[start:]:
        if self.steps[sid]["output"].status in ("done", "stale"):
            self.steps[sid]["output"].status = "stale"
            self.steps[sid]["output"].data["_stale_reason"] = reason or f"上游 {from_step_id} 已修改"
            self.steps[sid]["output"].data["_stale_depth"] = step_order.index(sid) - step_order.index(from_step_id)
            stale_count += 1
    
    self.log.append(f"[{datetime.now().isoformat()}] Cascade: {from_step_id} → {stale_count} downstream steps marked stale")
    return stale_count
```

## Step 2: 添加"一键级联重算"端点

```python
@app.route("/api/cascade/recalculate", methods=["POST"])
def cascade_recalculate():
    """从当前步骤开始，依次重算所有下游步骤"""
    data = request.get_json()
    sid = data["session_id"]
    from_step = data["from_step"]
    
    ctx = get_session(sid)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404
    
    step_order = ["L1_industry", "L2_customer", "L3_competition",
                  "L4_internal", "L5_opportunity", "L6_objective",
                  "L7_strategy", "L8_control", "final_report"]
    
    results = []
    start = step_order.index(from_step)
    for step_id in step_order[start:]:
        if ctx.steps[step_id]["output"].status in ("stale", "pending"):
            # 检查该步骤是否有足够输入
            inp = ctx.get_step_input(step_id)
            if not inp.fields:
                continue  # 跳过无输入的步骤
            
            result = StepEngine.analyze(step_id, ctx)
            ctx.set_step_result(step_id, result, summary=result[:100])
            results.append({"step": step_id, "status": "done"})
    
    save_session(ctx)
    return jsonify({"cascade_complete": True, "results": results})
```

## Step 3: 前端级联交互 (app.js)

```javascript
// 提交表单后自动检测是否需要级联重算
document.body.addEventListener('htmx:afterSwap', function(evt) {
    if (evt.target.id === 'output-panel') {
        const staleWarning = document.querySelector('.cascade-warning');
        if (staleWarning) {
            // 弹出确认对话框
            if (confirm('上游修改将影响下游'+ document.querySelector('.stale-count').textContent +'个步骤。是否自动重算？')) {
                htmx.ajax('POST', '/api/cascade/recalculate', {
                    target: '#output-panel',
                    swap: 'innerHTML'
                });
            }
        }
        // 刷新导航条
        refreshNavStatus();
    }
});
```

## Step 4: 进度指示器

在级联重算过程中展示进度条：

```html
<div id="cascade-progress" class="htmx-indicator">
    <div class="progress-bar">
        <div class="progress-fill" style="width: {percent}%"></div>
    </div>
    <p>正在重算: {current_step} ({current}/{total})</p>
</div>
```

## Step 5: 验证

测试场景：
1. 完整填写L1 → 提交 → 验证L1 done
2. 完整填写L2 → 提交 → 验证L2 done
3. 返回L1修改字段 → 提交 → 验证L2标记为stale
4. 触发级联重算 → 验证L2重新计算

## Step 6: Commit

```bash
git add -A
git commit -m "feat: cascade recalculation engine + auto-recalc UI"
git push origin main
```
