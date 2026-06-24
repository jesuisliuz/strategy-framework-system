# Task 8: 中间输出面板与级联进度指示

**Files:**
- Modify: `app/templates/step.html`
- Modify: `app/static/css/main.css`

## Step 1: 输出面板模板

```html
<div class="output-panel" id="output-panel">
    <!-- 上游数据折叠区 -->
    {% if upstream_steps %}
    <details class="upstream-summary" open>
        <summary>
            📋 前置步骤摘要 
            <span class="badge">{{ upstream_steps|length }}步已完成</span>
        </summary>
        <div class="upstream-cards">
            {% for us in upstream_steps %}
            <div class="upstream-card">
                <span class="upstream-step-num">{{ us.number }}</span>
                <strong>{{ us.name }}</strong>
                <p>{{ us.summary[:120] }}{% if us.summary|length > 120 %}...{% endif %}</p>
                <span class="upstream-status {{ us.status }}">{{ us.status_label }}</span>
            </div>
            {% endfor %}
        </div>
    </details>
    {% endif %}
    
    <!-- 级联警告 -->
    {% if downstream_stale_count > 0 %}
    <div class="cascade-warning">
        ⚠️ 修改此步骤将导致下游 <strong>{{ downstream_stale_count }}</strong> 个步骤需要重新计算。
        <button class="btn-recalculate" 
                hx-post="/api/step/{{ step_id }}/recalculate"
                hx-target="#output-panel">
            确认重算
        </button>
    </div>
    {% endif %}
    
    <!-- 分析结果 -->
    <div class="analysis-result">
        {% if step_output.status == 'pending' %}
        <div class="empty-state">
            <p>请在左侧填写输入信息并提交分析</p>
        </div>
        {% elif step_output.status == 'analyzing' %}
        <div class="loading-state">
            <div class="spinner"></div>
            <p>正在分析中...</p>
        </div>
        {% elif step_output.status in ('done', 'stale') %}
        <div class="result-content {% if step_output.status == 'stale' %}stale{% endif %}">
            <div class="result-header">
                <h3>分析结果</h3>
                <div class="result-actions">
                    <button class="btn-action" onclick="copyResult()">📋 复制</button>
                    <button class="btn-action" hx-post="/api/step/{{ step_id }}/recalculate" hx-target="#output-panel">
                        🔄 重新生成
                    </button>
                </div>
            </div>
            <div class="markdown-body">
                {{ step_output.content | safe }}
            </div>
        </div>
        {% else %}
        <div class="error-state">
            <p>❌ 分析出错：{{ step_output.content }}</p>
        </div>
        {% endif %}
    </div>
</div>
```

## Step 2: 级联重算端点 (app.py)

```python
@app.route("/api/step/<step_id>/recalculate", methods=["POST"])
def recalculate_step(step_id):
    sid = request.form.get("session_id") or request.args.get("session_id")
    ctx = get_session(sid)
    if not ctx:
        return "Session not found", 404
    
    result = StepEngine.analyze(step_id, ctx)
    ctx.set_step_result(step_id, result, summary=result[:100])
    ctx.invalidate_downstream(step_id)
    save_session(ctx)
    
    return render_template("_output_panel.html", 
                          step_output=ctx.get_step_output(step_id),
                          step_def=STEP_DEFINITIONS.get(step_id))
```

## Step 3: 输出面板CSS

- `upstream-summary`: 折叠卡片，半透明背景
- `cascade-warning`: 橙色警告横幅
- `result-content`: 白色卡片，Markdown渲染
- `.stale` 覆盖层：半透明+斜条纹背景+角标"数据已过期"

## Step 4: 验证

1. 提交L1表单 → 确认输出面板显示分析结果
2. 返回L1修改 → 确认级联警告出现
3. 提交下游步骤 → 确认上游数据正确汇总

## Step 5: Commit

```bash
git add -A
git commit -m "feat: output panel + cascade warning + upstream summary"
git push origin main
```
