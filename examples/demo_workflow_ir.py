"""
Demo: Workflow IR 工作流中间表示

演示：
1. 如何从JSON定义工作流
2. 如何编译到自研状态机执行
3. 如何与LogicLayer集成

Usage:
    python examples/demo_workflow_ir.py
"""
import json
from src.evolution.workflow_ir import (
    WorkflowIR,
    WorkflowCompiler,
    WorkflowEngine,
    TargetRuntime,
    EXAMPLE_WORKFLOW_JSON
)

def demo_basic_workflow():
    """演示基本工作流解析和执行"""
    
    print("\n=== Demo 1: 基本工作流解析 ===\n")
    
    # 使用示例JSON
    ir = WorkflowIR.from_json(EXAMPLE_WORKFLOW_JSON)
    
    print(f"工作流: {ir.name}")
    print(f"ID: {ir.id}")
    print(f"描述: {ir.description}")
    print(f"入口步骤: {ir.entry_step}")
    print(f"步骤数量: {len(ir.steps)}")
    
    for step in ir.steps:
        print(f"\n  步骤 [{step.id}]")
        print(f"    类型: {step.step_type.value}")
        if step.action:
            print(f"    动作: {step.action}")
        if step.condition:
            print(f"    条件: {step.condition}")
        if step.next_step:
            print(f"    下一步: {step.next_step}")
        if step.then_step:
            print(f"    then → {step.then_step}, else → {step.else_step}")
    
    return ir


def demo_state_machine_execution(ir: WorkflowIR):
    """演示状态机执行"""
    
    print("\n=== Demo 2: 状态机执行 ===\n")
    
    # 定义动作函数
    def send_welcome_message(state, **kwargs):
        print("  [执行] 发送欢迎消息")
        return {**state, "welcome_sent": True}
    
    def create_admin_account(state, **kwargs):
        print("  [执行] 创建管理员账户")
        return {**state, "account_type": "admin", "setup_complete": True}
    
    def create_regular_account(state, **kwargs):
        print("  [执行] 创建普通账户")
        return {**state, "account_type": "regular", "setup_complete": True}
    
    # 条件评估器
    def evaluate_condition(condition, state):
        """简单条件评估"""
        if condition.get("predicate") == "is_admin":
            return state.get("user_is_admin", False)
        return False
    
    # 编译到状态机
    context = {
        "functions": {
            "send_welcome_message": send_welcome_message,
            "create_admin_account": create_admin_account,
            "create_regular_account": create_regular_account
        },
        "condition_evaluator": evaluate_condition,
        "max_iterations": 100
    }
    
    # 使用自研状态机
    engine = WorkflowEngine(TargetRuntime.STATE_MACHINE)
    engine.load(ir)
    
    # 测试1: 普通用户
    print("--- 普通用户流程 ---")
    state1 = {"user_id": "user123", "user_is_admin": False}
    result1 = engine.execute(state1, context)
    print(f"  最终状态: {result1}")
    
    # 测试2: 管理员用户
    print("\n--- 管理员用户流程 ---")
    state2 = {"user_id": "admin456", "user_is_admin": True}
    result2 = engine.execute(state2, context)
    print(f"  最终状态: {result2}")


def demo_workflow_from_dict():
    """演示从字典创建工作流"""
    
    print("\n=== Demo 3: 从字典创建工作流 ===\n")
    
    workflow_data = {
        "id": "wf_simple_decision",
        "name": "简单决策流程",
        "description": "测试条件分支",
        "entry": "start",
        "steps": [
            {
                "id": "start",
                "type": "action",
                "action": {"type": "update", "updates": {"step": "start"}},
                "next": "decide"
            },
            {
                "id": "decide",
                "type": "condition",
                "condition": {"field": "value", "op": "gt", "threshold": 10},
                "then": "high",
                "else": "low"
            },
            {
                "id": "high",
                "type": "action",
                "action": {"type": "update", "updates": {"result": "high_value"}},
                "next": "end"
            },
            {
                "id": "low",
                "type": "action",
                "action": {"type": "update", "updates": {"result": "low_value"}},
                "next": "end"
            },
            {
                "id": "end",
                "type": "end"
            }
        ]
    }
    
    ir = WorkflowIR.from_dict(workflow_data)
    print(f"创建工作流: {ir.name}")
    print(f"步骤数: {len(ir.steps)}")
    
    # 简单执行
    engine = WorkflowEngine(TargetRuntime.STATE_MACHINE)
    engine.load(ir)
    
    # 测试高值
    print("\n--- 测试高值 (value=15) ---")
    result = engine.execute({"value": 15})
    print(f"  结果: {result}")
    
    # 测试低值
    print("\n--- 测试低值 (value=5) ---")
    result = engine.execute({"value": 5})
    print(f"  结果: {result}")


def demo_compile_to_rules(ir: WorkflowIR):
    """演示编译到规则引擎"""
    
    print("\n=== Demo 4: 编译到规则引擎 ===\n")
    
    rules = WorkflowCompiler.compile(ir, TargetRuntime.RULES)
    
    print(f"生成 {len(rules)} 条规则:")
    for rule in rules:
        print(f"\n  [{rule.id}]")
        print(f"    name: {rule.name}")
        print(f"    description: {rule.description}")
        print(f"    conditions: {rule.conditions}")
        print(f"    actions: {rule.actions}")


if __name__ == "__main__":
    print("=" * 60)
    print("Workflow IR 工作流中间表示演示")
    print("=" * 60)
    
    # Demo 1: 基本解析
    ir = demo_basic_workflow()
    
    # Demo 2: 状态机执行
    demo_state_machine_execution(ir)
    
    # Demo 3: 从字典创建
    demo_workflow_from_dict()
    
    # Demo 4: 编译到规则
    demo_compile_to_rules(ir)
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)
    print("""
下一步:
1. 尝试自定义工作流JSON
2. 集成到LogicLayer作为WORKFLOW类型patterns
3. 实现LangGraph编译（需要安装langgraph）
""")