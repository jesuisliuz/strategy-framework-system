# Findings — 华为三板斧战略分析系统

## 框架结构确认（从前序对话恢复）

### 8步工作流 + 最终报告

| 步骤ID | 名称 | 方法论 | 输入字段数 | 产出 |
|--------|------|--------|-----------|------|
| L1_industry | 看行业/趋势 | 五看 | 6 | PEST、波特五力、技术趋势 |
| L2_customer | 看客户 | 五看 | 4 | 客户细分、$APPEALS、需求分析 |
| L3_competition | 看竞争 | 五看 | 4 | 竞对地图、份额分析、战略集团图 |
| L4_internal | 看自己 | 五看 | 3 | 资源盘点、能力评估、根因分析 |
| L5_opportunity | 看机会 | 五看 | 4 | SPAN矩阵、机会优先级排序 |
| L6_objective | 定目标 | 三定 | 4 | BSC目标体系、差距分析 |
| L7_strategy | 定策略 | 三定 | 4 | 业务设计、创新焦点、关键任务 |
| L8_control | 定控制点 | 三定 | 3 | 护城河设计、风险预案 |
| final_report | 最终报告 | DSTE+BEM | 自动聚合 | L1战略洞察/L2战略解码/L3落地执行 |

### 技能映射（分析时调用）

| 阶段 | 可用技能 | 用途 |
|------|---------|------|
| L1-L5 | mbb-strategist, sn-deep-research | 结构化行业/竞品分析 |
| L3 | mbb-strategist (Porter's, SWOT) | 竞争定位 |
| L6-L8 | mbb-strategist (Financial, Risk) | 目标体系与风险 |
| 全部 | sn-da-excel-workflow | 数据可视化（如输入Excel数据） |

### 技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 后端框架 | Flask | 轻量、SSR、单容器部署 |
| 前端交互 | htmx | SPA-like体验、无构建工具 |
| 配色 | Deep Blue + Amber Gold | ToB SaaS成熟风格 |
| 部署 | Docker Compose + Nginx | 单机部署、版本可控 |
| VPS | 新网 117.50.157.11 | Debian 12 / 4GB / 60G |
| 版本管理 | GitHub 公开仓库 | 方便分享、CI/社区 |

### Pitfalls 已知

- GitHub clone 从本机超时 → 使用 Python urllib + PAT API 创建仓库
- 中国VPS Docker构建慢 → 用 python:3.11-slim + 清华PyPI镜像
- 隐私保护 → .env不入库、.gitignore严格、部署用scp非git clone

---

*Last Updated: 2026-06-24 14:46 UTC*
