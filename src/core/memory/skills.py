import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class ReasoningSkill:
    """
    程序性记忆 (Procedural Memory) - 技能单元
    
    将复杂的、验证过的推理路径或 SQL 模板固化为本体中的可复用技能。
    """
    id: str
    name: str
    description: str
    logic_template: str
    success_rate: float = 1.0
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)

class SkillRegistry:
    """
    分层记忆结构 (Layered Memory) - 技能注册中心
    """
    def __init__(self, semantic_memory: Any):
        self.semantic_memory = semantic_memory
        self.skills: Dict[str, ReasoningSkill] = {}
        self._load_built_in_skills()

    def _load_built_in_skills(self):
        """加载初始内置技能"""
        self.register_skill(ReasoningSkill(
            id="skill:gas_regulator_quality_audit",
            name="调压柜质量全量审计",
            description="自动联通 GB 27791 和设备参数进行闭环合规扫描。",
            logic_template="MATCH (e:Entity {type:'Regulator'})-[:has_parameter]->(p) ..."
        ))

    def register_skill(self, skill: ReasoningSkill):
        self.skills[skill.id] = skill
        # 同时在图谱中创建 Skill 节点，实现跨 Agent 共享
        if self.semantic_memory:
            from core.reasoner import Fact
            skill_fact = Fact(
                subject=skill.id, 
                predicate="rdf:type", 
                object="owl:Skill", 
                confidence=1.0, 
                source="skill_registry"
            )
            self.semantic_memory.store_fact(skill_fact)
            logger.info(f"Skill persisted to Graph: {skill.name}")

    def get_skill(self, skill_id: str) -> Optional[ReasoningSkill]:
        return self.skills.get(skill_id)

    def list_skills(self) -> List[Dict]:
        return [
            {"id": s.id, "name": s.name, "description": s.description}
            for s in self.skills.values()
        ]
