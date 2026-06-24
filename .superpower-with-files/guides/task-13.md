# Task 13: 统一技能调用接口

> **对应文档**: 二、商业分析技能全景 + 三、技能嵌入映射表

**Files:**
- Create: `app/skill_interface.py`

## Step 1: 技能调用接口定义

```python
class SkillInterface:
    """统一技能调用接口——封装所有Hermes技能的调用逻辑"""
    
    SKILL_CATEGORIES = {
        "战略框架": ["mbb-strategist"],
        "深度研究": ["sn-deep-research", "sn-research-planning", "sn-dimension-research",
                    "sn-research-synthesis", "sn-research-report", "sn-report-format-discovery"],
        "搜索": ["sn-search-academic", "sn-search-code", "sn-search-social-cn", "sn-search-social-en"],
        "文件规划": ["planning-with-files"],
        "Excel分析": ["excel-data-analysis", "sn-da-excel-workflow", "sn-da-large-file-analysis",
                     "excel-bar-chart-visualization", "excel-line-chart-visualization",
                     "excel-pie-chart-data-analysis", "pivot-table-cross-analysis",
                     "trend-analysis", "outlier-detection-and-quality-assessment",
                     "statistical-distribution-and-outlier-analysis",
                     "time-series-and-categorical-analysis",
                     # 及其他30+ Excel子技能
        ],
    }
    
    @staticmethod
    def get_skill_info(skill_name: str) -> dict:
        """获取技能详细信息"""
        
    @staticmethod
    def get_step_skills(step_id: str) -> dict:
        """获取步骤所需的技能映射（含框架和用法说明）"""
        return STEP_SKILL_MAP.get(step_id, {})
    
    @staticmethod
    def build_analysis_prompt(step_id: str, fields: dict, upstream: dict) -> str:
        """构建包含技能调用指令的分析Prompt"""
        mapping = STEP_SKILL_MAP.get(step_id, {})
        skills = mapping.get("skills", [])
        frameworks = mapping.get("mbb_frameworks", [])
        usage = mapping.get("usage", "")
        
        system_prompt = SkillInterface._get_system_prompt(step_id, skills)
        user_prompt = f"""## 分析任务
{usage}

## 输入数据
{SkillInterface._format_fields(fields)}

## 上游上下文
{SkillInterface._format_upstream(upstream)}

## 技能指令
请依次调用以下技能完成分析：
{SkillInterface._format_skill_chain(step_id)}
"""
        return system_prompt, user_prompt
    
    @staticmethod
    def _get_system_prompt(step_id: str, skills: list) -> str:
        """为每个步骤构建专属system prompt"""
        # 根据技能映射构建角色和指令
        
    @staticmethod
    def _format_skill_chain(step_id: str) -> str:
        """格式化技能调用链"""
        # 从4个场景调用流程中推导
```

## Step 2: 技能调用链生成

```python
@staticmethod
def get_call_chain(step_id: str) -> list:
    """获取步骤的技能调用链（有序）"""
    # 例如 L1_industry:
    # 1. sn-deep-research (初始化研究)
    # 2. sn-research-planning (生成plan.json)
    # 3. sn-dimension-research (行业维度取证)
    #    → sn-search-academic (学术论文)
    #    → sn-search-social-cn/en (用户口碑)
    # 4. mbb-strategist(Industry Trends, PESTEL)
    # 5. sn-research-synthesis (综合判断)
    # 6. sn-research-report (生成子报告)
```

## Step 3: Commit

```bash
git add -A && git commit -m "feat: unified skill interface + call chain generation for all 19 steps"
```
