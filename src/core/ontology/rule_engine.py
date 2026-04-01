import ast
import operator
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class SafeMathSandbox:
    """基于 AST 的纯净高安全沙盒，用于执行动态提取出的业务公式"""
    allowed_operators = {
        ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow,
        ast.USub: operator.neg, ast.Eq: operator.eq, ast.NotEq: operator.ne,
        ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge,
        ast.And: lambda a,b: a and b, ast.Or: lambda a,b: a or b, ast.Not: operator.not_
    }

    @classmethod
    def evaluate(cls, expression: str, context: Dict[str, Any]) -> Any:
        try:
            tree = ast.parse(expression, mode='eval')
            return cls._eval_node(tree.body, context)
        except Exception as e:
            logger.error(f"Rule evaluation failed for '{expression}' with context {context}: {e}")
            raise ValueError(f"公式求值失败: {e}")

    @classmethod
    def _eval_node(cls, node, context: Dict[str, Any]):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            if node.id in context:
                return context[node.id]
            raise ValueError(f"沙盒找不到变量映射: {node.id}")
        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left, context)
            right = cls._eval_node(node.right, context)
            return cls.allowed_operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand, context)
            return cls.allowed_operators[type(node.op)](operand)
        elif isinstance(node, ast.Compare):
            left = cls._eval_node(node.left, context)
            for op, comparator in zip(node.ops, node.comparators):
                right = cls._eval_node(comparator, context)
                if not cls.allowed_operators[type(op)](left, right):
                    return False
                left = right
            return True
        elif isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                return all(cls._eval_node(v, context) for v in node.values)
            elif isinstance(node.op, ast.Or):
                return any(cls._eval_node(v, context) for v in node.values)
        raise TypeError(f"不支持的语法节点: {type(node)}")


@dataclass
class OntologyRule:
    """与本体实体强绑定的定量业务规则"""
    id: str
    target_object_class: str
    expression: str
    description: str

class RuleEngine:
    """
    认知图谱规则引擎 (Neuro-Symbolic Gatekeeper)
    取代大模型脆弱的内部数学权重认知，提供坚实的防线。
    """
    def __init__(self):
        self.rules: Dict[str, OntologyRule] = {}
        self._register_default_rules()

    def _register_default_rules(self):
        # 初始化几条行业级绝对规则
        self.register_rule(OntologyRule(
            id="rule:gas_regulator_safety_margin",
            target_object_class="GasRegulator",
            expression="supply_capacity >= flow_requirement * 1.5",
            description="调压箱供气能力必须大于等于需求流量的1.5倍"
        ))
        
        self.register_rule(OntologyRule(
            id="rule:budget_exceed_limit",
            target_object_class="ProcurementProject",
            expression="quoted_price <= planned_budget * 1.1",
            description="供应商总报价不得超过预算计划的110%"
        ))

    def register_rule(self, rule: OntologyRule):
        self.rules[rule.id] = rule

    def get_rules_for_object(self, object_class: str) -> List[OntologyRule]:
        return [r for r in self.rules.values() if r.target_object_class == object_class]

    def evaluate_rule(self, rule_id: str, context: Dict[str, float]) -> Dict[str, Any]:
        """执行指定规则并返回评定详情"""
        rule = self.rules.get(rule_id)
        if not rule:
            return {"status": "ERROR", "msg": f"Rule {rule_id} not found."}
        
        try:
            passed = SafeMathSandbox.evaluate(rule.expression, context)
            return {
                "status": "PASS" if passed else "FAIL",
                "rule_name": rule.description,
                "expression": rule.expression,
                "context_used": context
            }
        except Exception as e:
            return {"status": "ERROR", "msg": str(e)}

    def evaluate_action_preconditions(self, action_id: str, object_class: str, context: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        三点聚合 (Action -> Object <- Rule)
        在允许执行物理 Action 前，拉取作用对象上的所有硬性规则闭链验算
        """
        results = []
        bound_rules = self.get_rules_for_object(object_class)
        for rule in bound_rules:
            res = self.evaluate_rule(rule.id, context)
            results.append(res)
        return results
