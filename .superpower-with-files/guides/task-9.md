# Task 9: 三层级导航条 + DSTE日历视图

> **对应文档**: 一、框架全景图 — 三层级结构可视化 + 五、年度时间计划(DSTE日历)

**Files:**
- Modify: `app/templates/base.html`
- Create: `app/templates/_nav.html`
- Modify: `app/static/css/main.css`

## Step 1: 三层级导航条组件 (_nav.html)

```html
<nav class="tier-nav" id="step-navigation">
    <!-- Tier1: 五看三定 -->
    <div class="tier-group">
        <div class="tier-header tier1">
            <span class="tier-badge">Tier1</span>
            五看三定 <small>战略洞察+制定 · 4-9月</small>
        </div>
        <div class="tier-steps">
            <a href="/step/L1_industry" class="step-item ...">1 看行业</a>
            <a href="/step/L2_customer" class="step-item ...">2 看客户</a>
            <!-- ... L3-L8 ... -->
        </div>
    </div>
    
    <!-- Tier2: BEM -->
    <div class="tier-group">
        <div class="tier-header tier2">
            <span class="tier-badge">Tier2</span>
            BEM <small>战略解码 · 10-12月</small>
        </div>
        <div class="tier-steps">
            <a href="/step/B1_csf" class="step-item ...">CSF导出</a>
            <!-- ... B2-B5 ... -->
        </div>
    </div>
    
    <!-- Tier3: DSTE -->
    <div class="tier-group">
        <div class="tier-header tier3">
            <span class="tier-badge">Tier3</span>
            DSTE <small>全流程管理 · 全年</small>
        </div>
        <div class="tier-steps">
            <a href="/step/D1_execution" class="step-item ...">SP/BP执行监控</a>
            <!-- ... D2-D3 ... -->
        </div>
    </div>
</nav>
```

## Step 2: DSTE日历组件 (_dste_calendar.html)

```html
<div class="dste-calendar">
    <h3>📅 DSTE年度日历</h3>
    <div class="calendar-grid">
        {% for month in dste_months %}
        <div class="month-card {% if month.is_current %}current{% endif %}">
            <div class="month-header">{{ month.label }}</div>
            <div class="month-phase">{{ month.phase }}</div>
            <div class="month-tasks">{{ month.tasks }}</div>
            <div class="month-skills">
                {% for skill in month.skills %}
                <span class="skill-tag">{{ skill }}</span>
                {% endfor %}
            </div>
            <div class="month-output">{{ month.output }}</div>
        </div>
        {% endfor %}
    </div>
</div>
```

DSTE月份数据（10个月度卡片）:
- 4月: 启动 → planning-with-files → 研究计划
- 5-6月: 五看(行业/客户/竞争) → sn-deep-research+mbb-strategist → 子报告
- 7月: 五看(自己/机会) → mbb-strategist+excel
- 8月: 三定 → mbb-strategist → 战略草案
- 9月: 评审 → Executive Synthesis → L1报告
- 10月: 解码(CSF/KPI) → excel-analysis
- 11月: 解码(重点/PBC) → planning-with-files → L2方案
- 12月: 预算 → excel-analysis
- 1-3月: 执行 → planning-with-files → 执行报告
- 4月(次年): 复盘 → sn-research-synthesis → 复盘报告

## Step 3: 整合到 base.html

在导航区域放置可切换的两个视图：步骤导航 / DSTE日历

## Step 4: Commit

```bash
git add -A && git commit -m "feat: three-tier navigation bar + DSTE calendar view"
```
