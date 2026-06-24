# Task 8: 会话管理与API路由

**Files:**
- Create: `app/session.py`
- Modify: `app/app.py` → 添加完整API路由

## Step 1: 会话管理 (session.py)

支持创建/读取/保存/过期清理，JSON持久化到 app/instance/

## Step 2: API路由 (app.py)

```python
# === 会话 ===
POST /api/session/start          → 创建新会话
GET  /api/session/<id>/status    → 会话状态（所有步骤完成情况）

# === 步骤操作 ===
GET  /api/step/<step_id>?session_id=X         → 获取步骤数据（定义+输入+输出）
POST /api/step/<step_id>/save                  → 保存输入+执行分析
POST /api/step/<step_id>/recalculate           → 单体重算
POST /api/cascade/recalculate                  → 级联重算（从指定步骤起）

# === 技能 ===
GET  /api/skills/list                          → 所有技能清单
GET  /api/step/<step_id>/skills                → 该步骤关联技能

# === 触发词 ===
POST /api/trigger/match                        → 匹配触发词

# === 报告 ===
GET  /api/report/L1?session_id=X               → L1报告
GET  /api/report/L2?session_id=X               → L2报告
GET  /api/report/L3?session_id=X               → L3报告
GET  /api/report/full?session_id=X             → 完整三份报告

# === 导航状态 ===
GET  /api/nav/status?session_id=X              → 导航条状态HTML片段

# === DSTE日历 ===
GET  /api/dste/calendar?session_id=X           → DSTE日历数据
```

## Step 3: 步骤操作核心逻辑

```python
@app.route("/api/step/<step_id>/save", methods=["POST"])
def save_step_input(step_id):
    data = request.get_json()
    ctx = get_session(data["session_id"])
    
    # 1. 保存输入
    ctx.set_step_input(step_id, data.get("fields", {}))
    
    # 2. 标记下游为stale（跨层级）
    ctx.invalidate_downstream(step_id)
    
    # 3. 获取该步骤所需的技能列表
    skills = SkillRegistry.get_skills_for_step(step_id)
    
    # 4. 执行分析（调用技能集成引擎）
    result = AnalysisEngine.analyze(step_id, ctx, skills)
    
    # 5. 保存输出
    ctx.set_step_result(step_id, result)
    save_session(ctx)
    
    return jsonify({"status": "done", "output": ctx.get_step(step_id)["output"]})
```

## Step 4: Commit

```bash
git add -A && git commit -m "feat: session management + complete API routes (19 steps)"
```
