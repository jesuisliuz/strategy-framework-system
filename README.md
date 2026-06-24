# 华为三板斧战略分析系统

> ⚔️ 基于华为五看三定+BEM+DSTE方法论的ToB SaaS战略分析工作台

[![Deploy](https://img.shields.io/badge/deploy-Docker-blue)](https://github.com/jesuisliuz/strategy-framework-system)
[![Stack](https://img.shields.io/badge/stack-Flask%20%2B%20htmx-orange)](https://github.com/jesuisliuz/strategy-framework-system)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 概览

将华为三十年战略管理方法论（五看三定、BEM战略解码、DSTE端到端流程）构建为可交互的Web分析系统。通过8个步骤引导用户完成从行业洞察到落地执行的全流程战略分析。

### 工作流

```
看行业 → 看客户 → 看竞争 → 看自己 → 看机会 → 定目标 → 定策略 → 定控制点 → 📊最终报告
  L1       L2       L3       L4       L5       L6       L7       L8       三级报告
└────────────────── 五看 ──────────────────┘ └────────── 三定 ──────────┘ └ DSTE+BEM ┘
```

### 报告输出

- **L1 战略洞察报告** (10k-30k字): 五看综合分析
- **L2 战略解码报告** (5k-10k字): BEM解码→CSF→KPI→CTQ
- **L3 落地执行报告** (2k-5k字): DSTE年度日历+资源预算

## 快速开始

```bash
# 克隆
git clone https://github.com/jesuisliuz/strategy-framework-system.git
cd strategy-framework-system

# 配置
cp .env.example .env
# 编辑 .env 填入 ANALYSIS_LLM_API_KEY

# Docker部署
docker compose up -d

# 访问 http://localhost
```

## 项目结构

```
strategy-framework-system/
├── app/
│   ├── app.py              # Flask 入口
│   ├── models.py           # AnalyzeContext 数据模型 + 步骤定义
│   ├── steps.py            # 步骤分析引擎
│   ├── report.py           # L1/L2/L3 报告生成器
│   ├── session.py          # 会话管理
│   ├── templates/          # Jinja2 模板
│   │   ├── base.html       # ToB布局基础模板
│   │   ├── index.html      # 主页（步骤概览卡片）
│   │   ├── step.html       # 单步骤工作页
│   │   └── report.html     # 最终报告页面
│   └── static/
│       ├── css/main.css    # Deep Blue + Amber Gold 主题
│       └── js/app.js       # htmx 交互
├── nginx/
│   └── nginx.conf          # 反向代理配置
├── docker-compose.yml
├── Dockerfile
├── .env.example            # 环境变量模板（公开）
└── .gitignore
```

## 隐私说明

- ✅ `.env` 已加入 `.gitignore`，不会被提交
- ✅ 所有API密钥通过环境变量注入容器
- ✅ 仓库公开但无敏感信息

## 许可

MIT License
