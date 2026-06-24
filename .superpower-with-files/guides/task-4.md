# Task 4: AnalyzeContext 数据模型与会话管理

**Files:**
- Create: `app/models.py`
- Create: `app/session.py`

## Step 1: 定义数据模型 (models.py)

```python
"""华为三板斧战略分析数据模型"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import uuid
import json


@dataclass
class StepInput:
    """单步骤输入数据"""
    fields: dict = field(default_factory=dict)  # {field_name: value}
    
    def to_dict(self):
        return {"fields": self.fields}


@dataclass
class StepOutput:
    """单步骤输出数据"""
    content: str = ""          # Markdown格式分析结果
    summary: str = ""          # 一句话摘要
    data: dict = field(default_factory=dict)  # 结构化数据（SPAN坐标、KPI值等）
    status: str = "pending"    # pending | analyzing | done | error
    
    def to_dict(self):
        return {
            "content": self.content,
            "summary": self.summary,
            "data": self.data,
            "status": self.status
        }


@dataclass
class AnalyzeContext:
    """分析上下文——贯穿全流程的核心对象"""
    session_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    project_name: str = "未命名项目"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 8步 + 最终报告
    steps: dict = field(default_factory=lambda: {
        "L1_industry": {"input": StepInput(), "output": StepOutput()},
        "L2_customer": {"input": StepInput(), "output": StepOutput()},
        "L3_competition": {"input": StepInput(), "output": StepOutput()},
        "L4_internal": {"input": StepInput(), "output": StepOutput()},
        "L5_opportunity": {"input": StepInput(), "output": StepOutput()},
        "L6_objective": {"input": StepInput(), "output": StepOutput()},
        "L7_strategy": {"input": StepInput(), "output": StepOutput()},
        "L8_control": {"input": StepInput(), "output": StepOutput()},
        "final_report": {"input": StepInput(), "output": StepOutput()},
    })
    
    # 分析日志
    log: list = field(default_factory=list)
    
    def get_step_input(self, step_id: str) -> StepInput:
        return self.steps[step_id]["input"]
    
    def get_step_output(self, step_id: str) -> StepOutput:
        return self.steps[step_id]["output"]
    
    def set_step_result(self, step_id: str, content: str, summary: str = "", data: dict = None):
        self.steps[step_id]["output"].content = content
        self.steps[step_id]["output"].summary = summary
        self.steps[step_id]["output"].data = data or {}
        self.steps[step_id]["output"].status = "done"
    
    def invalidate_downstream(self, from_step_id: str):
        """标记下游步骤为需要重新计算"""
        step_order = ["L1_industry", "L2_customer", "L3_competition", 
                      "L4_internal", "L5_opportunity", "L6_objective",
                      "L7_strategy", "L8_control", "final_report"]
        start = step_order.index(from_step_id) + 1
        for sid in step_order[start:]:
            if self.steps[sid]["output"].status == "done":
                self.steps[sid]["output"].status = "stale"
                self.log.append(f"[{datetime.now().isoformat()}] {sid} marked stale due to {from_step_id} change")
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "project_name": self.project_name,
            "created_at": self.created_at,
            "steps": {
                k: {"input": v["input"].to_dict(), "output": v["output"].to_dict()}
                for k, v in self.steps.items()
            },
            "log": self.log[-50:]  # 最近50条日志
        }
```

### Step Definitions（硬编码在模型中）

```python
STEP_DEFINITIONS = {
    "L1_industry": {
        "name": "看行业/趋势",
        "number": 1,
        "method": "五看 · 看行业",
        "fields": [
            {"id": "industry_name", "label": "行业名称", "type": "text", "required": True, "placeholder": "如：新能源汽车"},
            {"id": "market_size", "label": "当前市场规模（亿元）", "type": "number", "required": False},
            {"id": "growth_rate", "label": "年增长率（%）", "type": "number", "required": False},
            {"id": "tam", "label": "TAM（总可寻址市场）", "type": "text", "required": False},
            {"id": "key_trends", "label": "关键趋势驱动因素（每行一个）", "type": "textarea", "required": True, "placeholder": "如：\n政策推动碳中和\n电池成本持续下降\n消费者环保意识提升"},
            {"id": "technology_trends", "label": "关键技术趋势", "type": "textarea", "required": False},
            {"id": "additional_context", "label": "补充背景信息", "type": "textarea", "required": False, "placeholder": "任何有助于分析的上下文..."},
        ],
        "output_sections": ["宏观环境(PEST)", "市场格局(波特五力)", "技术趋势", "关键发现与战略启示"]
    },
    # ... L2-L8, final_report (定义在Task 5)
}
```

## Step 2: 编写会话管理 (session.py)

```python
"""会话管理——内存存储，按需持久化"""
import json
import os
from datetime import datetime, timedelta
from .models import AnalyzeContext

# 内存存储
_sessions: dict = {}

# 持久化路径
INSTANCE_DIR = os.path.join(os.path.dirname(__file__), "instance")


def get_session(session_id: str) -> AnalyzeContext:
    """获取或创建会话"""
    if session_id not in _sessions:
        # 尝试从磁盘恢复
        filepath = os.path.join(INSTANCE_DIR, f"{session_id}.json")
        if os.path.exists(filepath):
            with open(filepath) as f:
                data = json.load(f)
            ctx = _deserialize(data)
            _sessions[session_id] = ctx
        else:
            return None
    return _sessions.get(session_id)


def create_session() -> AnalyzeContext:
    ctx = AnalyzeContext()
    _sessions[ctx.session_id] = ctx
    return ctx


def save_session(ctx: AnalyzeContext):
    _sessions[ctx.session_id] = ctx
    # 异步落盘
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    filepath = os.path.join(INSTANCE_DIR, f"{ctx.session_id}.json")
    with open(filepath, "w") as f:
        json.dump(ctx.to_dict(), f, ensure_ascii=False, indent=2)


def _deserialize(data: dict) -> AnalyzeContext:
    # 从JSON恢复AnalyzeContext对象
    from .models import StepInput, StepOutput
    ctx = AnalyzeContext(
        session_id=data["session_id"],
        project_name=data.get("project_name", ""),
        created_at=data.get("created_at", ""),
    )
    for sid, sdata in data.get("steps", {}).items():
        inp = sdata.get("input", {})
        out = sdata.get("output", {})
        ctx.steps[sid]["input"].fields = inp.get("fields", {})
        ctx.steps[sid]["output"].content = out.get("content", "")
        ctx.steps[sid]["output"].summary = out.get("summary", "")
        ctx.steps[sid]["output"].data = out.get("data", {})
        ctx.steps[sid]["output"].status = out.get("status", "pending")
    ctx.log = data.get("log", [])
    return ctx
```

## Step 3: 验证模型导入

```bash
cd /c/Users/jesui/Projects/strategy-framework-system
python -c "from app.models import AnalyzeContext, STEP_DEFINITIONS; ctx = AnalyzeContext(); print(ctx.session_id)"
```

## Step 4: Commit

```bash
git add -A
git commit -m "feat: AnalyzeContext data model + session management"
git push origin main
```
