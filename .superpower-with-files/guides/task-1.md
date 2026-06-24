# Task 1: 目录结构与配置初始化

**Files:**
- Create: `app/__init__.py`
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`

## Step 1: 创建目录结构

```bash
mkdir -p app/templates app/static/css app/static/js
touch app/__init__.py
```

## Step 2: 编写 requirements.txt

```
flask==3.1.0
gunicorn==23.0.0
python-dotenv==1.1.0
```

## Step 3: 编写 .env.example（公开模板，无真实密钥）

```
# 分析功能用LLM API密钥（部署时填入.env）
ANALYSIS_LLM_API_KEY=your_api_key_here
ANALYSIS_LLM_BASE_URL=https://api.openai.com/v1
ANALYSIS_LLM_MODEL=gpt-4o
SECRET_KEY=change-me-to-random-string
```

## Step 4: 编写 .gitignore

```
# 环境与密钥
.env
credentials/
*.pem
*.key

# Python
__pycache__/
*.pyc
.venv/
venv/

# IDE
.vscode/
.idea/

# 运行态
app/instance/
*.db
*.sqlite

# 上传
uploads/

# Superpowers
.superpower-with-files/progress.md
.superpower-with-files/handoff.md

# 系统
.DS_Store
Thumbs.db
```

## Step 5: 验证

```bash
ls -R app/
cat .gitignore | head -5
```

## Step 6: Commit

```bash
git add -A
git commit -m "feat: project skeleton — dirs, config, .gitignore"
git push origin main
```
