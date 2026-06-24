# Task 26: 使用指南页面

> **对应文档**: 七、使用指南 — 触发词 + 技能调用优先级

**Files:**
- Create: `app/templates/usage_guide.html`

## Step 1: 使用指南页面

```html
<!-- 触发词快速参考 -->
<section class="guide-section">
    <h2>🔤 触发词快速参考</h2>
    <div class="trigger-grid">
        {% for scenario in trigger_map %}
        <div class="trigger-card">
            <h3>{{ scenario.name }}</h3>
            <div class="trigger-words">
                {% for word in scenario.triggers %}
                <code>{{ word }}</code>
                {% endfor %}
            </div>
            <div class="trigger-skills">
                {% for skill in scenario.skills %}
                <span class="skill-tag">{{ skill }}</span>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
</section>

<!-- 技能优先级 -->
<section class="guide-section">
    <h2>⚡ 技能调用优先级</h2>
    <div class="priority-chain">
        <div class="priority-item p1">
            <span class="priority-num">P1</span>
            <strong>sn-deep-research</strong>
            <p>深度研究编排器。触发条件：深度研究/行业研究/竞品分析</p>
        </div>
        <div class="arrow">↓</div>
        <div class="priority-item p2">
            <span class="priority-num">P2</span>
            <strong>mbb-strategist</strong>
            <p>MBB战略框架。触发条件：战略分析/SWOT/PESTEL/波特五力</p>
        </div>
        <div class="arrow">↓</div>
        <div class="priority-item p3">
            <span class="priority-num">P3</span>
            <strong>Excel分析系列</strong>
            <p>30+分析技能。触发条件：数据分析/KPI设计/可视化</p>
        </div>
        <div class="arrow">↓</div>
        <div class="priority-item p4">
            <span class="priority-num">P4</span>
            <strong>planning-with-files</strong>
            <p>文件化规划。触发条件：多步骤任务/进度跟踪</p>
        </div>
    </div>
</section>

<!-- 完整技能清单 -->
<section class="guide-section">
    <h2>📦 完整技能清单</h2>
    {% for category, skills in skill_categories.items() %}
    <div class="skill-category">
        <h3>{{ category }}</h3>
        {% for skill in skills %}
        <div class="skill-item">
            <strong>{{ skill.name }}</strong>: {{ skill.capabilities }}
        </div>
        {% endfor %}
    </div>
    {% endfor %}
</section>
```

## Step 2: 路由

```python
@app.route("/guide")
def usage_guide():
    return render_template("usage_guide.html", 
                          trigger_map=TRIGGER_MAP,
                          skill_priority=SKILL_PRIORITY,
                          skill_categories=SkillInterface.SKILL_CATEGORIES)
```

## Step 3: Commit

```bash
git add -A && git commit -m "feat: usage guide page — triggers + priority + full skill inventory"
```
