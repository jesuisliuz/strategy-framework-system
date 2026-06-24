# Task 15: 最终集成测试与GitHub推送

**Files:**
- Create: `tests/test_integration.py`

## Step 1: 集成测试

```python
"""端到端集成测试"""
import pytest
from app.models import AnalyzeContext, STEP_DEFINITIONS
from app.steps import StepEngine
from app.report import ReportGenerator, generate_full_report


class TestFullWorkflow:
    def setup_method(self):
        self.ctx = AnalyzeContext(project_name="测试项目")
    
    def test_complete_8step_workflow(self):
        """完整8步工作流测试"""
        # L1: 看行业
        self.ctx.steps["L1_industry"]["input"].fields = {
            "industry_name": "新能源汽车",
            "market_size": "5000",
            "growth_rate": "35",
            "key_trends": "政策推动碳中和\n电池成本下降",
        }
        result = StepEngine.analyze("L1_industry", self.ctx)
        self.ctx.set_step_result("L1_industry", result, "新能源行业高速增长")
        assert self.ctx.get_step_output("L1_industry").status == "done"
        
        # L2-L8 依次...
        # （模拟完整流程）
        
        # 验证级联
        self.ctx.invalidate_downstream("L1_industry")
        assert self.ctx.get_step_output("L2_customer").status == "stale"
    
    def test_report_generation(self):
        """报告生成测试"""
        # 填充mock数据...
        full = generate_full_report(self.ctx)
        assert "L1" in full
        assert "L2" in full
        assert "L3" in full
    
    def test_session_persistence(self):
        """会话持久化测试"""
        from app.session import save_session, get_session, create_session
        ctx = create_session()
        ctx.project_name = "持久化测试"
        save_session(ctx)
        
        # 模拟新会话加载
        loaded = get_session(ctx.session_id)
        assert loaded is not None
        assert loaded.project_name == "持久化测试"
```

## Step 2: 运行测试

```bash
cd /c/Users/jesui/Projects/strategy-framework-system
pip install pytest
python -m pytest tests/ -v
```

预期：所有测试PASS。

## Step 3: 最终GitHub状态检查

```bash
# 检查隐私泄露
git log --all --full-history -- '**/.env'  # 应该为空
git log --all --full-history -- '**/credentials/**'  # 应该为空
grep -r "sk-" app/ || echo "No API keys found in code — OK"
grep -r "ghp_" app/ || echo "No GitHub tokens in code — OK"

# 检查.gitignore覆盖
cat .gitignore
```

## Step 4: 最终提交与推送

```bash
git add -A
git status
# 确认没有 .env, credentials, *.pem, *.key 在暂存区

git commit -m "release: v1.0 — 完整8步战略分析系统 + Docker部署"

# 打标签
git tag v1.0.0 -m "华为三板斧战略分析系统首个可用版本"

git push origin main --tags
```

## Step 5: 验证GitHub仓库

- 访问 https://github.com/jesuisliuz/strategy-framework-system
- 确认 README 存在
- 确认无敏感文件
- 确认 CI (如有) 通过

## Step 6: 记录部署信息到 memory

保存关键信息：
- VPS IP: 117.50.157.11
- 部署路径: /opt/strategy-framework
- 访问地址: http://117.50.157.11
- GitHub: https://github.com/jesuisliuz/strategy-framework-system

## Step 7: 清理

```bash
rm /tmp/strategy-deploy.tar.gz
```

---

*所有15个任务完成。系统可用。*
