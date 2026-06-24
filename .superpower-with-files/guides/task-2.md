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

- 使用CSS Variables定义配色：Deep Blue (#1a2332) 主背景, Amber Gold (#d4a853) 强调色
- 标准ToB布局：顶部导航 + 主内容区
- 引入 htmx CDN: `<script src="https://unpkg.com/htmx.org@2.0.4"></script>`

## Step 3: 编写 index.html（主页——步骤概览卡片）

- 继承 base.html
- 展示8步卡片网格，每张卡片显示步骤名称、方法、状态
- 点击进入对应步骤

## Step 4: 编写 main.css

定义完整的CSS变量系统：
```css
:root {
  --bg-primary: #1a2332;
  --bg-secondary: #243447;
  --bg-card: #2d4052;
  --text-primary: #e8edf2;
  --text-secondary: #a0b4c8;
  --accent: #d4a853;
  --accent-hover: #e6c06b;
  --border: #3a5068;
  --success: #4caf50;
  --danger: #ef5350;
  --radius: 8px;
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
}
```

## Step 5: 编写 app.js（htmx事件处理）

- 步骤导航高亮
- 表单提交与结果刷新
- 级联重算进度提示

## Step 6: 本地启动验证

```bash
cd /c/Users/jesui/Projects/strategy-framework-system
pip install -r requirements.txt
python app/app.py
# 访问 http://localhost:5000
```

## Step 7: Commit

```bash
git add -A
git commit -m "feat: flask entry point + ToB base layout with theme"
git push origin main
```
