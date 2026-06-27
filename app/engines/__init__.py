"""
Analysis Engine Registry

注册所有分析引擎函数，供 AnalysisEngine 统一调度。
"""
from .tier1_five_looks import (
    analyze_L1_industry,
    analyze_L2_customer,
    analyze_L3_competition,
    analyze_L4_internal,
    analyze_L5_opportunity,
)
from .tier1_three_sets import (
    analyze_L6_objective,
    analyze_L7_strategy,
    analyze_L8_control,
)
from .tier2_bem import analyze_B1_csf, analyze_B2_kpi, analyze_B3_ctq, analyze_B4_keytasks, analyze_B5_pbc
from .tier3_dste import analyze_D1_execution, analyze_D2_analysis, analyze_D3_review

ANALYZERS = {
    # Tier1: 五看
    "L1_industry": analyze_L1_industry,
    "L2_customer": analyze_L2_customer,
    "L3_competition": analyze_L3_competition,
    "L4_internal": analyze_L4_internal,
    "L5_opportunity": analyze_L5_opportunity,
    # Tier1: 三定
    "L6_objective": analyze_L6_objective,
    "L7_strategy": analyze_L7_strategy,
    "L8_control": analyze_L8_control,
    # Tier2: BEM
    "B1_csf": analyze_B1_csf,
    "B2_kpi": analyze_B2_kpi,
    "B3_ctq": analyze_B3_ctq,
    "B4_keytasks": analyze_B4_keytasks,
    "B5_pbc": analyze_B5_pbc,
    # Tier3: DSTE
    "D1_execution": analyze_D1_execution,
    "D2_analysis": analyze_D2_analysis,
    "D3_review": analyze_D3_review,
}


class AnalysisEngine:
    """统一分析引擎入口。

    根据 step_id 路由到对应的分析函数。
    支持多 Agent 并行（通过 skill_interface.delegate_parallel）。
    """

    @staticmethod
    def analyze(step_id: str, ctx: dict, skill_interface) -> dict:
        analyzer = ANALYZERS.get(step_id)
        if not analyzer:
            return {
                "content": f"⚠️ Step {step_id} 暂无分析实现",
                "summary": f"{step_id} 未实现",
                "artifacts": [],
                "skills_used": [],
                "data": {},
            }
        step_input = ctx.get_step_input(step_id) if hasattr(ctx, "get_step_input") else ctx.get("inputs", {}).get(step_id, {})
        upstream = ctx.get("upstream", {})
        return analyzer(step_input, upstream, skill_interface)