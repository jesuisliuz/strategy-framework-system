# Task 24: DSTE年度日历视图

> **对应文档**: 五、年度时间计划（DSTE日历）— 4月→9月→12月→次年3月→4月

**Files:**
- Create: `app/templates/dste_calendar.html`
- Modify: `app/app.py`

## Step 1: DSTE日历数据

```python
DSTE_CALENDAR = [
    {"month": 4, "label": "4月", "phase": "启动", "tasks": "启动战略规划，明确研究范围", "skills": ["planning-with-files"], "outputs": ["研究计划"]},
    {"month": 5, "label": "5-6月", "phase": "五看", "tasks": "看行业/趋势、看客户、看竞争", "skills": ["sn-deep-research", "mbb-strategist"], "outputs": ["子报告"]},
    {"month": 7, "label": "7月", "phase": "五看", "tasks": "看自己、看机会", "skills": ["mbb-strategist", "excel-data-analysis"], "outputs": ["子报告"]},
    {"month": 8, "label": "8月", "phase": "三定", "tasks": "定目标、定策略、定控制点", "skills": ["mbb-strategist"], "outputs": ["战略草案"]},
    {"month": 9, "label": "9月", "phase": "评审", "tasks": "战略评审与定稿", "skills": ["mbb-strategist(Executive Synthesis)"], "outputs": ["L1报告"]},
    {"month": 10, "label": "10月", "phase": "解码", "tasks": "CSF/KPI导出", "skills": ["excel-data-analysis"], "outputs": ["CSF/KPI清单"]},
    {"month": 11, "label": "11月", "phase": "解码", "tasks": "重点工作分解、PBC签订", "skills": ["planning-with-files"], "outputs": ["L2方案"]},
    {"month": 12, "label": "12月", "phase": "预算", "tasks": "预算编制与审批", "skills": ["excel-data-analysis"], "outputs": ["预算方案"]},
    {"month": 1, "label": "1-3月", "phase": "执行", "tasks": "执行与监控", "skills": ["planning-with-files"], "outputs": ["执行报告"]},
    {"month": 4, "label": "4月(次年)", "phase": "复盘", "tasks": "战略复盘与迭代", "skills": ["sn-research-synthesis"], "outputs": ["复盘报告"]},
]
```

## Step 2: 日历页面 (dste_calendar.html)

- 10个月度卡片网格
- 当前月份高亮
- 每张卡片显示: 阶段标签、核心任务、技能图标、输出物
- 点击卡片跳转到对应步骤

## Step 3: 路由

```python
@app.route("/calendar")
def calendar_page():
    return render_template("dste_calendar.html", calendar=DSTE_CALENDAR)
```

## Step 4: Commit

```bash
git add -A && git commit -m "feat: DSTE annual calendar view — 10-month cycle visualization"
```
