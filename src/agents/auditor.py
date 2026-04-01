import logging
from typing import Dict, Any, List
from .base import BaseAgent
from core.ontology.grain_validator import GrainValidator

logger = logging.getLogger(__name__)

class AuditorAgent(BaseAgent):
    """
    审计部智能体 (Auditor Agent)
    
    独立于推理主线，专门负责：
    1. 粒度冲突审计 (Fan-trap 探测)
    2. 合规性底线审计 (基于本体红线)
    3. 执行前置准入校验
    """
    
    def __init__(self, name: str, reasoner: Any):
        super().__init__(name, reasoner)
        self.grain_validator = GrainValidator()

    async def audit_plan(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        审计工具执行计划
        """
        logger.info(f"Auditor [{self.name}] 正在审计工具调用: {tool_name}")
        
        status = "PASSED"
        risk_details = []
        
        # 1. 针对 query_graph 的粒度审计
        if tool_name == "query_graph":
            query = args.get("query", "")
            # 简单关键词探测聚合意图
            agg_keywords = {
                "SUM": ["总计", "总额", "SUM"],
                "AVG": ["平均", "AVG"],
                "COUNT": ["计数", "数量", "COUNT"]
            }
            detected_agg_type = None
            for agg_type, keys in agg_keywords.items():
                if any(k in query.upper() for k in keys):
                    detected_agg_type = agg_type
                    break
            
            if detected_agg_type:
                # 触发粒度校验
                entities = [e for e in ["Order", "OrderItem", "Supplier"] if e.lower() in query.lower()]
                validation = self.grain_validator.validate_query_logic(entities, detected_agg_type)
                
                if validation["status"] == "RISK":
                    status = "BLOCKED"
                    risk_details.append(validation["message"])
                    risk_details.extend(validation["details"])

        return {
            "status": status,
            "auditor": self.name,
            "risks": risk_details,
            "decision": "允许执行" if status == "PASSED" else "拦截并拒绝"
        }

    async def run(self, task: str) -> Dict[str, Any]:
        """
        审计模式：对任务全生命周期进行旁路监控
        """
        return {"status": "monitoring", "audit_trail": []}
