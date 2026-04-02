import ast
import operator
import logging
import json
import yaml
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from pathlib import Path
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class SafeMathSandbox:
    """AST-based secure sandbox for executing dynamically extracted business formulas"""
    
    # Extended operator support including math functions
    allowed_operators = {
        ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow,
        ast.USub: operator.neg, ast.Eq: operator.eq, ast.NotEq: operator.ne,
        ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge,
        ast.And: lambda a,b: a and b, ast.Or: lambda a,b: a or b, ast.Not: operator.not_
    }
    
    # Supported math functions
    allowed_functions = {
        'abs': abs, 'min': min, 'max': max, 'round': round,
        'sum': sum, 'len': len
    }

    @classmethod
    def evaluate(cls, expression: str, context: Dict[str, Any]) -> Any:
        """
        Evaluate expression in secure sandbox
        
        Args:
            expression: Mathematical or logical expression
            context: Variable bindings for evaluation
            
        Returns:
            Result of expression evaluation
            
        Raises:
            ValueError: If expression parsing or evaluation fails
        """
        try:
            tree = ast.parse(expression, mode='eval')
            return cls._eval_node(tree.body, context)
        except SyntaxError as e:
            logger.error(f"Syntax error in expression '{expression}': {e}")
            raise ValueError(f"Invalid expression syntax: {e}")
        except Exception as e:
            logger.error(f"Rule evaluation failed for '{expression}' with context {context}: {e}")
            raise ValueError(f"Expression evaluation failed: {e}")

    @classmethod
    def _eval_node(cls, node, context: Dict[str, Any]):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            if node.id in context:
                return context[node.id]
            raise ValueError(f"Variable '{node.id}' not found in context")
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
        raise TypeError(f"Unsupported AST node type: {type(node)}")


@dataclass
class OntologyRule:
    """Business rule bound to ontology entities with versioning support"""
    id: str
    target_object_class: str
    expression: str
    description: str
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize rule to dictionary"""
        return {
            "id": self.id,
            "target_object_class": self.target_object_class,
            "expression": self.expression,
            "description": self.description,
            "version": self.version,
            "created_at": self.created_at,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OntologyRule':
        """Deserialize rule from dictionary"""
        return cls(
            id=data["id"],
            target_object_class=data["target_object_class"],
            expression=data["expression"],
            description=data["description"],
            version=data.get("version", "1.0.0"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            metadata=data.get("metadata", {})
        )

class RuleEngine:
    """
    Cognitive Graph Rule Engine (Neuro-Symbolic Gatekeeper)
    
    Provides deterministic mathematical validation to prevent LLM hallucinations.
    Supports YAML/JSON rule loading, conflict detection, and versioning.
    """
    
    def __init__(self, rules_path: Optional[Path] = None):
        self.rules: Dict[str, OntologyRule] = {}
        self.rule_history: List[Dict[str, Any]] = []  # Audit trail
        self._register_default_rules()
        
        if rules_path:
            self.load_rules_from_file(rules_path)

    def _register_default_rules(self):
        """Initialize default industry-grade rules"""
        default_rules = [
            OntologyRule(
                id="rule:gas_regulator_safety_margin",
                target_object_class="GasRegulator",
                expression="supply_capacity >= flow_requirement * 1.5",
                description="Gas regulator supply capacity must be at least 1.5x the flow requirement"
            ),
            OntologyRule(
                id="rule:budget_exceed_limit",
                target_object_class="ProcurementProject",
                expression="quoted_price <= planned_budget * 1.1",
                description="Supplier total quote must not exceed 110% of planned budget"
            ),
            OntologyRule(
                id="rule:pressure_range",
                target_object_class="GasRegulator",
                expression="outlet_pressure >= 0.002 and outlet_pressure <= 0.4",
                description="Outlet pressure must be between 2kPa and 400kPa (safe operating range)"
            ),
            OntologyRule(
                id="rule:quantity_positive",
                target_object_class="ProcurementItem",
                expression="quantity > 0",
                description="Procurement quantity must be positive"
            )
        ]
        
        for rule in default_rules:
            self.register_rule(rule)

    def register_rule(self, rule: OntologyRule, check_conflict: bool = True) -> Dict[str, Any]:
        """
        Register a new rule with optional conflict detection
        
        Args:
            rule: Rule to register
            check_conflict: Whether to check for conflicts
            
        Returns:
            Registration result with any conflict warnings
        """
        result = {"status": "success", "rule_id": rule.id, "warnings": []}
        
        if check_conflict:
            conflicts = self._detect_conflicts(rule)
            if conflicts:
                result["warnings"] = conflicts
                logger.warning(f"Rule {rule.id} has potential conflicts: {conflicts}")
        
        
        # Check if rule already exists (versioning)
        if rule.id in self.rules:
            old_rule = self.rules[rule.id]
            self._record_rule_change(old_rule, rule, "UPDATE")
            logger.info(f"Updated rule {rule.id} from version {old_rule.version} to {rule.version}")
        else:
            self._record_rule_change(None, rule, "CREATE")
        
        
        self.rules[rule.id] = rule
        return result

    def _detect_conflicts(self, new_rule: OntologyRule) -> List[str]:
        """
        Detect conflicts between new rule and existing rules
        
        Returns list of conflict descriptions
        """
        conflicts = []
        
        for rule_id, existing_rule in self.rules.items():
            if rule_id == new_rule.id:
                continue
                
            # Same target class, check for contradictory expressions
            if existing_rule.target_object_class == new_rule.target_object_class:
                # Extract variables from expressions
                new_vars = self._extract_variables(new_rule.expression)
                existing_vars = self._extract_variables(existing_rule.expression)
                
                # Check for potential contradictions
                common_vars = set(new_vars) & set(existing_vars)
                if common_vars:
                    conflicts.append(
                        f"Rules '{rule_id}' and '{new_rule.id}' both constrain "
                        f"{new_rule.target_object_class} on variables: {common_vars}"
                    )
        
        
        return conflicts

    def _extract_variables(self, expression: str) -> List[str]:
        """Extract variable names from expression"""
        import re
        # Find all word characters that aren't numbers
        return list(set(re.findall(r'\b([a-zA-Z_]\w*)\b', expression)))

    def _record_rule_change(self, old_rule: Optional[OntologyRule], new_rule: OntologyRule, action: str):
        """Record rule change in audit trail"""
        self.rule_history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "rule_id": new_rule.id,
            "old_version": old_rule.version if old_rule else None,
            "new_version": new_rule.version,
            "old_expression": old_rule.expression if old_rule else None,
            "new_expression": new_rule.expression
        })

    def load_rules_from_file(self, filepath: Path) -> int:
        """
        Load rules from YAML or JSON file
        
        Args:
            filepath: Path to rules file
            
        Returns:
            Number of rules loaded
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Rules file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            if filepath.suffix in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            elif filepath.suffix == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {filepath.suffix}")
        
        rules_data = data.get('rules', []) if isinstance(data, dict) else data
        
        loaded_count = 0
        for rule_dict in rules_data:
            try:
                rule = OntologyRule.from_dict(rule_dict)
                self.register_rule(rule, check_conflict=True)
                loaded_count += 1
            except Exception as e:
                logger.error(f"Failed to load rule: {e}")
                
        logger.info(f"Loaded {loaded_count} rules from {filepath}")
        return loaded_count

    def save_rules_to_file(self, filepath: Path) -> None:
        """Save current rules to file"""
        rules_data = [rule.to_dict() for rule in self.rules.values()]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            if filepath.suffix in ['.yaml', '.yml']:
                yaml.dump({'rules': rules_data}, f, default_flow_style=False)
            elif filepath.suffix == '.json':
                json.dump({'rules': rules_data}, f, indent=2)
            else:
                raise ValueError(f"Unsupported file format: {filepath.suffix}")
                
        logger.info(f"Saved {len(self.rules)} rules to {filepath}")

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
