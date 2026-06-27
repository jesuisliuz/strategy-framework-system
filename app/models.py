"""
三层级数据模型 + AnalyzeContext

核心设计：
- TIER_DEFINITIONS: 三层级元数据（Tier1/Tier2/Tier3）
- STEP_DEFINITIONS: 19步完整定义（从 step_definitions.json 加载）
- AnalyzeContext: 分析会话上下文，支持跨层级级联失效
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


# =============================================================================
# 1. 三层级定义
# =============================================================================

TIER_DEFINITIONS = {
    "tier1": {
        "name": "五看三定",
        "subtitle": "战略洞察 + 战略制定",
        "timeframe": "4月-9月（7个月）",
        "core_skills": ["sn-deep-research", "mbb-strategist"],
        "aux_skills": ["sn-search系列", "Excel分析系列"],
        "output": "L1 战略洞察报告",
        "word_count": "10,000-30,000字",
        "steps": ["L1_industry", "L2_customer", "L3_competition", "L4_internal",
                   "L5_opportunity", "L6_objective", "L7_strategy", "L8_control"],
    },
    "tier2": {
        "name": "BEM",
        "subtitle": "战略解码",
        "timeframe": "10月-12月（3个月）",
        "core_skills": ["Excel分析系列", "planning-with-files"],
        "aux_skills": [],
        "output": "L2 战略解码方案",
        "word_count": "5,000-10,000字",
        "steps": ["B1_csf", "B2_kpi", "B3_ctq", "B4_keytasks", "B5_pbc"],
    },
    "tier3": {
        "name": "DSTE",
        "subtitle": "全流程管理",
        "timeframe": "1月-12月（全年循环）",
        "core_skills": ["planning-with-files", "Excel分析系列"],
        "aux_skills": [],
        "output": "L3 落地执行方案",
        "word_count": "2,000-5,000字",
        "steps": ["D1_execution", "D2_analysis", "D3_review"],
    },
}

# 步骤依赖关系（上游→下游）
STEP_DEPENDENCIES = {
    # Tier1 五看三定
    "L1_industry": [],
    "L2_customer": [],
    "L3_competition": [],
    "L4_internal": [],
    "L5_opportunity": ["L1_industry", "L2_customer", "L3_competition", "L4_internal"],
    "L6_objective": ["L5_opportunity"],
    "L7_strategy": ["L6_objective"],
    "L8_control": ["L7_strategy"],
    # Tier2 BEM（依赖 Tier1 输出）
    "B1_csf": ["L6_objective", "L7_strategy", "L8_control"],
    "B2_kpi": ["B1_csf"],
    "B3_ctq": ["B2_kpi"],
    "B4_keytasks": ["B3_ctq"],
    "B5_pbc": ["B4_keytasks"],
    # Tier3 DSTE（依赖 Tier2 输出）
    "D1_execution": ["B5_pbc"],
    "D2_analysis": ["D1_execution"],
    "D3_review": ["D2_analysis"],
    # 验证
    "cross_validation": ["L8_control", "B5_pbc", "D3_review"],
}

# 步骤顺序（用于前端展示和级联失效）
STEP_ORDER = [
    "L1_industry", "L2_customer", "L3_competition", "L4_internal", "L5_opportunity",
    "L6_objective", "L7_strategy", "L8_control",
    "B1_csf", "B2_kpi", "B3_ctq", "B4_keytasks", "B5_pbc",
    "D1_execution", "D2_analysis", "D3_review",
    "cross_validation",
]


# =============================================================================
# 2. 步骤定义加载
# =============================================================================

def load_step_definitions() -> list:
    """加载 step_definitions.json 中的步骤定义。"""
    path = os.path.join(os.path.dirname(__file__), "data", "step_definitions.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("steps", [])


ALL_STEPS = load_step_definitions()


def get_step_definition(step_id: str) -> dict:
    """获取单个步骤的定义。"""
    for step in ALL_STEPS:
        if step.get("step_id") == step_id:
            return step
    return {}


def get_steps_by_tier() -> dict:
    """按层级分组获取步骤定义。"""
    return {
        "tier1": [s for s in ALL_STEPS if s.get("tier") == "tier1"],
        "tier2": [s for s in ALL_STEPS if s.get("tier") == "tier2"],
        "tier3": [s for s in ALL_STEPS if s.get("tier") == "tier3"],
        "validation": [s for s in ALL_STEPS if s.get("tier") == "validation"],
    }


# =============================================================================
# 3. AnalyzeContext 数据模型
# =============================================================================

@dataclass
class StepState:
    """单个步骤的状态。"""
    step_id: str
    status: str = "pending"  # pending / running / done / stale / error
    input: dict = field(default_factory=dict)
    output: dict = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    error: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def to_dict(self) -> dict:
        return {
            "step_id": self.step_id,
            "status": self.status,
            "input": self.input,
            "output": self.output,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StepState":
        return cls(
            step_id=data.get("step_id", ""),
            status=data.get("status", "pending"),
            input=data.get("input", {}),
            output=data.get("output", {}),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            error=data.get("error", ""),
        )


@dataclass
class AnalyzeContext:
    """分析会话上下文。

    持久化所有状态，支持断点续跑和跨层级级联失效。
    """
    session_id: str
    project_name: str
    created_at: str = ""
    current_tier: str = "tier1"
    current_step: str = "L1_industry"

    # 步骤状态
    steps: dict = field(default_factory=dict)  # step_id -> StepState

    # DSTE 日历状态
    dste_calendar: dict = field(default_factory=dict)

    # 分析日志
    log: list = field(default_factory=list)

    # 配置快照
    config_snapshot: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    # ---- 步骤操作 ----

    def get_step(self, step_id: str) -> Optional[StepState]:
        """获取步骤状态。"""
        return self.steps.get(step_id)

    def get_step_input(self, step_id: str) -> dict:
        """获取步骤输入。"""
        step = self.steps.get(step_id)
        return step.input if step else {}

    def set_step_input(self, step_id: str, input_data: dict) -> None:
        """设置步骤输入。"""
        if step_id not in self.steps:
            self.steps[step_id] = StepState(step_id=step_id)
        self.steps[step_id].input = input_data
        self.steps[step_id].updated_at = datetime.now().isoformat()

    def set_step_output(self, step_id: str, output_data: dict) -> None:
        """设置步骤输出。"""
        if step_id not in self.steps:
            self.steps[step_id] = StepState(step_id=step_id)
        self.steps[step_id].output = output_data
        self.steps[step_id].status = "done"
        self.steps[step_id].updated_at = datetime.now().isoformat()
        self._log(f"Step {step_id} completed")

    def set_step_status(self, step_id: str, status: str, error: str = "") -> None:
        """设置步骤状态。"""
        if step_id not in self.steps:
            self.steps[step_id] = StepState(step_id=step_id)
        self.steps[step_id].status = status
        self.steps[step_id].error = error
        self.steps[step_id].updated_at = datetime.now().isoformat()

    def is_step_done(self, step_id: str) -> bool:
        """检查步骤是否完成。"""
        step = self.steps.get(step_id)
        return step is not None and step.status == "done"

    def is_step_stale(self, step_id: str) -> bool:
        """检查步骤是否过期。"""
        step = self.steps.get(step_id)
        return step is not None and step.status == "stale"

    # ---- 级联失效 ----

    def invalidate_downstream(self, from_step_id: str) -> list:
        """标记所有下游步骤为 stale。

        跨层级级联：
        - Tier1 修改 → Tier2 stale
        - Tier2 修改 → Tier3 stale
        """
        invalidated = []
        downstream = self._get_downstream_steps(from_step_id)

        for step_id in downstream:
            if step_id in self.steps:
                if self.steps[step_id].status == "done":
                    self.steps[step_id].status = "stale"
                    self.steps[step_id].updated_at = datetime.now().isoformat()
                    invalidated.append(step_id)
                    self._log(f"Step {step_id} invalidated (downstream of {from_step_id})")

        return invalidated

    def _get_downstream_steps(self, step_id: str) -> list:
        """获取所有下游步骤。"""
        downstream = []
        for sid, deps in STEP_DEPENDENCIES.items():
            if step_id in deps:
                downstream.append(sid)
                downstream.extend(self._get_downstream_steps(sid))
        return list(dict.fromkeys(downstream))  # 去重保序

    def get_ready_steps(self) -> list:
        """获取可以执行的步骤（所有依赖已完成）。"""
        ready = []
        for step_id in STEP_ORDER:
            deps = STEP_DEPENDENCIES.get(step_id, [])
            if all(self.is_step_done(d) for d in deps):
                step = self.steps.get(step_id)
                if step is None or step.status in ("pending", "stale", "error"):
                    ready.append(step_id)
        return ready

    # ---- 序列化 ----

    def to_dict(self) -> dict:
        """序列化为字典。"""
        return {
            "session_id": self.session_id,
            "project_name": self.project_name,
            "created_at": self.created_at,
            "current_tier": self.current_tier,
            "current_step": self.current_step,
            "steps": {sid: s.to_dict() for sid, s in self.steps.items()},
            "dste_calendar": self.dste_calendar,
            "log": self.log,
            "config_snapshot": self.config_snapshot,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AnalyzeContext":
        """从字典反序列化。"""
        steps = {}
        for sid, sdata in data.get("steps", {}).items():
            steps[sid] = StepState.from_dict(sdata)

        return cls(
            session_id=data.get("session_id", ""),
            project_name=data.get("project_name", ""),
            created_at=data.get("created_at", ""),
            current_tier=data.get("current_tier", "tier1"),
            current_step=data.get("current_step", "L1_industry"),
            steps=steps,
            dste_calendar=data.get("dste_calendar", {}),
            log=data.get("log", []),
            config_snapshot=data.get("config_snapshot", {}),
        )

    # ---- 日志 ----

    def _log(self, message: str) -> None:
        """记录日志。"""
        self.log.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
        })

    def get_log(self, limit: int = 50) -> list:
        """获取最近日志。"""
        return self.log[-limit:] if self.log else []

    # ---- DSTE 日历 ----

    def get_dste_calendar(self) -> dict:
        """获取 DSTE 年度日历。"""
        if not self.dste_calendar:
            self.dste_calendar = self._build_default_calendar()
        return self.dste_calendar

    def _build_default_calendar(self) -> dict:
        """构建默认 DSTE 日历。"""
        return {
            "4": {"phase": "启动", "tasks": ["明确研究范围"], "skills": ["planning-with-files"], "outputs": ["研究计划"]},
            "5": {"phase": "五看", "tasks": ["看行业/客户/竞争"], "skills": ["sn-deep-research", "mbb-strategist"], "outputs": ["子报告"]},
            "6": {"phase": "五看", "tasks": ["看行业/客户/竞争"], "skills": ["sn-deep-research", "mbb-strategist"], "outputs": ["子报告"]},
            "7": {"phase": "五看", "tasks": ["看自己/机会"], "skills": ["mbb-strategist", "excel"], "outputs": ["子报告"]},
            "8": {"phase": "三定", "tasks": ["定目标/策略/控制点"], "skills": ["mbb-strategist"], "outputs": ["战略草案"]},
            "9": {"phase": "评审", "tasks": ["战略评审定稿"], "skills": ["mbb-strategist"], "outputs": ["L1报告"]},
            "10": {"phase": "解码", "tasks": ["CSF/KPI导出"], "skills": ["excel-analysis"], "outputs": ["CSF/KPI清单"]},
            "11": {"phase": "解码", "tasks": ["重点工作/PBC"], "skills": ["planning-with-files"], "outputs": ["L2方案"]},
            "12": {"phase": "预算", "tasks": ["预算编制审批"], "skills": ["excel-analysis"], "outputs": ["预算方案"]},
            "1": {"phase": "执行", "tasks": ["执行与监控"], "skills": ["planning-with-files"], "outputs": ["执行报告"]},
            "2": {"phase": "执行", "tasks": ["执行与监控"], "skills": ["planning-with-files"], "outputs": ["执行报告"]},
            "3": {"phase": "复盘", "tasks": ["战略复盘迭代"], "skills": ["sn-research-synthesis"], "outputs": ["复盘报告"]},
        }