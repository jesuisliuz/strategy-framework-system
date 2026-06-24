# Task 12: L1/L2/L3 三级报告生成器

**Files:**
- Create: `app/report.py`

## Step 1: 报告数据结构

```python
"""三级战略报告生成器"""
from .models import AnalyzeContext, STEP_DEFINITIONS


class ReportGenerator:
    """将8步分析结果聚合为三级报告"""
    
    LEVELS = {
        "L1": {
            "title": "战略洞察报告",
            "subtitle": "华为五看三定 · 第一级产出",
            "word_count": "10,000-30,000字",
            "source_steps": ["L1_industry", "L2_customer", "L3_competition", 
                           "L4_internal", "L5_opportunity"],
        },
        "L2": {
            "title": "战略解码报告", 
            "subtitle": "BEM战略解码 · 第二级产出",
            "word_count": "5,000-10,000字",
            "source_steps": ["L6_objective", "L7_strategy", "L8_control"],
        },
        "L3": {
            "title": "落地执行报告",
            "subtitle": "DSTE年度循环 · 第三级产出",
            "word_count": "2,000-5,000字",
            "source_steps": ["final_report"],  # 从final_report结果中提取
        },
    }
    
    @staticmethod
    def generate(ctx: AnalyzeContext, level: str) -> str:
        """生成指定级别的报告（Markdown格式）"""
        config = ReportGenerator.LEVELS[level]
        
        # 收集源步骤输出
        sections = []
        for sid in config["source_steps"]:
            out = ctx.get_step_output(sid)
            if out.status in ("done", "stale"):
                sections.append({
                    "step_id": sid,
                    "name": STEP_DEFINITIONS[sid]["name"],
                    "content": out.content,
                    "data": out.data
                })
        
        if not sections:
            return ReportGenerator._empty_report(config, ctx)
        
        return ReportGenerator._assemble_report(config, sections, ctx)
    
    @staticmethod
    def _assemble_report(config: dict, sections: list, ctx: AnalyzeContext) -> str:
        """组装报告"""
        lines = []
        
        # 封面
        lines.append(f"# {config['title']}")
        lines.append(f"*{config['subtitle']}*")
        lines.append(f"")
        lines.append(f"**项目名称**: {ctx.project_name}")
        lines.append(f"**生成时间**: {ctx.created_at}")
        lines.append(f"**目标字数**: {config['word_count']}")
        lines.append(f"")
        lines.append("---")
        lines.append("")
        
        # 目录
        lines.append("## 目录")
        for i, sec in enumerate(sections, 1):
            lines.append(f"{i}. [{sec['name']}](#{sec['step_id']})")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # 各步骤内容
        for sec in sections:
            lines.append(f"<a id='{sec['step_id']}'></a>")
            lines.append(sec["content"])
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # 综合判断
        lines.append("## 综合战略判断")
        lines.append("*基于以上分析，系统自动生成的战略建议...*")
        lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def _empty_report(config: dict, ctx: AnalyzeContext) -> str:
        """未完成时的空报告提示"""
        return f"""# {config['title']}

*{config['subtitle']}*

⚠️ 该报告依赖的源步骤尚未全部完成。

已完成步骤: {len([s for s in config['source_steps'] if ctx.get_step_output(s).status == 'done'])} / {len(config['source_steps'])}

请先完成相关步骤的分析。"""


def generate_full_report(ctx: AnalyzeContext) -> dict:
    """生成完整的三级报告"""
    return {
        "L1": ReportGenerator.generate(ctx, "L1"),
        "L2": ReportGenerator.generate(ctx, "L2"),
        "L3": ReportGenerator.generate(ctx, "L3"),
    }
```

## Step 2: 报告导出API

在 app.py 中添加：

```python
@app.route("/api/report/<level>")
def get_report(level):
    sid = request.args.get("session_id")
    ctx = get_session(sid)
    if not ctx:
        return "Session not found", 404
    if level not in ("L1", "L2", "L3"):
        return "Invalid level", 400
    
    report = ReportGenerator.generate(ctx, level)
    return jsonify({"level": level, "content": report, "title": ReportGenerator.LEVELS[level]["title"]})

@app.route("/api/report/full")
def get_full_report():
    sid = request.args.get("session_id")
    ctx = get_session(sid)
    if not ctx:
        return "Session not found", 404
    return jsonify(generate_full_report(ctx))
```

## Step 3: 验证

```python
from app.report import ReportGenerator, generate_full_report

ctx = _build_full_mock_context()
l1 = ReportGenerator.generate(ctx, "L1")
assert "战略洞察报告" in l1
assert ctx.project_name in l1

full = generate_full_report(ctx)
assert set(full.keys()) == {"L1", "L2", "L3"}
print("PASS")
```

## Step 4: Commit

```bash
git add -A
git commit -m "feat: L1/L2/L3 three-tier report generator"
git push origin main
```
