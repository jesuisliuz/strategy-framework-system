# 华为三板斧战略分析技能整合框架 — 实施计划

## 架构决策汇总

| 维度 | 决策 | 说明 |
|------|------|------|
| LLM API | 可配置，支持一键部署 MiniMax / SiliconFlow / DeepSeek | 不同API配不同prompt模板（上下文长度、指令遵循差异） |
| 数据持久化 | SQLite | 存step结构化输出，支持跨session恢复 |
| 测试 | 单元测试 + 集成测试 + UAT | UAT作为独立验收环节 |
| 报告输出 | 先HTML + MD，PDF/PPT后续追加 | 页面可展示优先 |
| **后台配置** | **Web配置面板 + 环境变量存储** | 用户可自助录入API信息，存到.env或config.json，全局调用 |
| **PDF导出** | **暂缓开发，技术规划先行** | 评估typst / weasyprint / pdfkit方案，后续Phase追加 |

---

## 工作分解

### Phase 0: 后台配置管理 (Priority: P0)

**目标**: 提供一个Web配置面板，让用户自助录入API信息，存储到环境变量，供各功能模块调用。

#### 0.1 配置文件设计
- 方案A: `.env` 文件（推荐，兼容所有LLM SDK）
- 方案B: `config.json` + `.env.example` 模板
- 决策: 使用 `.env` + `config.json` 双文件
  - `.env`: 存储敏感API密钥（不提交到git）
  - `config.json`: 存储非敏感配置（模型选择、prompt模板等）

#### 0.2 配置数据结构
```json
{
  "llm": {
    "provider": "minimax",
    "models": {
      "minimax": "abab-7",
      "siliconflow": "deepseek-ai/DeepSeek-V3",
      "deepseek": "deepseek-chat"
    },
    "prompt_templates": {
      "minimax": "templates/minimax_prompt.md",
      "siliconflow": "templates/siliconflow_prompt.md",
      "deepseek": "templates/deepseek_prompt.md"
    }
  },
  "research": {
    "max_depth": 3,
    "parallel_dimensions": 2,
    "report_format": "html"
  }
}
```

#### 0.3 环境变量设计
```bash
# .env
MINIMAX_API_KEY=xxx
MINIMAX_BASE_URL=https://api.minimax.chat/v1

SILICONFLOW_API_KEY=xxx
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1

DEEPSEEK_API_KEY=xxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

#### 0.4 Web配置面板功能
- [ ] API密钥录入表单（MiniMax / SiliconFlow / DeepSeek）
- [ ] 模型选择下拉框
- [ ] Prompt模板预览/编辑
- [ ] 测试连接按钮（验证API密钥有效性）
- [ ] 保存/加载配置按钮
- [ ] 配置状态指示器（已配置/未配置/连接失败）

#### 0.5 配置加载模块
- [ ] `config_loader.py`: 读取 `.env` + `config.json`
- [ ] `config_manager.py`: 提供 `get_api_key(provider)`, `get_model(provider)`, `get_prompt_template(provider)` 接口
- [ ] 环境变量优先级：`.env` > `config.json` > 默认值
- [ ] 配置热更新（无需重启服务）

#### 0.6 安全考虑
- [ ] API密钥加密存储（可选：使用 `cryptography` 库）
- [ ] `.env` 加入 `.gitignore`
- [ ] 配置页面需要简单认证（可选：HTTP Basic Auth 或 Token）

---

### Phase 1: 核心架构 (Priority: P0)

#### 1.1 SQLite 数据层 — `data/storage/`
- 定义 `steps` 表：`id`, `session_id`, `step_name`, `input`, `output`, `created_at`, `updated_at`
- 定义 `sessions` 表：`id`, `topic`, `status`, `config_snapshot`, `created_at`
- 定义 `reports` 表：`id`, `session_id`, `report_type`, `report_path`, `created_at`
- 实现 `StorageManager` 类：CRUD操作、断点续跑支持

#### 1.2 LLM 调用层 — `core/llm/`
- 抽象 `LLMProvider` 接口：`generate(prompt, model, temperature)`
- 实现 `MiniMaxProvider`, `SiliconFlowProvider`, `DeepSeekProvider`
- 统一错误处理：重试、超时、速率限制
- Prompt模板管理：按provider加载不同模板

#### 1.3 研究编排层 — `orchestrator/`
- 实现 `ResearchOrchestrator` 类
- 阶段管理：初始化 → 规划 → 取证 → 综合 → 成稿
- 断点续跑：从 `steps` 表恢复未完成阶段
- 进度追踪：实时更新 `sessions` 表状态

#### 1.4 报告生成层 — `reporter/`
- HTML报告生成：`HTMLReporter`
- Markdown报告生成：`MarkdownReporter`
- 报告模板：`templates/report.html`, `templates/report.md`
- 导出功能：下载/分享

---

### Phase 2: 技能集成 (Priority: P1)

#### 2.1 mbb-strategist 集成
- 加载五看三定框架
- BEM（业务卓越管理）流程适配
- DSTE（从战略到执行）流程适配

#### 2.2 sn-deep-research 集成
- 复用规划、取证、综合、成稿模块
- 适配华为三板斧框架

#### 2.3 Excel 技能集成
- 数据导入：读取Excel数据作为研究素材
- 数据分析：调用现有Excel分析技能
- 结果导出：将研究结果写入Excel

---

### Phase 3: 测试与UAT (Priority: P2)

#### 3.1 单元测试
- `tests/unit/test_config_loader.py`
- `tests/unit/test_llm_providers.py`
- `tests/unit/test_storage_manager.py`

#### 3.2 集成测试
- `tests/integration/test_research_orchestrator.py`
- `tests/integration/test_end_to_end.py`

#### 3.3 UAT
- 用户验收测试场景
- 性能测试（大模型、长上下文）
- 安全测试（API密钥泄露防护）

#### 3.4 PDF导出技术规划（暂缓开发）
| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| Typst | 原生支持Markdown转PDF，排版精美 | 需安装编译环境 | ⭐⭐⭐⭐ |
| WeasyPrint | CSS驱动，与HTML报告无缝衔接 | 依赖puppeteer/chromium | ⭐⭐⭐ |
| pdfkit (wkhtmltopdf) | 成熟稳定 | 渲染引擎较老 | ⭐⭐ |

**决策**: 优先评估 Typst 方案（与现有md2pdf技能复用），后续Phase 5追加实现。

---

### Phase 4: 文档与部署 (Priority: P3)

#### 4.1 用户文档
- `README.md`: 快速开始
- `docs/configuration.md`: 配置指南
- `docs/api.md`: API参考

#### 4.2 部署脚本
- `docker-compose.yml`: 一键部署
- `scripts/setup.sh`: 环境初始化
- `.env.example`: 配置模板

---

## 目录结构

```
huawei-three-axes/
├── config.json              # 非敏感配置
├── .env                     # API密钥（gitignore）
├── .env.example             # 配置模板
├── requirements.txt         # Python依赖
├── main.py                  # 入口文件
├── core/
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py          # LLMProvider接口
│   │   ├── minimax.py
│   │   ├── siliconflow.py
│   │   └── deepseek.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── sqlite.py        # SQLite实现
│   │   └── models.py        # SQLAlchemy模型
│   └── config/
│       ├── __init__.py
│       ├── loader.py        # 配置加载
│       └── manager.py       # 配置管理
├── orchestrator/
│   ├── __init__.py
│   ├── research.py          # 研究编排
│   └── phases/              # 各阶段实现
│       ├── init.py
│       ├── planning.py
│       ├── research.py
│       ├── synthesis.py
│       └── report.py
├── reporter/
│   ├── __init__.py
│   ├── html.py
│   └── markdown.py
├── templates/
│   ├── report.html
│   ├── report.md
│   └── prompt/
│       ├── minimax_prompt.md
│       ├── siliconflow_prompt.md
│       └── deepseek_prompt.md
├── web/
│   ├── app.py               # Flask/FastAPI Web服务
│   ├── routes/
│   │   ├── config.py        # 配置管理API
│   │   ├── research.py      # 研究任务API
│   │   └── report.py        # 报告API
│   └── static/
│       ├── css/
│       └── js/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── data/
│   └── storage.db           # SQLite数据库
├── reports/                 # 生成报告输出
└── docs/
```

---

## 执行顺序

1. **Phase 0**: 后台配置管理（先做，因为其他模块依赖配置）
2. **Phase 1**: 核心架构（LLM + SQLite + 编排）
3. **Phase 2**: 技能集成（mbb-strategist + sn-deep-research + Excel）
4. **Phase 3**: 测试与UAT
5. **Phase 4**: PDF导出技术规划（暂缓实现）
5. **Phase 5**: 文档与部署
6. **Phase 6**: PDF导出功能实现（后续）

---

## 关键依赖

| 模块 | 依赖 | 说明 |
|------|------|------|
| LLM调用 | `openai` / `httpx` | 统一API调用 |
| SQLite | `sqlalchemy` | ORM支持 |
| Web面板 | `fastapi` + `uvicorn` + `jinja2` | 快速开发 |
| 配置管理 | `python-dotenv` | .env文件解析 |
| 加密存储 | `cryptography` | 可选，API密钥加密 |

---

## 验收标准

- [ ] 用户可通过Web面板录入API密钥
- [ ] API密钥存储到 `.env` 文件，不提交到git
- [ ] 配置页面可测试API连接
- [ ] 研究任务可自动加载配置并使用对应LLM
- [ ] 支持断点续跑（SQLite存储进度）
- [ ] 生成HTML + Markdown报告
- [ ] 单元测试覆盖率 > 80%
- [ ] UAT通过全部验收场景
- [ ] PDF导出技术选型报告完成（暂缓实现）

---

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| API密钥泄露 | 高 | `.env` 加入 `.gitignore`，可选加密存储 |
| LLM API不可用 | 中 | 多provider支持，自动切换 |
| 长上下文超出限制 | 中 | Prompt模板优化，分段处理 |
| 用户配置错误 | 低 | 配置验证 + 测试连接功能 |
| PDF导出方案未定 | 低 | 已做技术规划，后续Phase评估选型 |

---

*最后更新: 2026-06-24 (终版) — 已确认: LLM API可配置管理页面 / SQLite持久化 / PDF暂缓(技术规划) / 单元测试+集成测试+UAT*