# 华为三板斧战略分析系统 — 实施计划 (v2.0)

> **For Claude/Hermes:** REQUIRED SUB-SKILL: Use superpowers:spf-exec-plan to implement this plan task-by-task.
> **complexity:** complex

**Goal:** 构建ToB SaaS风格Web应用，完整嵌入华为三板斧三层级战略体系（五看三定→BEM→DSTE），19步骤全流程工作流。每步调用对应技能（mbb-strategist / sn-deep-research / Excel分析 / planning-with-files），按文档定义的技能映射表执行分析，输出精确匹配模板的三级报告，含DSTE年度日历、质量检查清单、场景化向导。Docker部署到阿里云VPS。

**Architecture:** Flask SSR + Jinja2 + htmx + 纯CSS/JS。三层级数据模型贯穿全流程：Tier1（五看三定8步）→Tier2（BEM六步法5步）→Tier3（DSTE 3步）。SkillRegistry管理技能注册与调用映射，TriggerRouter处理触发词→技能优先级路由，CascadeEngine处理上游修改的级联重算。AnalyticsContext持久化所有状态。

**Tech Stack:** Python 3.11, Flask, Jinja2, htmx, CSS Variables (Deep Blue + Amber Gold), Docker Compose, Nginx

---

## Phase 1: 项目骨架与开发环境

### Task 1: 目录结构与配置初始化
**Depends on:** None
**Parallel with:** None
**Guide:** See guides/task-1.md

### Task 2: Flask应用入口与前端框架
**Depends on:** Task 1
**Parallel with:** Task 3
**Guide:** See guides/task-2.md

### Task 3: Docker + Nginx 部署配置
**Depends on:** Task 1
**Parallel with:** Task 2
**Guide:** See guides/task-3.md

---

## Phase 2: 三层级数据模型与技能映射

### Task 4: 三层级数据模型 (Tier1五看三定 + Tier2 BEM + Tier3 DSTE)
**Depends on:** Task 2
**Parallel with:** None
**Guide:** See guides/task-4.md

### Task 5: 技能注册表与映射引擎 (SkillRegistry)
**Depends on:** Task 4
**Parallel with:** None
**Guide:** See guides/task-5.md

### Task 6: 19步完整定义 (8五看三定 + 6 BEM + 3 DSTE + 横纵验证 + 最终报告)
**Depends on:** Task 4, Task 5
**Parallel with:** None
**Guide:** See guides/task-6.md

### Task 7: 触发词引擎与优先级路由 (TriggerRouter)
**Depends on:** Task 5
**Parallel with:** None
**Guide:** See guides/task-7.md

### Task 8: 会话管理与API路由
**Depends on:** Task 4, Task 6
**Parallel with:** None
**Guide:** See guides/task-8.md

---

## Phase 3: 前端UI — ToB三层级工作流界面

### Task 9: 基础布局与三层级导航条 + DSTE日历视图
**Depends on:** Task 2
**Parallel with:** None
**Guide:** See guides/task-9.md

### Task 10: 左侧输入面板（19步动态表单，含文件上传）
**Depends on:** Task 6, Task 9
**Parallel with:** None
**Guide:** See guides/task-10.md

### Task 11: 中间输出面板与级联进度指示
**Depends on:** Task 10
**Parallel with:** None
**Guide:** See guides/task-11.md

### Task 12: 场景化向导页面（4场景快速入口）
**Depends on:** Task 9
**Parallel with:** None
**Guide:** See guides/task-12.md

---

## Phase 4: 技能集成分析引擎

### Task 13: 统一技能调用接口 (call_skill / 技能清单定义)
**Depends on:** Task 5
**Parallel with:** None
**Guide:** See guides/task-13.md

### Task 14: 五看分析引擎 (L1-L5) — 看行业/看客户/看竞争/看自己/看机会
**Depends on:** Task 13, Task 6
**Parallel with:** None
**Guide:** See guides/task-14.md

### Task 15: 三定分析引擎 (L6-L8) — 定目标/定策略/定控制点
**Depends on:** Task 14
**Parallel with:** None
**Guide:** See guides/task-15.md

### Task 16: BEM六步法引擎 — CSF→KPI→CTQ→重点工作→PBC
**Depends on:** Task 15
**Parallel with:** None
**Guide:** See guides/task-16.md

### Task 17: DSTE三层引擎 — SP/BP执行监控 + 经营分析会 + 战略复盘
**Depends on:** Task 16
**Parallel with:** None
**Guide:** See guides/task-17.md

### Task 18: 横纵分析法 + 级联重算引擎
**Depends on:** Task 17
**Parallel with:** None
**Guide:** See guides/task-18.md

---

## Phase 5: 三级报告生成 (精确匹配文档模板)

### Task 19: L1 战略洞察报告生成器（8章，10k-30k字）
**Depends on:** Task 14, Task 15
**Parallel with:** None
**Guide:** See guides/task-19.md

### Task 20: L2 战略解码方案生成器（7章，5k-10k字，含BEM结构）
**Depends on:** Task 16
**Parallel with:** None
**Guide:** See guides/task-20.md

### Task 21: L3 落地执行方案生成器（4章，2k-5k字，含DSTE结构）
**Depends on:** Task 17
**Parallel with:** None
**Guide:** See guides/task-21.md

### Task 22: 三级报告最终展示页面（标签切换 + Markdown渲染 + 导出）
**Depends on:** Task 19, Task 20, Task 21, Task 11
**Parallel with:** None
**Guide:** See guides/task-22.md

### Task 23: 质量检查清单验证模块
**Depends on:** Task 19, Task 20, Task 21
**Parallel with:** None
**Guide:** See guides/task-23.md

---

## Phase 6: DSTE年度日历 + 场景化技能调用

### Task 24: DSTE年度日历视图（月度时间线 + 技能任务）
**Depends on:** Task 9, Task 6
**Parallel with:** None
**Guide:** See guides/task-24.md

### Task 25: 4场景技能调用编排器
**Depends on:** Task 13, Task 7
**Parallel with:** None
**Guide:** See guides/task-25.md

### Task 26: 使用指南页面（触发词 + 优先级 + 技能清单可视化）
**Depends on:** Task 7, Task 5
**Parallel with:** None
**Guide:** See guides/task-26.md

---

## Phase 7: 部署上线

### Task 27: VPS环境准备与Docker部署
**Depends on:** Task 3, Task 22
**Parallel with:** None
**Guide:** See guides/task-27.md

### Task 28: 最终集成测试 + GitHub推送 + 隐私审计
**Depends on:** Task 27
**Parallel with:** None
**Guide:** See guides/task-28.md

---

*Last Updated: 2026-06-24 15:00 UTC*
