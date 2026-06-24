# Task 11: 中间输出面板与级联进度指示

**Files:**
- Create: `app/templates/_output_panel.html`
- Modify: `app/templates/step.html`

## Step 1: 输出面板组件

展示：上游摘要(折叠) + 级联警告 + 分析结果(Markdown) + 输出物清单

```html
<div class="output-panel" id="output-panel">
    <!-- 上游数据折叠 -->
    {% if upstream %}
    <details class="upstream-summary" open>
        <summary>📋 上游步骤摘要 ({{ upstream|length }}步已完成)</summary>
        <div class="upstream-cards">...</div>
    </details>
    {% endif %}
    
    <!-- 级联警告（跨层级） -->
    {% if cascade_info %}
    <div class="cascade-warning {{ cascade_info.severity }}">
        {% if cascade_info.cross_tier %}
        ⚠️ 该修改跨越层级边界 — Tier{{ cascade_info.from_tier }} → Tier{{ cascade_info.to_tier }}
        {% endif %}
        <p>下游 {{ cascade_info.count }} 个步骤标记为过期</p>
        <button class="btn-cascade" hx-post="/api/cascade/recalculate">一键级联重算</button>
    </div>
    {% endif %}
    
    <!-- 分析结果 -->
    <div class="analysis-result">
        <div class="result-header">
            <h3>分析结果</h3>
            <div class="result-actions">
                <button onclick="copyResult()">📋 复制</button>
                <button hx-post="/api/step/{{ step_id }}/recalculate">🔄 重新生成</button>
            </div>
        </div>
        <div class="markdown-body">{{ output.content | safe }}</div>
    </div>
    
    <!-- 输出物清单（来自技能映射表） -->
    <div class="output-artifacts">
        <h4>预期输出物</h4>
        <ul>
            {% for artifact in step.outputs %}
            <li>✅ {{ artifact }}</li>
            {% endfor %}
        </ul>
    </div>
</div>
```

## Step 2: 级联进度指示器

- 级联过程中显示进度条
- 展示当前重算步骤名称
- 完成后刷新导航条状态

## Step 3: 跨层级级联规则

- Tier1(五看三定)修改 → Tier1下游 + Tier2全部 + Tier3全部 stale
- Tier2(BEM)修改 → Tier2下游 + Tier3全部 stale  
- Tier3(DSTE)修改 → 仅当前Tier下游 stale

## Step 4: Commit

```bash
git add -A && git commit -m "feat: output panel + cross-tier cascade warnings + artifacts list"
```
