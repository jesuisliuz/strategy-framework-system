"""
SkillRegistry — 技能注册表与映射引擎

核心设计：
- 完整技能清单（SKILL_INVENTORY）
- 步骤→技能映射（STEP_SKILL_MAP）
- 多 Agent 并行支持（inspired by claude-code-best-practice Superpowers workflow）
  - 五看步骤支持 parallel_subagents 配置，每个 subagent 独立搜索+独立结论
  - 通过 skill_interface.delegate_parallel 实现批量并行
"""

# =============================================================================
# 1. 技能清单
# =============================================================================

SKILL_INVENTORY = {
    # === 战略框架 ===
    "mbb-strategist": {
        "category": "战略框架",
        "capabilities": [
            "SWOT", "PESTEL", "Porter's Five Forces", "Value Chain",
            "Blue Ocean", "GTM Strategy", "Pricing Strategy", "Risk & Scenario",
            "Financial Modeling", "Executive Synthesis", "Industry Trends",
            "Customer Journey", "Personas",
        ],
        "priority": 2,
    },
    # === 深度研究 ===
    "sn-deep-research": {
        "category": "深度研究",
        "capabilities": ["规划→取证→综合→成稿全流程编排"],
        "sub_skills": [
            "sn-research-planning",
            "sn-dimension-research",
            "sn-research-synthesis",
            "sn-research-report",
            "sn-report-format-discovery",
        ],
        "priority": 1,
    },
    # === 搜索系列 ===
    "sn-search-academic": {
        "category": "研究子技能",
        "capabilities": ["ArXiv", "Semantic Scholar", "PubMed"],
        "priority": 1,
    },
    "sn-search-code": {
        "category": "研究子技能",
        "capabilities": ["GitHub", "Stack Overflow"],
        "priority": 1,
    },
    "sn-search-social-cn": {
        "category": "研究子技能",
        "capabilities": ["B站", "知乎", "抖音"],
        "priority": 1,
    },
    "sn-search-social-en": {
        "category": "研究子技能",
        "capabilities": ["Reddit", "Twitter", "YouTube"],
        "priority": 1,
    },
    # === 文件规划 ===
    "planning-with-files": {
        "category": "文件规划",
        "capabilities": ["task_plan.md", "findings.md", "progress.md"],
        "priority": 4,
    },
    # === Excel分析系列 ===
    "excel-data-analysis": {
        "category": "Excel分析",
        "capabilities": ["数据清洗", "分类统计", "条件过滤", "KPI体系设计"],
        "priority": 3,
    },
    "excel-bar-chart-visualization": {
        "category": "Excel分析",
        "capabilities": ["柱状图"],
        "priority": 3,
    },
    "excel-line-chart-visualization": {
        "category": "Excel分析",
        "capabilities": ["折线图"],
        "priority": 3,
    },
    "excel-pie-chart-data-analysis": {
        "category": "Excel分析",
        "capabilities": ["饼图"],
        "priority": 3,
    },
    "pivot-table-cross-analysis": {
        "category": "Excel分析",
        "capabilities": ["透视表"],
        "priority": 3,
    },
    "trend-analysis": {
        "category": "Excel分析",
        "capabilities": ["趋势分析"],
        "priority": 3,
    },
    "outlier-detection-and-quality-assessment": {
        "category": "Excel分析",
        "capabilities": ["异常值检测"],
        "priority": 3,
    },
    "statistical-distribution-and-outlier-analysis": {
        "category": "Excel分析",
        "capabilities": ["统计分布"],
        "priority": 3,
    },
    "time-series-and-categorical-analysis": {
        "category": "Excel分析",
        "capabilities": ["时间序列"],
        "priority": 3,
    },
    # === 综合 ===
    "sn-research-synthesis": {
        "category": "综合判断",
        "capabilities": ["多源综合", "主线判断", "证据评估"],
        "priority": 1,
    },
}

# =============================================================================
# 2. 步骤→技能映射
# =============================================================================

STEP_SKILL_MAP = {
    # Tier1: 五看三定
    "L1_industry": {
        "skills": ["mbb-strategist", "sn-deep-research", "sn-search-academic"],
        "mbb_frameworks": ["Industry Trends", "PESTEL"],
        "usage": (
            "用MBB的Industry Trends框架分析行业趋势；"
            "用sn-deep-research做深度行业研究；"
            "用sn-search-academic搜索学术论文验证趋势"
        ),
        "outputs": ["行业趋势报告", "价值转移分析图"],
        # --- 多 Agent 并行配置 (claude-code-best-practice 模式) ---
        "parallel_subagents": [
            {
                "name": "宏观趋势",
                "role": "分析宏观经济、政策、技术演进对行业的影响",
                "skills": ["mbb-strategist", "sn-search-academic"],
                "mbb_frameworks": ["PESTEL"],
            },
            {
                "name": "市场数据",
                "role": "分析市场规模、增长率、细分赛道、价值链转移",
                "skills": ["mbb-strategist", "sn-deep-research"],
                "mbb_frameworks": ["Industry Trends"],
            },
            {
                "name": "技术演进",
                "role": "分析关键技术趋势、专利布局、技术替代风险",
                "skills": ["sn-search-academic", "sn-search-code"],
                "mbb_frameworks": [],
            },
        ],
    },
    "L2_customer": {
        "skills": ["mbb-strategist", "sn-deep-research", "sn-search-social-cn", "sn-search-social-en"],
        "mbb_frameworks": ["Customer Journey", "Personas"],
        "usage": (
            "用MBB的Customer Journey分析客户购买行为；"
            "用Personas做用户画像；"
            "用sn-search-social搜索用户口碑"
        ),
        "outputs": ["客户细分报告", "市场交易地图"],
        "parallel_subagents": [
            {
                "name": "用户画像",
                "role": "构建核心用户Persona，分析需求、痛点、决策路径",
                "skills": ["mbb-strategist", "sn-search-social-cn"],
                "mbb_frameworks": ["Personas"],
            },
            {
                "name": "客户旅程",
                "role": "分析客户从认知到购买的完整旅程，识别关键触点",
                "skills": ["mbb-strategist", "sn-deep-research"],
                "mbb_frameworks": ["Customer Journey"],
            },
            {
                "name": "口碑分析",
                "role": "搜索社交媒体、论坛、评测中的用户真实反馈",
                "skills": ["sn-search-social-cn", "sn-search-social-en"],
                "mbb_frameworks": [],
            },
        ],
    },
    "L3_competition": {
        "skills": ["mbb-strategist", "sn-deep-research", "sn-search-code"],
        "mbb_frameworks": ["SWOT", "Porter's Five Forces"],
        "usage": (
            "用SWOT分析自身与竞品；"
            "用Porter's Five Forces分析竞争格局；"
            "用sn-search-code搜索竞品技术信息"
        ),
        "outputs": ["竞争格局报告", "竞品对比矩阵"],
        # --- 多视角冲突模式 (ai-berkshire 模式) ---
        "parallel_subagents": [
            {
                "name": "进攻方视角",
                "role": "扮演新进入者，寻找现有竞争者的薄弱环节和可攻击点",
                "skills": ["mbb-strategist", "sn-deep-research"],
                "mbb_frameworks": ["Porter's Five Forces"],
                "perspective": "aggressive",
            },
            {
                "name": "防守方视角",
                "role": "扮演现有头部企业，评估护城河深度和防御能力",
                "skills": ["mbb-strategist", "sn-search-code"],
                "mbb_frameworks": ["SWOT"],
                "perspective": "defensive",
            },
            {
                "name": "中立观察者",
                "role": "客观评估竞争格局，不受立场影响，聚焦数据和事实",
                "skills": ["sn-deep-research", "sn-search-code"],
                "mbb_frameworks": ["Porter's Five Forces", "SWOT"],
                "perspective": "neutral",
            },
        ],
    },
    "L4_internal": {
        "skills": ["mbb-strategist", "excel-data-analysis"],
        "mbb_frameworks": ["SWOT"],
        "usage": "用SWOT分析自身优势劣势；用Excel分析内部运营数据",
        "outputs": ["能力评估报告"],
    },
    "L5_opportunity": {
        "skills": ["mbb-strategist", "excel-bar-chart-visualization"],
        "mbb_frameworks": ["Risk & Scenario"],
        "usage": "用Risk & Scenario分析机会风险；用Excel绘制SPAN矩阵",
        "outputs": ["SPAN机会矩阵"],
    },
    # Tier1: 三定
    "L6_objective": {
        "skills": ["mbb-strategist"],
        "mbb_frameworks": ["Executive Synthesis"],
        "usage": "用Executive Synthesis提炼战略目标",
        "outputs": ["战略目标清单"],
    },
    "L7_strategy": {
        "skills": ["mbb-strategist"],
        "mbb_frameworks": ["GTM Strategy", "Pricing Strategy"],
        "usage": "用GTM设计市场进入策略；用Pricing Strategy设计定价策略",
        "outputs": ["策略路线图"],
    },
    "L8_control": {
        "skills": ["mbb-strategist"],
        "mbb_frameworks": ["SWOT", "Porter's"],
        "usage": "用SWOT和Porter's分析护城河",
        "outputs": ["战略控制点清单"],
    },
    # Tier2: BEM六步法
    "B1_csf": {
        "skills": ["mbb-strategist"],
        "mbb_frameworks": ["Executive Synthesis"],
        "usage": "用Executive Synthesis提炼CSF",
        "outputs": ["CSF清单"],
    },
    "B2_kpi": {
        "skills": ["excel-data-analysis", "excel-threshold-analysis-and-styling"],
        "usage": "用Excel设计KPI体系；用阈值分析设定KPI目标值",
        "outputs": ["KPI体系表"],
    },
    "B3_ctq": {
        "skills": ["excel-outlier-detection-and-quality-assessment"],
        "usage": "用异常值检测识别关键品质点",
        "outputs": ["CTQ-Y清单"],
    },
    "B4_keytasks": {
        "skills": ["planning-with-files"],
        "usage": "用文件化规划分解重点工作",
        "outputs": ["重点工作分解表"],
    },
    "B5_pbc": {
        "skills": ["excel-data-analysis"],
        "usage": "用Excel设计PBC模板",
        "outputs": ["PBC模板"],
    },
    # Tier3: DSTE
    "D1_execution": {
        "skills": ["planning-with-files", "excel-line-chart-visualization"],
        "usage": "用文件化规划跟踪进度；用折线图可视化进度",
        "outputs": ["执行进度报告"],
    },
    "D2_analysis": {
        "skills": ["excel-trend-analysis", "statistical-distribution-and-outlier-analysis"],
        "usage": "用趋势分析识别偏差；用异常检测发现异常",
        "outputs": ["偏差分析报告"],
    },
    "D3_review": {
        "skills": ["sn-research-synthesis"],
        "usage": "用综合判断提炼复盘结论",
        "outputs": ["战略复盘报告"],
        # --- 逆向测试模式 (ai-berkshire 芒格式) ---
        "reverse_testing": {
            "enabled": True,
            "prompt_template": (
                "用芒格式逆向思维分析：我们的战略有哪 5 种死法？"
                "对每种死法评估概率（高/中/低）和触发条件。"
                "然后给出对应的预防措施。"
            ),
        },
    },
    # 验证
    "cross_validation": {
        "skills": ["sn-research-synthesis", "mbb-strategist"],
        "usage": "横向行业对齐+纵向时间推演验证",
        "outputs": ["验证报告"],
    },
}

# =============================================================================
# 3. SkillRegistry 类
# =============================================================================


class SkillRegistry:
    """技能注册表：查询、映射、并行调度。"""

    @staticmethod
    def get_skills_for_step(step_id: str) -> list:
        """获取步骤需要的技能列表。"""
        step_config = STEP_SKILL_MAP.get(step_id, {})
        return step_config.get("skills", [])

    @staticmethod
    def get_mbb_frameworks_for_step(step_id: str) -> list:
        """获取步骤需要的 MBB 框架。"""
        step_config = STEP_SKILL_MAP.get(step_id, {})
        return step_config.get("mbb_frameworks", [])

    @staticmethod
    def get_priority(skill_name: str) -> int:
        """获取技能调用优先级（数字越小优先级越高）。"""
        skill_info = SKILL_INVENTORY.get(skill_name, {})
        return skill_info.get("priority", 99)

    @staticmethod
    def get_all_skills_by_category() -> dict:
        """按类别分组获取所有技能——用于前端可视化。"""
        categories = {}
        for name, info in SKILL_INVENTORY.items():
            cat = info.get("category", "其他")
            categories.setdefault(cat, []).append({
                "name": name,
                "capabilities": info.get("capabilities", []),
                "priority": info.get("priority", 99),
            })
        return categories

    @staticmethod
    def get_parallel_subagents(step_id: str) -> list:
        """获取步骤的多 Agent 并行配置。

        返回每个 subagent 的配置字典，包含 name, role, skills, mbb_frameworks, perspective。
        如果步骤没有并行配置，返回空列表。
        """
        step_config = STEP_SKILL_MAP.get(step_id, {})
        return step_config.get("parallel_subagents", [])

    @staticmethod
    def get_reverse_testing_config(step_id: str) -> dict:
        """获取步骤的逆向测试配置（ai-berkshire 芒格式）。

        如果步骤启用了逆向测试，返回配置字典；否则返回空字典。
        """
        step_config = STEP_SKILL_MAP.get(step_id, {})
        return step_config.get("reverse_testing", {})

    @staticmethod
    def get_step_outputs(step_id: str) -> list:
        """获取步骤的预期输出物。"""
        step_config = STEP_SKILL_MAP.get(step_id, {})
        return step_config.get("outputs", [])

    @staticmethod
    def get_step_usage(step_id: str) -> str:
        """获取步骤的使用说明。"""
        step_config = STEP_SKILL_MAP.get(step_id, {})
        return step_config.get("usage", "")

    @staticmethod
    def get_all_steps() -> list:
        """获取所有步骤 ID 列表。"""
        return list(STEP_SKILL_MAP.keys())

    @staticmethod
    def get_steps_by_tier() -> dict:
        """按层级分组获取所有步骤。"""
        return {
            "Tier1_五看": ["L1_industry", "L2_customer", "L3_competition", "L4_internal", "L5_opportunity"],
            "Tier1_三定": ["L6_objective", "L7_strategy", "L8_control"],
            "Tier2_BEM": ["B1_csf", "B2_kpi", "B3_ctq", "B4_keytasks", "B5_pbc"],
            "Tier3_DSTE": ["D1_execution", "D2_analysis", "D3_review"],
            "验证": ["cross_validation"],
        }