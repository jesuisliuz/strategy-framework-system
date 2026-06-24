# Task 3: Docker + Nginx 部署配置

**Files:**
- Create: `Dockerfile`
- Create: `docker-compose.yml`
- Create: `nginx/nginx.conf`

**WARNING:** 严格遵循 `docker-compose-python-deployment` skill pitfall规则。

## Step 1: Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY app/ ./app/
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1
EXPOSE 5000
CMD ["python", "app/app.py"]
```

## Step 2: docker-compose.yml

```yaml
services:
  app:
    build: .
    container_name: strategy-framework
    restart: unless-stopped
    ports:
      - "127.0.0.1:5000:5000"
    env_file:
      - .env
    volumes:
      - ./app/instance:/app/app/instance
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

## Step 3: nginx.conf (反向代理)\n(见Task 3原Guide)

## Step 4: Commit

```bash
git add -A && git commit -m "feat: docker + nginx deployment config"
```
