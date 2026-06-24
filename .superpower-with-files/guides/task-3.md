# Task 3: Docker + Nginx 部署配置

**Files:**
- Create: `Dockerfile`
- Create: `docker-compose.yml`
- Create: `nginx/nginx.conf`

**WARNING:** 遵循 `docker-compose-python-deployment` skill 的所有pitfall规则。

## Step 1: 编写 Dockerfile

```dockerfile
FROM python:3.11-slim
# NOTE: 使用3.11-slim而非3.12-slim — 避免China VPS layer stall (pitfall #2)

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖（使用清华镜像加速）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用代码
COPY app/ ./app/

# 健康检查使用Python而非curl（pitfall #12: slim镜像无curl）
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

EXPOSE 5000

# 使用 python app.py 而非 gunicorn（触发 __main__ 初始化逻辑）
CMD ["python", "app/app.py"]
```

## Step 2: 编写 docker-compose.yml

```yaml
services:
  app:
    build: .
    container_name: strategy-framework
    restart: unless-stopped
    ports:
      - "127.0.0.1:5000:5000"  # 仅本地回环，Nginx反向代理
    env_file:
      - .env
    volumes:
      - ./app/instance:/app/app/instance  # 持久化会话数据
    healthcheck:
      test: ["CMD-SHELL", "python3 -c \"import urllib.request; urllib.request.urlopen('http://localhost:5000/')\" || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s

  nginx:
    image: nginx:alpine
    container_name: strategy-nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
```

## Step 3: 编写 Nginx 配置

```nginx
server {
    listen 80;
    server_name _;

    client_max_body_size 10m;

    location / {
        proxy_pass http://app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        proxy_pass http://app:5000;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

## Step 4: 本地Docker构建验证

```bash
docker compose build
docker compose up -d
curl -s http://localhost:5000/ | head -5
docker compose down
```

## Step 5: Commit

```bash
git add -A
git commit -m "feat: docker + nginx deployment config"
git push origin main
```
