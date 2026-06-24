# Task 28: 最终集成测试 + GitHub推送 + 隐私审计

**Files:**
- Create: `tests/test_integration.py`

## Step 1: 集成测试

测试覆盖:
- 三层级模型创建
- 19步全流程
- 技能映射正确性
- 报告生成精确匹配模板
- 质量检查通过率
- 级联重算（跨层级）
- 触发词匹配
- 4场景调用链

## Step 2: 隐私审计

```bash
grep -r "sk-" app/ || echo "OK: No API keys in code"
grep -r "ghp_" app/ || echo "OK: No GitHub tokens in code"
git log --all -- '**/.env'  # 应为空
cat .gitignore  # 确认 .env, credentials/, *.pem 在列表中
```

## Step 3: 最终提交

```bash
git add -A
git status  # 确认无敏感文件
git commit -m "release: v2.0 — 华为三板斧完整19步战略分析系统

Tier1: 五看三定(8步) → L1战略洞察报告
Tier2: BEM六步法(5步) → L2战略解码方案
Tier3: DSTE(3步) → L3落地执行方案
+ 横纵验证 + 最终报告
+ 技能映射引擎 + 触发词路由 + 4场景编排器
+ 质量检查清单 + DSTE年度日历
+ 19步完整输入字段定义
+ 精确匹配用户文档三级报告模板"

git tag v2.0.0 -m "完整版：三层级19步+技能集成+报告模板+质量检查+DSTE日历"

git push origin main --tags
```

## Step 4: GitHub验证

- 访问 https://github.com/jesuisliuz/strategy-framework-system
- 确认所有文件存在
- 确认无敏感文件
- README 完整

## Step 5: 记录部署信息

VPS: 117.50.157.11 / /opt/strategy-framework
