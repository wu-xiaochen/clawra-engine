import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class GrainDefinition:
    entity: str
    grain_key: str  # e.g., 'order_id', 'user_id'
    cardinality: str # '1', 'N'

class GrainValidator:
    """
    粒度理论 (Grain Theory) 校验引擎
    
    专门用于拦截 SQL/逻辑聚合中的 "Fan-trap" (扇形陷阱) 问题。
    当一个聚合查询涉及多个一对多关联，且没有正确处理 Cardinality 时，会触发警报。
    """
    
    def __init__(self):
        # 预定义本体中的粒度约束 (未来可从 Neo4j/RDF 加载)
        self.grains = {
            "Order": GrainDefinition("Order", "id", "N"),
            "OrderItem": GrainDefinition("OrderItem", "id", "N"),
            "Supplier": GrainDefinition("Supplier", "id", "1"),
            "Product": GrainDefinition("Product", "id", "1")
        }
        
        # 预定义关联集
        self.relationships = [
            {"from": "Supplier", "to": "Order", "type": "1:N"},
            {"from": "Order", "to": "OrderItem", "type": "1:N"}
        ]

    def validate_query_logic(self, entities_involved: List[str], aggregate_func: Optional[str] = None) -> Dict[str, Any]:
        """
        校验查询逻辑是否存在粒度不一致风险
        """
        if not aggregate_func:
            return {"status": "SAFE", "reason": "No aggregation detected"}
            
        # 核心逻辑：如果在 1:N 关系链上直接对 '1' 端进行 'SUM' 等聚合，存在 Fan-trap 风险
        # 示例：Supplier -> Order (1:N), 如果统计 Supplier 总金额但直接 SUM(Order.amount) 且中间有重复 join
        
        risk_detected = False
        findings = []
        
        # 简化模拟：如果涉及超过 1 个 N 端实体且有聚合
        n_end_entities = [e for e in entities_involved if e in self.grains and self.grains[e].cardinality == "N"]
        
        if len(n_end_entities) > 0 and aggregate_func.upper() in ["SUM", "AVG", "COUNT"]:
            risk_detected = True
            findings.append(f"检测到在 1:N 关系链中对 {entities_involved} 进行 {aggregate_func} 聚合，存在【扇形陷阱】风险。")
            
        if risk_detected:
            return {
                "status": "RISK",
                "risk_level": "CRITICAL",
                "message": "⚠️ 语义拦截：粒度冲突！",
                "details": findings,
                "suggestion": "请检查 SQL 中的 JOIN 逻辑，建议使用子查询预聚合或 DISTINCT 处理。"
            }
            
        return {"status": "SAFE", "reason": "Grain consistency verified"}

def check_fan_trap(query_entities: List[str], agg: str) -> bool:
    validator = GrainValidator()
    result = validator.validate_query_logic(query_entities, agg)
    return result["status"] == "SAFE"
