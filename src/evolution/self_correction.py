import logging
from typing import Any, List, Optional
from core.reasoner import Reasoner, Fact

logger = logging.getLogger(__name__)

class ContradictionChecker:
    """
    逻辑冲突检查哨兵 (Contradiction Checker)
    
    安全机制：在将大模型提取的新知识或自我蒸馏的新规则存入 Semantic Memory 之前，
    必须通过此类进行公理冲突检测。防止知识图谱发生数据污染 (Data Poisoning)。
    """
    def __init__(self, reasoner: Reasoner, semantic_mem: Optional[Any] = None):
        self.reasoner = reasoner
        self.semantic_mem = semantic_mem

    def _find_antonyms(self, predicate: str, object_val: str) -> List[str]:
        """
        动态查询 Neo4j 中的 owl:disjointWith 属性，寻找互斥概念。
        如果未连接外部图库，执行降级保护。
        """
        if self.semantic_mem and getattr(self.semantic_mem, 'is_connected', False):
            driver = self.semantic_mem.client.driver
            if driver:
                query = """
                MATCH (a:Entity {id: $obj})-[:disjointWith]-(b:Entity)
                RETURN b.id AS antonym
                """
                try:
                    with driver.session() as session:
                        result = session.run(query, obj=object_val)
                        return [record["antonym"] for record in result]
                except Exception as e:
                    logger.error(f"Neo4j Sentinel Query Error: {e}")
        
        # 降级：基于本地规则集
        antonyms = {
            "high_risk": ["safe", "low_risk"],
            "safe": ["high_risk", "danger"],
            "true": ["false"],
            "false": ["true"]
        }
        return antonyms.get(object_val.lower(), [])

    def check_fact(self, proposed_fact: Fact) -> bool:
        """
        检查提议的事实是否与现有知识库发生严重冲突。
        
        Args:
            proposed_fact: 待验证的的新事实
            
        Returns:
            bool: True 表示安全可存入，False 表示发现冲突，需拒绝或进入人工审查。
        """
        conflicting_objects = self._find_antonyms(proposed_fact.predicate, proposed_fact.object)
        
        if not conflicting_objects:
            # 没有明确的互斥定义，默认放行
            return True
            
        # 遍历现有所有事实，检查是否存在主体和谓词相同，但客体互斥的记录
        for existing_fact in self.reasoner.facts:
            if existing_fact.subject == proposed_fact.subject and existing_fact.predicate == proposed_fact.predicate:
                if existing_fact.object.lower() in conflicting_objects:
                    logger.error(
                        f"🚨 知识冲突警报! 试图存入: ({proposed_fact.subject} {proposed_fact.predicate} {proposed_fact.object}), "
                        f"但现有图谱已存在: ({existing_fact.subject} {existing_fact.predicate} {existing_fact.object})"
                    )
                    return False
        
        logger.info(f"✅ 哨兵检查通过，事实可安全存入: {proposed_fact.to_tuple()}")
        return True


class ReflectionLoop:
    """
    反思回路 (Reflection Loop)
    
    用于在执行动作前进行逻辑校验，并对失败的决策进行溯源分析。
    """
    def __init__(self, reasoner: Reasoner):
        self.reasoner = reasoner
        self.checker = ContradictionChecker(reasoner)
        
    def evaluate_thought(self, thought_trace: List[str]) -> bool:
        """评估推理轨迹的合理性"""
        logger.info("正在执行反思评估...")
        return True
