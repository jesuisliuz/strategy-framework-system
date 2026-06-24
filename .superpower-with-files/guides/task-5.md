# Task 5: 步骤定义引擎与API路由

**Files:**
- Modify: `app/models.py` → 补全 STEP_DEFINITIONS
- Modify: `app/app.py` → 添加路由
- Create: `app/steps.py`

## Step 1: 补全 STEP_DEFINITIONS（完整八步+最终报告定义）

在 `app/models.py` 中补全，包含以下结构：

```
L1_industry:   看行业/趋势    → fields: 行业名称/市场规模/增长率/TAM/趋势驱动/技术趋势
L2_customer:   看客户        → fields: 目标客群描述/购买动因/$APPEALS评分/未满足需求
L3_competition: 看竞争       → fields: 竞对名称/市场份额/优劣势/战略集团参数
L4_internal:   看自己        → fields: 资源清单/核心能力自评/组织健康度
L5_opportunity: 看机会       → fields: 机会列表/市场吸引力/竞争力评估/SPAN象限数据
L6_objective:  定目标        → fields: 战略意图/Vision/KPI基线/目标差距
L7_strategy:   定策略        → fields: 业务设计/创新焦点/关键任务/资源分配
L8_control:    定控制点      → fields: 护城河类型/控制强度/风险场景/Plan B
final_report:  最终报告      → 聚合所有步骤，生成三级报告
```

每个步骤定义包含：
- `name`: 中文名称
- `number`: 步骤序号 1-9
- `method`: 方法论标注（五看/三定/DSTE）
- `fields`: 输入字段列表 [{id, label, type, required, placeholder}]
- `output_sections`: 输出区块标题列表

## Step 2: 创建步骤处理引擎 (steps.py)

```python
"""步骤分析引擎——将输入转化为分析输出"""
from .models import AnalyzeContext, STEP_DEFINITIONS


class StepEngine:
    """负责单个步骤的分析逻辑"""
    
    @staticmethod
    def analyze(step_id: str, ctx: AnalyzeContext) -> str:
        """分析单个步骤，返回Markdown结果"""
        step_def = STEP_DEFINITIONS.get(step_id, {})
        step_input = ctx.get_step_input(step_id)
        upstream = StepEngine._gather_upstream(step_id, ctx)
        
        # 构建分析prompt（各步骤自定义）
        prompt = StepEngine._build_prompt(step_id, step_def, step_input, upstream)
        
        # 模拟分析结果（Phase 4替换为真实LLM调用）
        result = StepEngine._mock_analyze(step_id, step_input.fields)
        
        return result
    
    @staticmethod
    def _gather_upstream(step_id: str, ctx: AnalyzeContext) -> dict:
        """收集上游已完成步骤的输出摘要"""
        # 按步骤顺序收集
        pass
    
    @staticmethod
    def _build_prompt(step_id, step_def, step_input, upstream) -> str:
        """构建分析提示词"""
        pass
    
    @staticmethod
    def _mock_analyze(step_id: str, fields: dict) -> str:
        """临时mock——返回结构化占位分析结果"""
        step_name = STEP_DEFINITIONS.get(step_id, {}).get("name", step_id)
        return f"## {step_name}\n\n*分析引擎就绪，等待LLM接入...*\n\n已接收输入字段: {list(fields.keys())}\n"
```

## Step 3: 添加API路由 (app.py)

```python
# === 新增导入 ===
from flask import request, jsonify, session as flask_session
from app.models import AnalyzeContext, STEP_DEFINITIONS
from app.session import get_session, create_session, save_session
from app.steps import StepEngine

# === 新增路由 ===

@app.route("/api/session/start", methods=["POST"])
def start_session():
    ctx = create_session()
    save_session(ctx)
    return jsonify({"session_id": ctx.session_id})

@app.route("/api/step/<step_id>", methods=["GET"])
def get_step(step_id):
    sid = request.args.get("session_id")
    ctx = get_session(sid)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404
    step_def = STEP_DEFINITIONS.get(step_id)
    step_data = ctx.steps.get(step_id)
    return jsonify({
        "definition": step_def,
        "input": step_data["input"].to_dict() if step_data else {},
        "output": step_data["output"].to_dict() if step_data else {},
    })

@app.route("/api/step/<step_id>/save", methods=["POST"])
def save_step_input(step_id):
    data = request.get_json()
    sid = data.get("session_id")
    ctx = get_session(sid)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404
    
    # 保存输入
    ctx.steps[step_id]["input"].fields = data.get("fields", {})
    
    # 标记下游为 stale
    ctx.invalidate_downstream(step_id)
    
    # 执行当前步骤分析
    result = StepEngine.analyze(step_id, ctx)
    ctx.set_step_result(step_id, result, summary=result[:100])
    
    save_session(ctx)
    return jsonify({"status": "ok", "step": ctx.steps[step_id]["output"].to_dict()})

@app.route("/api/context/<session_id>", methods=["GET"])
def get_context(session_id):
    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Not found"}), 404
    return jsonify(ctx.to_dict())
```

## Step 4: 更新主页路由支持会话

修改 index 路由，创建默认会话并重定向到步骤1。

## Step 5: 验证

```bash
cd /c/Users/jesui/Projects/strategy-framework-system
python -c "
from app.models import STEP_DEFINITIONS
for k, v in STEP_DEFINITIONS.items():
    print(f'{k}: {v[\"name\"]} — {len(v[\"fields\"])} fields, {len(v.get(\"output_sections\",[]))} sections')
"
```

## Step 6: Commit

```bash
git add -A
git commit -m "feat: step definitions + API routes + mock engine"
git push origin main
```
