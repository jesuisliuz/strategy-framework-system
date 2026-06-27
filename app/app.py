"""
Flask 应用入口 + 完整 API 路由

三层级数据模型贯穿全流程：
Tier1（五看三定 8 步）→ Tier2（BEM 六步法 5 步）→ Tier3（DSTE 3 步）

API 路由：
- 会话管理：/api/session/*
- 步骤操作：/api/step/*
- 技能查询：/api/skills/*
- 触发词：/api/trigger/*
- 报告生成：/api/report/*
- 导航状态：/api/nav/*
- DSTE 日历：/api/dste/*
"""

import os
from flask import Flask, jsonify, request, render_template

from .models import (
    TIER_DEFINITIONS,
    STEP_DEPENDENCIES,
    STEP_ORDER,
    ALL_STEPS,
    get_step_definition,
    get_steps_by_tier,
)
from .skill_registry import SkillRegistry
from .trigger_router import TriggerRouter, match_trigger_api
from .session import (
    create_session,
    get_session,
    save_session,
    delete_session,
    list_sessions,
    cleanup_expired_sessions,
)
from .engines import AnalysisEngine
from .reports.l1_report import generate_L1_report, check_L1_requirements
from .reports.l2_report import generate_L2_report
from .reports.l3_report import generate_L3_report

app = Flask(__name__)

# =============================================================================
# 首页
# =============================================================================

@app.route("/")
def index():
    """主页 — 三层级概览。"""
    return render_template("index.html",
                           tiers=TIER_DEFINITIONS,
                           steps=get_steps_by_tier())


# =============================================================================
# 会话管理
# =============================================================================

@app.route("/api/session/start", methods=["POST"])
def start_session():
    """创建新会话。"""
    data = request.get_json() or {}
    project_name = data.get("project_name", "未命名项目")
    config = data.get("config", {})
    ctx = create_session(project_name, config)
    return jsonify({
        "session_id": ctx.session_id,
        "project_name": ctx.project_name,
        "created_at": ctx.created_at,
    })


@app.route("/api/session/<session_id>/status")
def session_status(session_id):
    """会话状态 — 所有步骤完成情况。"""
    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404

    steps_status = {}
    for step_id in STEP_ORDER:
        step = ctx.get_step(step_id)
        if step:
            steps_status[step_id] = {
                "status": step.status,
                "created_at": step.created_at,
                "updated_at": step.updated_at,
                "error": step.error,
            }
        else:
            steps_status[step_id] = {"status": "pending"}

    ready_steps = ctx.get_ready_steps()

    return jsonify({
        "session_id": session_id,
        "project_name": ctx.project_name,
        "current_tier": ctx.current_tier,
        "current_step": ctx.current_step,
        "steps": steps_status,
        "ready_steps": ready_steps,
        "log": ctx.get_log(20),
    })


@app.route("/api/sessions/list")
def sessions_list():
    """列出最近会话。"""
    limit = request.args.get("limit", 20, type=int)
    return jsonify({"sessions": list_sessions(limit)})


@app.route("/api/session/<session_id>", methods=["DELETE"])
def delete_session_api(session_id):
    """删除会话。"""
    if delete_session(session_id):
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Session not found"}), 404


@app.route("/api/session/cleanup")
def session_cleanup():
    """清理过期会话。"""
    cleaned = cleanup_expired_sessions()
    return jsonify({"cleaned": cleaned})


# =============================================================================
# 步骤操作
# =============================================================================

@app.route("/api/step/<step_id>")
def get_step(step_id):
    """获取步骤数据（定义+输入+输出）。"""
    session_id = request.args.get("session_id")
    step_def = get_step_definition(step_id)

    result = {
        "step_id": step_id,
        "definition": step_def,
    }

    if session_id:
        ctx = get_session(session_id)
        if ctx:
            step = ctx.get_step(step_id)
            if step:
                result["state"] = {
                    "status": step.status,
                    "input": step.input,
                    "output": step.output,
                    "created_at": step.created_at,
                    "updated_at": step.updated_at,
                    "error": step.error,
                }

    return jsonify(result)


@app.route("/api/step/<step_id>/save", methods=["POST"])
def save_step_input(step_id):
    """保存输入 + 执行分析。"""
    data = request.get_json() or {}
    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id required"}), 400

    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404

    # 1. 保存输入
    fields = data.get("fields", {})
    ctx.set_step_input(step_id, fields)

    # 2. 标记下游为 stale（跨层级级联）
    invalidated = ctx.invalidate_downstream(step_id)

    # 3. 执行分析
    ctx.set_step_status(step_id, "running")
    save_session(ctx)

    try:
        # 构建 skill_interface（模拟）
        skill_interface = _build_skill_interface(ctx, session_id)

        # 执行分析
        result = AnalysisEngine.analyze(step_id, ctx, skill_interface)

        # 4. 保存输出
        ctx.set_step_output(step_id, result)
        ctx.current_step = step_id
        save_session(ctx)

        return jsonify({
            "status": "done",
            "step_id": step_id,
            "output": result,
            "invalidated": invalidated,
        })
    except Exception as e:
        ctx.set_step_status(step_id, "error", error=str(e))
        save_session(ctx)
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/api/step/<step_id>/recalculate", methods=["POST"])
def recalculate_step(step_id):
    """单体重算。"""
    data = request.get_json() or {}
    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id required"}), 400

    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404

    # 标记为 stale 然后重新执行
    step = ctx.get_step(step_id)
    if step:
        step.status = "stale"
        save_session(ctx)

    return save_step_input(step_id)


@app.route("/api/cascade/recalculate", methods=["POST"])
def cascade_recalculate():
    """级联重算（从指定步骤起）。"""
    data = request.get_json() or {}
    session_id = data.get("session_id")
    from_step = data.get("from_step")
    if not session_id or not from_step:
        return jsonify({"error": "session_id and from_step required"}), 400

    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404

    # 标记下游为 stale
    invalidated = ctx.invalidate_downstream(from_step)
    save_session(ctx)

    return jsonify({
        "from_step": from_step,
        "invalidated": invalidated,
        "ready_steps": ctx.get_ready_steps(),
    })


# =============================================================================
# 技能查询
# =============================================================================

@app.route("/api/skills/list")
def skills_list():
    """所有技能清单。"""
    return jsonify({
        "by_category": SkillRegistry.get_all_skills_by_category(),
    })


@app.route("/api/step/<step_id>/skills")
def step_skills(step_id):
    """该步骤关联技能。"""
    skills = SkillRegistry.get_skills_for_step(step_id)
    frameworks = SkillRegistry.get_mbb_frameworks_for_step(step_id)
    subagents = SkillRegistry.get_parallel_subagents(step_id)
    reverse = SkillRegistry.get_reverse_testing_config(step_id)
    outputs = SkillRegistry.get_step_outputs(step_id)
    usage = SkillRegistry.get_step_usage(step_id)

    return jsonify({
        "step_id": step_id,
        "skills": skills,
        "mbb_frameworks": frameworks,
        "parallel_subagents": subagents,
        "reverse_testing": reverse,
        "outputs": outputs,
        "usage": usage,
    })


# =============================================================================
# 触发词
# =============================================================================

@app.route("/api/trigger/match", methods=["POST"])
def trigger_match():
    """匹配触发词。"""
    data = request.get_json() or {}
    user_input = data.get("user_input", "")
    result = match_trigger_api(user_input)
    return jsonify(result)


@app.route("/api/trigger/scenarios")
def trigger_scenarios():
    """所有场景配置。"""
    return jsonify(TriggerRouter.get_all_scenarios())


# =============================================================================
# 报告生成
# =============================================================================

@app.route("/api/report/L1")
def report_l1():
    """L1 战略洞察报告。"""
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id required"}), 400

    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404

    report = generate_L1_report(ctx.to_dict())
    quality = check_L1_requirements(report)

    return jsonify({
        "report": report,
        "quality": quality,
    })


@app.route("/api/report/L2")
def report_l2():
    """L2 战略解码方案。"""
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id required"}), 400

    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404

    report = generate_L2_report(ctx.to_dict())
    return jsonify({"report": report})


@app.route("/api/report/L3")
def report_l3():
    """L3 落地执行方案。"""
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id required"}), 400

    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404

    report = generate_L3_report(ctx.to_dict())
    return jsonify({"report": report})


@app.route("/api/report/full")
def report_full():
    """完整三份报告。"""
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id required"}), 400

    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404

    ctx_dict = ctx.to_dict()
    return jsonify({
        "L1": generate_L1_report(ctx_dict),
        "L2": generate_L2_report(ctx_dict),
        "L3": generate_L3_report(ctx_dict),
    })


# =============================================================================
# 导航状态
# =============================================================================

@app.route("/api/nav/status")
def nav_status():
    """导航条状态。"""
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"tiers": TIER_DEFINITIONS, "steps": get_steps_by_tier()})

    ctx = get_session(session_id)
    if not ctx:
        return jsonify({"error": "Session not found"}), 404

    tier_status = {}
    for tier_key, tier_def in TIER_DEFINITIONS.items():
        steps = tier_def.get("steps", [])
        done_count = sum(1 for s in steps if ctx.is_step_done(s))
        total_count = len(steps)
        tier_status[tier_key] = {
            "name": tier_def["name"],
            "done": done_count,
            "total": total_count,
            "progress": round(done_count / total_count * 100, 1) if total_count > 0 else 0,
        }

    return jsonify({
        "tiers": tier_status,
        "current_tier": ctx.current_tier,
        "current_step": ctx.current_step,
        "ready_steps": ctx.get_ready_steps(),
    })


# =============================================================================
# DSTE 日历
# =============================================================================

@app.route("/api/dste/calendar")
def dste_calendar():
    """DSTE 年度日历。"""
    session_id = request.args.get("session_id")
    if session_id:
        ctx = get_session(session_id)
        if ctx:
            return jsonify(ctx.get_dste_calendar())

    # 默认日历
    from .models import AnalyzeContext
    default_ctx = AnalyzeContext(session_id="default", project_name="默认")
    return jsonify(default_ctx.get_dste_calendar())


# =============================================================================
# 框架信息
# =============================================================================

@app.route("/api/framework/tiers")
def framework_tiers():
    """三层级定义。"""
    return jsonify(TIER_DEFINITIONS)


@app.route("/api/framework/steps")
def framework_steps():
    """所有步骤定义。"""
    return jsonify({"steps": ALL_STEPS})


@app.route("/api/framework/dependencies")
def framework_dependencies():
    """步骤依赖关系。"""
    return jsonify(STEP_DEPENDENCIES)


# =============================================================================
# Skill Interface（分析引擎调用技能）
# =============================================================================

def _build_skill_interface(ctx: AnalyzeContext, session_id: str):
    """构建 skill_interface 对象，供 AnalysisEngine 调用。

    当前为模拟实现，后续对接 Hermes delegate_task。
    """
    class SkillInterface:
        def __init__(self, ctx, session_id):
            self.ctx = ctx
            self.session_id = session_id

        def call_skill(self, skill_name, prompt, context=None):
            """调用单个技能。"""
            return {
                "content": f"[{skill_name}] 分析结果（模拟）\n\n{prompt}",
                "summary": f"{skill_name} 分析完成",
            }

        def delegate_parallel(self, prompts, agent_names, context=None):
            """并行调度多个 subagent。"""
            results = []
            for i, (prompt, name) in enumerate(zip(prompts, agent_names)):
                results.append({
                    "name": name,
                    "conclusion": f"[{name}] 独立分析结论（模拟）",
                    "confidence": "B",
                })
            return results

    return SkillInterface(ctx, session_id)