# Task 9: 五看阶段分析逻辑 (L1-L5)

**Files:**
- Modify: `app/steps.py` → 实现真实分析逻辑

## Step 1: 替换 mock — 构建分析Prompt模板

每个五看步骤有专属的system prompt和user prompt模板：

```python
ANALYSIS_PROMPTS = {
    "L1_industry": {
        "system": "你是华为战略部资深行业分析师，精通PEST分析、波特五力模型和技术趋势研判。",
        "template": """请对【{industry_name}】行业进行战略洞察分析。

## 输入信息
- 市场规模: {market_size}亿元
- 年增长率: {growth_rate}%
- TAM: {tam}
- 关键趋势驱动因素:
{key_trends}
- 技术趋势:
{technology_trends}
- 补充背景: {additional_context}
{upstream_context}

## 分析要求
请按以下结构输出分析（Markdown格式）：

### 一、宏观环境分析 (PEST)
- **政治/政策**: 
- **经济**: 
- **社会**: 
- **技术**: 

### 二、市场格局分析 (波特五力)
- **现有竞争者强度**: 
- **新进入者威胁**: 
- **替代品威胁**: 
- **供应商议价能力**: 
- **买家议价能力**: 

### 三、技术趋势研判
- 关键技术方向
- 技术成熟度评估
- 技术对竞争格局的影响

### 四、关键发现与战略启示
- 3-5个核心洞察
- 对该行业参与者的战略建议""",
    },
    "L2_customer": {
        "system": "你是华为战略部客户洞察专家，精通$APPEALS需求分析模型和客户细分方法论。",
        "template": """...L2模板..."""
    },
    # ... L3, L4, L5 类似
}
```

## Step 2: 实现 StepEngine.analyze()

```python
class StepEngine:
    @staticmethod
    def analyze(step_id: str, ctx: AnalyzeContext) -> str:
        step_def = STEP_DEFINITIONS[step_id]
        fields = ctx.get_step_input(step_id).fields
        upstream = StepEngine._gather_upstream(step_id, ctx)
        
        prompt_config = ANALYSIS_PROMPTS.get(step_id)
        if not prompt_config:
            return f"## {step_def['name']}\n\n*该步骤的分析模板尚未定义。*"
        
        # 构建完整prompt
        prompt = prompt_config["template"].format(
            **fields,
            upstream_context=StepEngine._format_upstream(upstream)
        )
        
        # 调用LLM（目前用mock；Phase 4接入真实API）
        result = StepEngine._call_llm(
            system=prompt_config["system"],
            user=prompt
        )
        
        return result
    
    @staticmethod
    def _call_llm(system: str, user: str) -> str:
        """LLM调用——当前mock，后续接入真实API"""
        import os
        api_key = os.getenv("ANALYSIS_LLM_API_KEY")
        if not api_key:
            return _get_fallback_analysis(system, user)
        
        # TODO: 真实API调用
        # import openai
        # client = openai.OpenAI(api_key=api_key, base_url=os.getenv("ANALYSIS_LLM_BASE_URL"))
        # response = client.chat.completions.create(...)
        
        return _get_fallback_analysis(system, user)
```

## Step 3: 实现上游数据收集

```python
@staticmethod
def _gather_upstream(step_id: str, ctx: AnalyzeContext) -> dict:
    """收集所有上游步骤的输出摘要"""
    step_order = ["L1_industry", "L2_customer", "L3_competition",
                  "L4_internal", "L5_opportunity", "L6_objective",
                  "L7_strategy", "L8_control"]
    upstream = {}
    for sid in step_order:
        if sid == step_id:
            break
        out = ctx.get_step_output(sid)
        if out.status in ("done", "stale"):
            upstream[sid] = {
                "name": STEP_DEFINITIONS[sid]["name"],
                "summary": out.summary,
                "key_data": out.data
            }
    return upstream
```

## Step 4: 为每个五看步骤添加fallback分析模板

当LLM不可用时，根据输入字段生成结构化的占位分析，明确标注"基于输入数据自动生成，待LLM深化"。

## Step 5: 验证

```python
# test_steps.py
from app.models import AnalyzeContext, STEP_DEFINITIONS
from app.steps import StepEngine

ctx = AnalyzeContext()
ctx.steps["L1_industry"]["input"].fields = {
    "industry_name": "新能源汽车",
    "market_size": "5000",
    "growth_rate": "35",
    "key_trends": "政策推动\n技术进步\n消费者认知提升",
}
result = StepEngine.analyze("L1_industry", ctx)
assert "新能源汽车" in result
assert "PEST" in result or "宏观" in result or "波特" in result
print("PASS")
```

## Step 6: Commit

```bash
git add -A
git commit -m "feat: five-looks (L1-L5) analysis prompts + upstream gathering"
git push origin main
```
