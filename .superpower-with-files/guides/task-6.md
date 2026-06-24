# Task 6: 基础布局与步骤导航条

**Files:**
- Modify: `app/templates/base.html`
- Create: `app/templates/step.html`
- Modify: `app/static/css/main.css`

## Step 1: 完善 base.html 布局

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}华为三板斧战略分析系统{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/main.css">
    <script src="https://unpkg.com/htmx.org@2.0.4"></script>
</head>
<body>
    <div class="app-container">
        <!-- 顶部导航栏 -->
        <header class="top-bar">
            <div class="logo">
                <span class="logo-icon">⚔️</span>
                <span class="logo-text">战略分析工作台</span>
            </div>
            <div class="project-name" id="project-name-display">
                {% if project_name %}{{ project_name }}{% endif %}
            </div>
        </header>
        
        <!-- 步骤导航条 -->
        <nav class="step-nav" id="step-navigation">
            {% block step_nav %}{% endblock %}
        </nav>
        
        <!-- 主内容区 -->
        <main class="main-content">
            {% block content %}{% endblock %}
        </main>
    </div>
    
    <script src="/static/js/app.js"></script>
</body>
</html>
```

## Step 2: 创建步骤导航条组件（macros.html 或直接嵌入）

```html
<div class="step-progress">
    {% set steps = [
        ('L1_industry', '1', '看行业'),
        ('L2_customer', '2', '看客户'),
        ('L3_competition', '3', '看竞争'),
        ('L4_internal', '4', '看自己'),
        ('L5_opportunity', '5', '看机会'),
        ('L6_objective', '6', '定目标'),
        ('L7_strategy', '7', '定策略'),
        ('L8_control', '8', '定控制点'),
        ('final_report', '📊', '最终报告'),
    ] %}
    
    {% for step_id, num, label in steps %}
    <a href="/step/{{ step_id }}?session_id={{ session_id }}"
       class="step-item {% if step_id == current_step %}active{% elif steps_status[step_id] == 'done' %}done{% elif steps_status[step_id] == 'stale' %}stale{% endif %}"
       id="nav-{{ step_id }}">
        <span class="step-num">{{ num }}</span>
        <span class="step-label">{{ label }}</span>
        {% if steps_status[step_id] == 'done' %}
        <span class="step-check">✓</span>
        {% elif steps_status[step_id] == 'analyzing' %}
        <span class="step-spinner"></span>
        {% endif %}
    </a>
    {% endfor %}
</div>
```

## Step 3: 创建 step.html（单步骤页面模板）

布局：
- 继承 base.html
- 左侧面板（30%宽）：输入表单
- 中间面板（70%宽）：输出展示 + 上游数据折叠卡片
- 响应式：小屏幕上下堆叠

## Step 4: 完善 main.css 导航样式

- `.step-nav`: flex布局，水平滚动
- `.step-item`: 连接线效果，hover/active/done/stale 四态
- Done = 绿色对勾，Active = 金色边框，Stale = 橙色虚线警告

## Step 5: 验证

```bash
# 启动Flask
python app/app.py &
sleep 2
# 验证首页
curl -s http://localhost:5000/ | grep "战略分析工作台"
# 验证步骤页
curl -s http://localhost:5000/step/L1_industry | grep "看行业"
```

## Step 6: Commit

```bash
git add -A
git commit -m "feat: step navigation bar + step page layout"
git push origin main
```
