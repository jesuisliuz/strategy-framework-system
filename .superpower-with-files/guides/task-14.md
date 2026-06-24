# Task 14: VPS环境准备与Docker部署

**Files:**
- Modify: `docker-compose.yml` （增加生产环境配置）

**WARNING:** 严格遵循 `docker-compose-python-deployment` skill的所有规则。目标VPS：117.50.157.11 (Debian 12, 4GB RAM)

## Step 1: VPS环境检查

通过SSH连接，验证：
```bash
ssh -i ~/.ssh/xinnet-vps root@117.50.157.11 "
    echo '=== OS ===' && cat /etc/os-release | head -3
    echo '=== Docker ===' && docker --version && docker compose version
    echo '=== Disk ===' && df -h /
    echo '=== RAM ===' && free -h
    echo '=== DNS ===' && python3 -c 'import socket; socket.getaddrinfo(\"pypi.tuna.tsinghua.edu.cn\", 443)' 2>&1 | head -1
"
```

## Step 2: 上传项目文件

使用 rsync 或 scp（排除 .git 和 .superpower-with-files）：
```bash
# 打包
cd /c/Users/jesui/Projects/strategy-framework-system
tar --exclude='.git' --exclude='.superpower-with-files' --exclude='__pycache__' \
    -czf /tmp/strategy-deploy.tar.gz .

# 上传
scp -i ~/.ssh/xinnet-vps /tmp/strategy-deploy.tar.gz root@117.50.157.11:/opt/

# VPS上解压
ssh -i ~/.ssh/xinnet-vps root@117.50.157.11 "
    mkdir -p /opt/strategy-framework && cd /opt/strategy-framework
    tar xzf /opt/strategy-deploy.tar.gz
    ls -la
"
```

## Step 3: 配置 .env（在VPS上创建）

```bash
ssh -i ~/.ssh/xinnet-vps root@117.50.157.11 "
cd /opt/strategy-framework
cat > .env << 'ENVEOF'
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
ANALYSIS_LLM_API_KEY=your_real_key_here
ANALYSIS_LLM_BASE_URL=https://api.openai.com/v1
ANALYSIS_LLM_MODEL=gpt-4o
ENVEOF
chmod 600 .env
"
```

## Step 4: Docker构建与启动

在VPS上：
```bash
ssh -i ~/.ssh/xinnet-vps root@117.50.157.11 "
cd /opt/strategy-framework
# 配置Docker镜像加速器（中国VPS必需）
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << 'EOF'
{
  \"registry-mirrors\": [
    \"https://mirror.ccs.tencentyun.com\",
    \"https://docker.m.daocloud.io\"
  ]
}
EOF
systemctl restart docker

# 构建（使用清华PyPI镜像加速pip）
docker compose build --build-arg PIP_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple

# 启动
docker compose up -d

# 等待就绪
sleep 5
docker compose ps
"
```

## Step 5: 验证部署

```bash
# 本地验证VPS上的服务
curl -s http://117.50.157.11/ | grep "战略分析工作台"
# 预期输出包含"战略分析工作台"
```

## Step 6: Pitfall检查清单

- [ ] 使用 `python:3.11-slim` 而非 3.12-slim（pitfall #2）
- [ ] 使用 `python app/app.py` 而非 gunicorn（确保 init 逻辑执行）
- [ ] 健康检查用 Python 而非 curl（pitfall #12）
- [ ] Docker daemon.json 配置了国内镜像加速
- [ ] pip 使用清华镜像
- [ ] `.env` 未提交到Git
- [ ] 只监听 127.0.0.1:5000，通过Nginx暴露

## Step 7: 无Git操作（部署不需要Git）

部署文件通过 scp 传输，VPS上不做 git clone（避免暴露GitHub凭据）。源码版本管理通过本地推送GitHub完成。

---

*注意：此步骤需要真实API密钥。部署前确保 `.env` 中的 `ANALYSIS_LLM_API_KEY` 已配置。*
