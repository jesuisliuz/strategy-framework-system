# Task 7: 左侧输入面板（动态表单）

**Files:**
- Modify: `app/templates/step.html`
- Modify: `app/static/css/main.css`
- Modify: `app/static/js/app.js`

## Step 1: 动态表单渲染（Jinja2 + htmx）

在 step.html 的左侧面板中：

```html
<div class="input-panel" id="input-panel">
    <div class="panel-header">
        <h2>{{ step_def.name }}</h2>
        <span class="method-badge">{{ step_def.method }}</span>
    </div>
    
    <form hx-post="/api/step/{{ step_id }}/save"
          hx-target="#output-panel"
          hx-swap="innerHTML"
          hx-indicator="#analyzing-indicator">
        
        <input type="hidden" name="session_id" value="{{ session_id }}">
        
        {% for field in step_def.fields %}
        <div class="form-group">
            <label for="{{ field.id }}">
                {{ field.label }}
                {% if field.required %}<span class="required">*</span>{% endif %}
            </label>
            
            {% if field.type == 'textarea' %}
            <textarea id="{{ field.id }}" name="{{ field.id }}"
                      rows="4" placeholder="{{ field.placeholder }}"
                      {% if field.required %}required{% endif %}
            >{{ step_input.fields.get(field.id, '') }}</textarea>
            
            {% elif field.type == 'number' %}
            <input type="number" id="{{ field.id }}" name="{{ field.id }}"
                   value="{{ step_input.fields.get(field.id, '') }}"
                   placeholder="{{ field.placeholder }}"
                   {% if field.required %}required{% endif %}>
            
            {% else %}
            <input type="text" id="{{ field.id }}" name="{{ field.id }}"
                   value="{{ step_input.fields.get(field.id, '') }}"
                   placeholder="{{ field.placeholder }}"
                   {% if field.required %}required{% endif %}>
            {% endif %}
        </div>
        {% endfor %}
        
        <button type="submit" class="btn-submit">
            提交分析
        </button>
        <div id="analyzing-indicator" class="htmx-indicator">
            ⏳ 分析中...
        </div>
    </form>
    
    <!-- 步骤间快速跳转 -->
    <div class="step-quick-nav">
        {% if prev_step %}<a href="/step/{{ prev_step }}?session_id={{ session_id }}" class="btn-nav">← 上一步</a>{% endif %}
        {% if next_step %}<a href="/step/{{ next_step }}?session_id={{ session_id }}" class="btn-nav">下一步 →</a>{% endif %}
    </div>
</div>
```

## Step 2: 输入面板CSS

- 左侧固定宽度 340px
- 表单字段间距 16px
- `input`/`textarea` 深色背景 + 浅色文字
- focus 状态金色边框
- required 字段红色星号

## Step 3: htmx 表单提交逻辑 (app.js)

```javascript
// 表单提交后自动刷新导航条状态
document.body.addEventListener('htmx:afterSwap', function(evt) {
    if (evt.target.id === 'output-panel') {
        // 刷新导航条
        htmx.ajax('GET', '/api/nav-status?session_id=' + getSessionId(), {
            target: '#step-navigation',
            swap: 'innerHTML'
        });
    }
});
```

## Step 4: 添加导航状态API端点

在 app.py 中添加 `/api/nav-status` 端点，返回当前会话所有步骤的状态HTML片段。

## Step 5: 验证

手动提交一个表单，确认：
- 数据保存到session
- 输出面板展示结果
- 导航条状态更新

## Step 6: Commit

```bash
git add -A
git commit -m "feat: dynamic input panel with htmx form submission"
git push origin main
```
