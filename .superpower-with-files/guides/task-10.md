# Task 10: 左侧输入面板（19步动态表单）

**Files:**
- Modify: `app/templates/step.html`
- Modify: `app/static/js/app.js`

## Step 1: 动态表单渲染

根据 step_definitions.json 中的 fields 定义，渲染不同类型的输入控件。支持：text, number, textarea, imported(自动填充), file(Excel上传), select

```html
<form hx-post="/api/step/{{ step_id }}/save"
      hx-target="#output-panel"
      hx-swap="innerHTML">
    
    <input type="hidden" name="session_id" value="{{ session_id }}">
    
    <!-- 步骤信息 -->
    <div class="step-info">
        <h2>{{ step.name }}</h2>
        <span class="method-badge">{{ step.method }}</span>
        <p class="core-task">{{ step.core_task }}</p>
    </div>
    
    <!-- 关联技能展示 -->
    <div class="step-skills">
        {% for skill in step.skills %}
        <span class="skill-tag {{ skill.category }}">{{ skill.name }}</span>
        {% endfor %}
    </div>
    
    <!-- 输入字段 -->
    {% for field in step.fields %}
    <div class="form-group">
        <label>{{ field.label }}{% if field.required %}*{% endif %}</label>
        {% if field.type == 'imported' %}
            <div class="imported-value">{{ auto_fill_value }}</div>
        {% elif field.type == 'file' %}
            <input type="file" name="{{ field.id }}" accept=".xlsx,.xls,.csv">
        {% elif field.type == 'textarea' %}
            <textarea name="{{ field.id }}" rows="5">{{ saved_value }}</textarea>
        {% else %}
            <input type="{{ field.type }}" name="{{ field.id }}" value="{{ saved_value }}">
        {% endif %}
    </div>
    {% endfor %}
    
    <button type="submit">提交分析</button>
</form>
```

## Step 2: 步骤间快速跳转

```html
<div class="step-nav-buttons">
    {% if prev_step %}
    <a href="/step/{{ prev_step }}?session_id={{ session_id }}" class="btn-prev">← {{ prev_step_name }}</a>
    {% endif %}
    {% if next_step %}
    <a href="/step/{{ next_step }}?session_id={{ session_id }}" class="btn-next">{{ next_step_name }} →</a>
    {% endif %}
</div>
```

## Step 3: Imported字段自动填充

前端JS: 加载步骤时，自动从上游步骤获取数据填充 imported 类型字段。

## Step 4: Commit

```bash
git add -A && git commit -m "feat: 19-step dynamic forms with imported fields + file upload"
```
