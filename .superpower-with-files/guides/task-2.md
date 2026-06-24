# Task 2: Flask应用入口与前端框架

**Files:**
- Create: `app/app.py`
- Create: `app/templates/base.html`
- Create: `app/templates/index.html`
- Create: `app/static/css/main.css`
- Create: `app/static/js/app.js`

## Step 1: 编写 app.py（最小可运行Flask）

```python
import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-in-production")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

## Step 2: 编写 base.html（ToB SaaS基础布局）

- CSS Variables: Deep Blue (#1a2332) 主背景, Amber Gold (#d4a853) 强调色
- 引入 htmx CDN: `<script src="https://unpkg.com/htmx.org@2.0.4"></script>`
- 引入 marked.js: `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>`

## Step 3: 编写 main.css

完整CSS变量系统（见Task 2原Guide）

## Step 4: 编写 index.html（主页-三层级概览卡片）

显示三个层级卡片：Tier1五看三定 / Tier2 BEM / Tier3 DSTE，每个卡片下展示子步骤数

## Step 5: Commit

```bash
git add -A && git commit -m "feat: flask entry + ToB theme + index page"
```
