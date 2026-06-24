# Task 27: VPS环境准备与Docker部署

**WARNING:** 严格遵循 `docker-compose-python-deployment` skill pitfall规则。目标: 117.50.157.11

## Step 1: VPS环境检查

```bash
ssh root@117.50.157.11 "docker --version && docker compose version && free -h && df -h /"
```

## Step 2: 上传项目 (scp exclude .git)

```bash
tar --exclude='.git' --exclude='__pycache__' -czf /tmp/strategy-deploy.tar.gz .
scp /tmp/strategy-deploy.tar.gz root@117.50.157.11:/opt/
ssh root@117.50.157.11 "mkdir -p /opt/strategy-framework && cd /opt/strategy-framework && tar xzf /opt/strategy-deploy.tar.gz"
```

## Step 3: 配置.env (VPS上)

```bash
ssh root@117.50.157.11 "cd /opt/strategy-framework && cat > .env << 'EOF'
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
ANALYSIS_LLM_API_KEY=your_real_key_here
EOF
chmod 600 .env"
```

## Step 4: Docker构建+启动

```bash
ssh root@117.50.157.11 "cd /opt/strategy-framework && docker compose build && docker compose up -d"
```

## Step 5: 验证

```bash
curl -s http://117.50.157.11/ | grep "战略分析工作台"
```

## Pitfall检查清单
- [ ] python:3.11-slim (非3.12)
- [ ] 健康检查用Python非curl
- [ ] 国内镜像加速
- [ ] .env未入Git

## Step 6: 无Git操作

部署通过scp传输，VPS不做git clone。源码版本管理由本地GitHub推送完成。
