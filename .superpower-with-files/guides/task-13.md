# Task 13: 最终报告展示页面

**Files:**
- Create: `app/templates/report.html`
- Modify: `app/app.py` → 添加报告页面路由
- Modify: `app/static/css/main.css`

## Step 1: 报告页面路由

```python
@app.route("/report")
def report_page():
    sid = request.args.get("session_id")
    ctx = get_session(sid)
    if not ctx:
        return redirect("/")
    
    # 检查所有步骤完成度
    completed = sum(1 for s in ctx.steps.values() 
                   if s["output"].status == "done")
    
    return render_template("report.html", 
                          ctx=ctx, 
                          completed=completed,
                          total=8)
```

## Step 2: 报告页面模板 (report.html)

```html
{% extends "base.html" %}
{% block title %}最终报告 - {{ ctx.project_name }}{% endblock %}

{% block content %}
<div class="report-page">
    <!-- 报告状态横幅 -->
    <div class="report-banner {% if completed >= 8 %}complete{% else %}incomplete{% endif %}">
        <h1>📊 战略分析最终报告</h1>
        <p>项目: {{ ctx.project_name }} | 完成度: {{ completed }}/8 步骤</p>
    </div>
    
    <!-- 三级报告标签切换 -->
    <div class="report-tabs">
        <button class="tab active" onclick="switchTab('L1')" id="tab-L1">
            L1 战略洞察
        </button>
        <button class="tab" onclick="switchTab('L2')" id="tab-L2">
            L2 战略解码
        </button>
        <button class="tab" onclick="switchTab('L3')" id="tab-L3">
            L3 落地执行
        </button>
    </div>
    
    <!-- 报告内容区 -->
    <div class="report-content" id="report-content">
        <div class="report-loading">
            <div class="spinner"></div>
            <p>正在生成报告...</p>
        </div>
    </div>
    
    <!-- 导出操作 -->
    <div class="report-actions">
        <button class="btn-export" onclick="copyReport()">📋 复制全文</button>
        <button class="btn-export" onclick="downloadReport()">📥 下载 Markdown</button>
        <a href="/" class="btn-back">← 返回分析</a>
    </div>
</div>

<script>
// 页面加载时获取L1报告
fetchReport('L1');

async function fetchReport(level) {
    const sid = new URLSearchParams(window.location.search).get('session_id');
    const resp = await fetch(`/api/report/${level}?session_id=${sid}`);
    const data = await resp.json();
    document.getElementById('report-content').innerHTML = 
        `<div class="markdown-body">${marked.parse(data.content)}</div>`;
}

function switchTab(level) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById('tab-' + level).classList.add('active');
    document.getElementById('report-content').innerHTML = 
        '<div class="report-loading"><div class="spinner"></div><p>加载中...</p></div>';
    fetchReport(level);
}

function downloadReport() {
    const content = document.getElementById('report-content').innerText;
    const blob = new Blob([content], {type: 'text/markdown'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = '战略分析报告.md';
    a.click();
    URL.revokeObjectURL(url);
}
</script>
{% endblock %}
```

## Step 3: 引入 Markdown 渲染

在 base.html 的 head 中添加：
```html
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
```

## Step 4: 报告页面CSS

- `.report-banner`: 渐变背景，完成/未完成两种颜色
- `.report-tabs`: 标签页切换，Active标签有金色底部边框
- `.report-content`: 最大宽度900px，居中，Markdown正文样式
- `.report-actions`: 固定在底部

## Step 5: 验证

1. 启动应用，完成至少前5步
2. 点击步骤导航条的"最终报告"按钮
3. 验证L1/L2/L3标签切换正常
4. 验证下载按钮生成 .md 文件

## Step 6: Commit

```bash
git add -A
git commit -m "feat: final report page with L1/L2/L3 tabs + markdown rendering"
git push origin main
```
