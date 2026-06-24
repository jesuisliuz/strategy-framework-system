# 华为三板斧战略分析系统

> ⚔️ 基于华为五看三定+BEM+DSTE方法论的ToB SaaS战略分析工作台

[![Deploy](https://img.shields.io/badge/deploy-Docker-blue)](https://github.com/jesuisliuz/strategy-framework-system)
[![Stack](https://img.shields.io/badge/stack-Flask%20%2B%20htmx-orange)](https://github.com/jesuisliuz/strategy-framework-system)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 概览

将华为三十年战略管理方法论构建为可交互的Web分析系统。三层级19步全流程：从行业洞察到战略制定，从战略解码到落地执行，覆盖DSTE端到端年度循环。

### 三层级架构

```
┌─────────────────────────────────────────────────────────────┐
│  Tier1: 五看三定 (战略洞察+制定)    4-9月, 8步              │
│  看行业→看客户→看竞争→看自己→看机会→定目标→定策略→定控制点      │
│  核心技能: sn-deep-research + mbb-strategist                │
│  输出: L1 战略洞察报告 (10k-30k字)                           │
├─────────────────────────────────────────────────────────────┤
│  Tier2: BEM六步法 (战略解码)        10-12月, 5步             │
│  CSF导出→KPI导出→CTQ-Y导出→重点工作分解→PBC签订               │
│  核心技能: Excel分析系列 + planning-with-files               │
│  输出: L2 战略解码方案 (5k-10k字)                             │
├─────────────────────────────────────────────────────────────┤
│  Tier3: DSTE (全流程管理)           全年循环, 3步             │
│  SP/BP执行监控→经营分析会→战略复盘                             │
│  核心技能: planning-with-files + Excel分析系列               │
│  输出: L3 落地执行方案 (2k-5k字)                              │
└─────────────────────────────────────────────────────────────┘
         + 横纵验证 + 最终报告聚合
```

### 每步骤嵌入技能

每个分析步骤精确嵌入对应的商业分析技能：

| 步骤 | 嵌入技能 | MBB框架 |
|------|---------|---------|
| 看行业 | sn-deep-research, sn-search-academic | Industry Trends, PESTEL |
| 看客户 | sn-deep-research, sn-search-social | Customer Journey, Personas |
| 看竞争 | sn-deep-research, sn-search-code | SWOT, Porter's Five Forces |
| 看自己 | excel-data-analysis | SWOT |
| 看机会 | excel-bar-chart-visualization | Risk & Scenario |
| 定目标 | mbb-strategist | Executive Synthesis |
| 定策略 | mbb-strategist | GTM Strategy, Pricing Strategy |
| 定控制点 | mbb-strategist | SWOT, Porter's |
| CSF导出 | mbb-strategist | Executive Synthesis |
| KPI导出 | excel-analysis, threshold-analysis | — |
| CTQ-Y导出 | outlier-detection | — |
| 重点工作 | planning-with-files | — |
| PBC签订 | excel-data-analysis | — |
| 执行监控 | planning-with-files, line-chart | — |
| 经营分析 | trend-analysis, outlier-analysis | — |
| 战略复盘 | sn-research-synthesis | — |

### 功能特性

- **场景化向导**: 行业研究/竞品分析/KPI设计/执行跟踪 4场景快速入口
- **触发词路由**: 输入"做战略洞察"/"竞品分析"等自动匹配入口步骤
- **技能优先级**: P1 sn-deep-research → P2 mbb-strategist → P3 Excel → P4 planning
- **级联重算**: 修改上游步骤自动标记下游stale，一键跨层级重算
- **质量检查**: L1/L2/L3 三级报告自动质量检查清单
- **DSTE日历**: 4月→9月→12月→次年3月→4月 年度循环视图
- **Markdown报告**: 三级报告精确匹配文档模板，支持导出

## 快速开始

```bash
git clone https://github.com/jesuisliuz/strategy-framework-system.git
cd strategy-framework-system
cp .env.example .env
# 编辑 .env 填入 ANALYSIS_LLM_API_KEY
docker compose up -d
# 访问 http://localhost
```

## 项目结构

```
strategy-framework-system/
├── app/
│   ├── app.py                  # Flask 入口 + 全部API路由
│   ├── models.py               # 三层级数据模型 + 19步定义
│   ├── skill_registry.py       # 技能注册表 + 步骤→技能映射
│   ├── trigger_router.py       # 触发词引擎 + 优先级路由
│   ├── skill_interface.py      # 统一技能调用接口
│   ├── quality_check.py        # L1/L2/L3 质量检查清单
│   ├── scenario_orchestrator.py # 4场景技能调用编排器
│   ├── session.py              # 会话管理
│   ├── engines/
│   │   ├── tier1_five_looks.py # 五看分析 (L1-L5)
│   │   ├── tier1_three_sets.py # 三定分析 (L6-L8)
│   │   ├── tier2_bem.py        # BEM六步法 (B1-B5)
│   │   ├── tier3_dste.py       # DSTE三层 (D1-D3)
│   │   └── cross_validation.py # 横纵验证
│   ├── reports/
│   │   ├── l1_report.py        # L1 战略洞察报告 (8章模板)
│   │   ├── l2_report.py        # L2 战略解码方案 (7章模板)
│   │   └── l3_report.py        # L3 落地执行方案 (4章模板)
│   ├── data/
│   │   └── step_definitions.json # 19步完整定义
│   ├── templates/
│   │   ├── base.html           # ToB布局基础模板
│   │   ├── index.html          # 主页 (三层级概览卡片)
│   │   ├── step.html           # 单步骤工作页 (输入+输出)
│   │   ├── report.html         # 三级报告页面 (标签切换)
│   │   ├── guide.html          # 使用指南 (触发词+优先级+技能清单)
│   │   ├── dste_calendar.html  # DSTE年度日历视图
│   │   └── _*.html             # 组件片段
│   └── static/
│       ├── css/main.css        # Deep Blue + Amber Gold 主题
│       └── js/app.js           # htmx 交互
├── .superpower-with-files/
│   ├── active_tdd_plan.md      # 28任务实施计划
│   ├── findings.md             # 框架设计决策记录
│   └── guides/task-*.md        # 28个详细实施指南
├── nginx/nginx.conf
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── .gitignore
```

## 实施计划

详见 [`.superpower-with-files/active_tdd_plan.md`](.superpower-with-files/active_tdd_plan.md) — 28个任务，7个Phase。

设计决策见 [`.superpower-with-files/findings.md`](.superpower-with-files/findings.md)。

## 隐私说明

- `.env` 已加入 `.gitignore`，不会被提交
- 所有API密钥通过环境变量注入容器
- 仓库公开但无敏感信息

## 许可

MIT License
