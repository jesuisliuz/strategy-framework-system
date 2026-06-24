# Task 25: 4场景技能调用编排器

> **对应文档**: 六、技能调用流程 — 4个场景的完整调用序列

**Files:**
- Create: `app/scenario_orchestrator.py`

## Step 1: 场景编排引擎

```python
class ScenarioOrchestrator:
    """按场景编排技能调用序列"""
    
    SCENARIOS = {
        "industry_research": {
            "name": "行业研究",
            "steps": [
                {"skill": "sn-deep-research", "action": "初始化研究", "params": {"topic": "{industry_name}"}},
                {"skill": "sn-research-planning", "action": "生成研究计划", "output_key": "plan"},
                {"skill": "sn-dimension-research", "action": "行业维度取证", "depends_on": "plan"},
                {"skill": "sn-search-academic", "action": "学术论文搜索", "indent": 1},
                {"skill": "sn-search-social-cn", "action": "中文社交搜索", "indent": 1},
                {"skill": "sn-search-social-en", "action": "英文社交搜索", "indent": 1},
                {"skill": "mbb-strategist", "action": "Industry Trends框架分析", "params": {"framework": "Industry Trends"}},
                {"skill": "sn-research-synthesis", "action": "综合判断", "depends_on": "research_results"},
                {"skill": "sn-research-report", "action": "生成子报告", "depends_on": "synthesis_result"},
            ],
        },
        "competition_analysis": {
            "name": "竞品分析",
            "steps": [
                {"skill": "mbb-strategist", "action": "SWOT分析", "params": {"framework": "SWOT"}},
                {"skill": "mbb-strategist", "action": "波特五力分析", "params": {"framework": "Porter's Five Forces"}},
                {"skill": "sn-search-code", "action": "竞品技术搜索"},
                {"skill": "excel-bar-chart-visualization", "action": "竞品对比图"},
            ],
        },
        "kpi_design": {
            "name": "KPI设计",
            "steps": [
                {"skill": "excel-data-analysis", "action": "KPI体系设计"},
                {"skill": "excel-threshold-analysis-and-styling", "action": "KPI阈值设定"},
                {"skill": "excel-outlier-detection-and-quality-assessment", "action": "异常值识别"},
            ],
        },
        "execution_tracking": {
            "name": "执行跟踪",
            "steps": [
                {"skill": "planning-with-files", "action": "progress.md 进度跟踪"},
                {"skill": "excel-line-chart-visualization", "action": "进度图"},
                {"skill": "excel-trend-analysis", "action": "趋势偏差分析"},
                {"skill": "statistical-distribution-and-outlier-analysis", "action": "异常检测"},
            ],
        },
    }
    
    @staticmethod
    def execute_scenario(scenario_id: str, ctx, params: dict) -> dict:
        """按序列执行场景的所有技能调用"""
        
    @staticmethod
    def get_scenario_flow(scenario_id: str) -> list:
        """获取场景的调用流程图（供前端展示）"""
```

## Step 2: API端点

```python
@app.route("/api/scenario/execute", methods=["POST"])
def execute_scenario():
    """POST {scenario_id, session_id, params} → 执行完整场景调用链"""
```

## Step 3: Commit

```bash
git add -A && git commit -m "feat: 4-scenario orchestrator — call chain executor matching user spec section 6"
```
