# Task 22: 三级报告最终展示页面

**Files:**
- Create: `app/templates/report.html`
- Modify: `app/app.py`

## Step 1: 报告页面路由

```python
@app.route("/report")
def report_page():
    ctx = get_session(request.args.get("session_id"))
    # 统计三层级完成度
    tier1_done = count_completed_tier(ctx, "tier1")
    tier2_done = count_completed_tier(ctx, "tier2")
    tier3_done = count_completed_tier(ctx, "tier3")
    return render_template("report.html", ctx=ctx, 
                          tier1_done=tier1_done, tier2_done=tier2_done, tier3_done=tier3_done)
```

## Step 2: 报告页面 (report.html)

- 三层级完成度横幅
- L1/L2/L3 三个标签页
- 每页从 `/api/report/L1?session_id=X` 加载
- Markdown渲染（marked.js）
- 复制全文 / 下载Markdown 按钮
- "返回分析" 链接

## Step 3: 质量摘要区域

在报告页面顶部显示：
- 已使用技能清单
- 步骤完成百分比
- 报告字数统计

## Step 4: Commit

```bash
git add -A && git commit -m "feat: final report page — L1/L2/L3 tabs + markdown + export"
```
