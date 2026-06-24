# Findings — 华为三板斧战略分析系统 v2.0

## 框架结构 (对应用户"框架全景图"文档)

### 三层级模型 (Tier1 → Tier2 → Tier3)

| 层级 | 名称 | 阶段 | 时间 | 步数 | 核心技能 | 输出 |
|------|------|------|------|------|---------|------|
| Tier1 | 五看三定 | 战略洞察+制定 | 4-9月(7个月) | 8步 | sn-deep-research + mbb-strategist + sn-search系列 | L1 战略洞察报告 (10k-30k字) |
| Tier2 | BEM | 战略解码 | 10-12月(3个月) | 5步 | Excel分析系列 + planning-with-files | L2 战略解码方案 (5k-10k字) |
| Tier3 | DSTE | 全流程管理 | 全年循环 | 3步 | planning-with-files + Excel分析系列 | L3 落地执行方案 (2k-5k字) |

### 19步骤完整清单

**Tier1: 五看三定 (8步)**
- L1_industry: 看行业/趋势 → mbb-strategist(Industry Trends, PESTEL) + sn-deep-research + sn-search-academic
- L2_customer: 看客户 → mbb-strategist(Customer Journey, Personas) + sn-deep-research + sn-search-social
- L3_competition: 看竞争 → mbb-strategist(SWOT, Porter's Five Forces) + sn-deep-research + sn-search-code
- L4_internal: 看自己 → mbb-strategist(SWOT) + excel-data-analysis
- L5_opportunity: 看机会 → mbb-strategist(Risk & Scenario) + excel-bar-chart-visualization(SPAN矩阵)
- L6_objective: 定目标 → mbb-strategist(Executive Synthesis)
- L7_strategy: 定策略 → mbb-strategist(GTM Strategy, Pricing Strategy)
- L8_control: 定控制点 → mbb-strategist(SWOT, Porter's)

**Tier2: BEM六步法 (5步)**
- B1_csf: CSF导出 → mbb-strategist(Executive Synthesis)
- B2_kpi: KPI导出 → excel-data-analysis + excel-threshold-analysis-and-styling
- B3_ctq: CTQ-Y导出 → excel-outlier-detection-and-quality-assessment
- B4_keytasks: 重点工作分解 → planning-with-files(task_plan.md)
- B5_pbc: PBC签订 → excel-data-analysis(PBC模板设计)

**Tier3: DSTE (3步)**
- D1_execution: SP/BP执行监控 → planning-with-files(progress.md) + excel-line-chart-visualization
- D2_analysis: 经营分析会 → excel-trend-analysis + statistical-distribution-and-outlier-analysis
- D3_review: 战略复盘 → sn-research-synthesis

**验证与收口**
- cross_validation: 横纵分析法 (横向行业对齐+纵向时间推演)
- final_report: 最终报告聚合

### 技能映射表 (对应用户"技能嵌入映射表")

```
L1_industry → [mbb-strategist(Industry Trends,PESTEL), sn-deep-research, sn-search-academic]
L2_customer → [mbb-strategist(Customer Journey,Personas), sn-deep-research, sn-search-social-cn/en]
L3_competition → [mbb-strategist(SWOT,Porter's), sn-deep-research, sn-search-code]
L4_internal → [mbb-strategist(SWOT), excel-data-analysis]
L5_opportunity → [mbb-strategist(Risk&Scenario), excel-bar-chart-visualization]
L6_objective → [mbb-strategist(Executive Synthesis)]
L7_strategy → [mbb-strategist(GTM Strategy,Pricing)]
L8_control → [mbb-strategist(SWOT,Porter's)]
B1_csf → [mbb-strategist(Executive Synthesis)]
B2_kpi → [excel-data-analysis, excel-threshold-analysis-and-styling]
B3_ctq → [excel-outlier-detection-and-quality-assessment]
B4_keytasks → [planning-with-files]
B5_pbc → [excel-data-analysis]
D1_execution → [planning-with-files, excel-line-chart-visualization]
D2_analysis → [excel-trend-analysis, statistical-distribution-and-outlier-analysis]
D3_review → [sn-research-synthesis]
cross_validation → [sn-research-synthesis, mbb-strategist]
```

### 技能优先级 (对应用户"技能调用优先级")

1. **第一优先级**: sn-deep-research — 触发: 深度研究/行业研究/竞品分析
2. **第二优先级**: mbb-strategist — 触发: 战略分析/SWOT/PESTEL/波特五力
3. **第三优先级**: Excel分析系列 — 触发: 数据分析/KPI设计/可视化
4. **第四优先级**: planning-with-files — 触发: 多步骤任务/进度跟踪

### 触发词映射 (对应用户"使用指南")

| 场景 | 触发词 | 调用技能 |
|------|--------|---------|
| 战略洞察 | "做战略洞察"/"五看分析"/"看行业"/"看客户"/"看竞争" | sn-deep-research + mbb-strategist |
| 战略解码 | "做战略解码"/"BEM解码"/"设计KPI"/"分解重点工作" | excel-analysis + planning-with-files |
| 执行监控 | "跟踪执行进度"/"经营分析"/"战略复盘" | planning-with-files + excel-analysis |
| 竞品分析 | "竞品分析"/"竞争格局" | mbb-strategist + sn-search-code |
| 行业研究 | "行业研究"/"深度研究" | sn-deep-research |

### 报告模板精确要求

**L1 战略洞察报告**: 8章 (执行摘要/看行业/看客户/看竞争/看自己/看机会/三定/数据来源)
**L2 战略解码方案**: 7章 (战略回顾/CSF导出/KPI体系/CTQ-Y/重点工作/PBC/附件)
**L3 落地执行方案**: 4章 (执行计划/监控机制/复盘机制/附件)

### 质量检查清单

**L1**: 覆盖五看三定全部模块 ✓ / 使用mbb-strategist至少2个框架 ✓ / sn-deep-research深度取证 ✓ / 数据支撑 ✓ / 10k-30k字 ✓ / 行动建议 ✓
**L2**: CSF战略目标映射 ✓ / KPI SMART化 ✓ / 重点工作分解到责任人 ✓ / PBC模板 ✓ / 5k-10k字 ✓
**L3**: 季度/月度行动计划 ✓ / 监控机制 ✓ / 复盘机制 ✓ / 2k-5k字 ✓

### DSTE年度日历

| 月份 | 阶段 | 任务 | 技能 | 产出 |
|------|------|------|------|------|
| 4月 | 启动 | 明确研究范围 | planning-with-files | 研究计划 |
| 5-6月 | 五看 | 看行业/客户/竞争 | sn-deep-research + mbb-strategist | 子报告 |
| 7月 | 五看 | 看自己/机会 | mbb-strategist + excel | 子报告 |
| 8月 | 三定 | 定目标/策略/控制点 | mbb-strategist | 战略草案 |
| 9月 | 评审 | 战略评审定稿 | mbb-strategist(Executive Synthesis) | L1报告 |
| 10月 | 解码 | CSF/KPI导出 | excel-analysis | CSF/KPI清单 |
| 11月 | 解码 | 重点工作/PBC | planning-with-files | L2方案 |
| 12月 | 预算 | 预算编制审批 | excel-analysis | 预算方案 |
| 1-3月 | 执行 | 执行与监控 | planning-with-files(progress.md) | 执行报告 |
| 4月(次年) | 复盘 | 战略复盘迭代 | sn-research-synthesis | 复盘报告 |

### 技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 后端框架 | Flask | 轻量、SSR、单容器部署 |
| 前端交互 | htmx | SPA-like、无构建工具 |
| 配色 | Deep Blue + Amber Gold | ToB SaaS成熟风格 |
| 部署 | Docker Compose + Nginx | 单机部署 |
| VPS | 新网 117.50.157.11 | Debian 12 / 4GB / 60G |
| 版本管理 | GitHub 公开仓库 | jesuisliuz/strategy-framework-system |

---

*Last Updated: 2026-06-24 15:01 UTC*
