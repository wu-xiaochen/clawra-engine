"""
Workflow IR (Intermediate Representation) 模块

提供工作流的中间表示，支持：
1. 从JSON/YAML解析工作流定义
2. 编译到目标运行时（LangGraph状态机 / 自研状态机）
3. 与LogicLayer集成

设计原则：
- IR是数据格式，与运行时解耦
- 保持逻辑规则的可读性和portability
- 利用成熟的状态机生态

Usage:
    from src.evolution.workflow_ir import WorkflowIR, WorkflowCompiler

    ir = WorkflowIR.from_json(workflow_json)
    compiled = WorkflowCompiler.compile(ir, target="langgraph")
"""
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib
import logging

logger = logging.getLogger(__name__)


class StepType(Enum):
    """工作流步骤类型"""
    ACTION = "action"           # 执行动作
    CONDITION = "condition"      # 条件判断
    PARALLEL = "parallel"        # 并行执行
    LOOP = "loop"               # 循环
    WAIT = "wait"               # 等待/异步
    END = "end"                 # 结束


class TargetRuntime(Enum):
    """目标运行时"""
    LANGGRAPH = "langgraph"     # LangGraph状态机
    STATE_MACHINE = "state_machine"  # 自研状态机
    RULES = "rules"             # 规则引擎facts


@dataclass
class WorkflowStep:
    """工作流步骤"""
    id: str
    step_type: StepType
    
    # 动作定义（ACTION类型）
    action: Optional[Dict[str, Any]] = None
    
    # 条件定义（CONDITION类型）
    condition: Optional[Dict[str, Any]] = None
    then_step: Optional[str] = None  # 条件为真的下一步
    else_step: Optional[str] = None  # 条件为假的下一步
    
    # 循环定义（LOOP类型）
    loop_until: Optional[str] = None  # 循环终止条件
    loop_body: Optional[List[str]] = None  # 循环体步骤IDs
    
    # 并行定义（PARALLEL类型）
    parallel_steps: Optional[List[str]] = None  # 并行执行的步骤IDs
    
    # 等待定义（WAIT类型）
    wait_for: Optional[str] = None  # 等待的事件/信号
    timeout: Optional[int] = None   # 超时（秒）
    
    # 通用
    next_step: Optional[str] = None  # 默认下一步
    description: Optional[str] = None


@dataclass
class WorkflowIR:
    """
    工作流中间表示
    
    完整的workflow定义，包含元信息和步骤序列。
    与LogicPattern兼容，可以存入LogicLayer。
    """
    id: str
    name: str
    description: str
    
    # 步骤序列
    steps: List[WorkflowStep] = field(default_factory=list)
    
    # 入口步骤
    entry_step: str = "start"
    
    # 元信息
    domain: str = "generic"
    version: int = 1
    confidence: float = 0.9
    
    # 原始定义（用于审计）
    raw_definition: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_json(cls, json_str: str) -> "WorkflowIR":
        """从JSON字符串解析"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowIR":
        """从字典解析"""
        steps = []
        for step_data in data.get("steps", []):
            step = WorkflowStep(
                id=step_data["id"],
                step_type=StepType(step_data.get("type", "action")),
                action=step_data.get("action"),
                condition=step_data.get("condition"),
                then_step=step_data.get("then"),
                else_step=step_data.get("else"),
                loop_until=step_data.get("loop_until"),
                loop_body=step_data.get("loop_body"),
                parallel_steps=step_data.get("parallel"),
                wait_for=step_data.get("wait_for"),
                timeout=step_data.get("timeout"),
                next_step=step_data.get("next"),
                description=step_data.get("description")
            )
            steps.append(step)
        
        return cls(
            id=data.get("id", cls._generate_id(data.get("name", "workflow"))),
            name=data.get("name", "Unnamed Workflow"),
            description=data.get("description", ""),
            steps=steps,
            entry_step=data.get("entry", "start"),
            domain=data.get("domain", "generic"),
            version=data.get("version", 1),
            raw_definition=data
        )
    
    @staticmethod
    def _generate_id(name: str) -> str:
        """生成稳定的ID"""
        return f"wf:{hashlib.md5(name.encode()).hexdigest()[:8]}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "entry": self.entry_step,
            "steps": [
                {
                    "id": s.id,
                    "type": s.step_type.value,
                    "action": s.action,
                    "condition": s.condition,
                    "then": s.then_step,
                    "else": s.else_step,
                    "next": s.next_step,
                    "description": s.description
                }
                for s in self.steps
            ],
            "domain": self.domain,
            "version": self.version
        }
    
    def get_step(self, step_id: str) -> Optional[WorkflowStep]:
        """根据ID获取步骤"""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None


class WorkflowCompiler:
    """
    工作流编译器
    
    将WorkflowIR编译到目标运行时。
    """
    
    @staticmethod
    def compile(
        ir: WorkflowIR,
        target: TargetRuntime,
        context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        编译WorkflowIR到目标运行时
        
        Args:
            ir: 工作流中间表示
            target: 目标运行时
            context: 编译上下文（用于LangGraph等）
            
        Returns:
            编译后的运行时对象
        """
        context = context or {}
        
        if target == TargetRuntime.LANGGRAPH:
            return WorkflowCompiler._compile_langgraph(ir, context)
        elif target == TargetRuntime.STATE_MACHINE:
            return WorkflowCompiler._compile_state_machine(ir, context)
        elif target == TargetRuntime.RULES:
            return WorkflowCompiler._compile_rules(ir)
        else:
            raise ValueError(f"Unknown target runtime: {target}")
    
    @staticmethod
    def _compile_langgraph(
        ir: WorkflowIR,
        context: Dict[str, Any]
    ) -> "StateGraph":
        """
        编译到LangGraph StateGraph
        
        Returns a LangGraph StateGraph that can be compiled and executed.
        """
        try:
            from langgraph.graph import StateGraph, END
        except ImportError:
            raise ImportError(
                "LangGraph not installed. Install with: pip install langgraph"
            )
        
        # 创建状态图
        workflow = StateGraph(
            state_schema=context.get("state_schema"),
            input_schema=context.get("input_schema"),
            output_schema=context.get("output_schema")
        )
        
        # 添加节点
        for step in ir.steps:
            if step.step_type == StepType.ACTION:
                workflow.add_node(step.id, step.action.get("handler"))
            elif step.step_type == StepType.CONDITION:
                # 条件节点
                def make_condition_handler(s: WorkflowStep):
                    def handler(state):
                        # 执行条件判断
                        condition_result = context.get("condition_evaluator", lambda c: True)(s.condition)
                        return "condition_true" if condition_result else "condition_false"
                    return handler
                workflow.add_node(step.id, make_condition_handler(step))
        
        # 添加边
        for step in ir.steps:
            if step.step_type == StepType.ACTION:
                if step.next_step:
                    workflow.add_edge(step.id, step.next_step)
            elif step.step_type == StepType.CONDITION:
                workflow.add_conditional_edges(
                    step.id,
                    context.get("condition_router", lambda s: "continue"),
                    {
                        "true": step.then_step or step.next_step,
                        "false": step.else_step or END
                    }
                )
        
        # 设置入口和出口
        workflow.set_entry_point(ir.entry_step)
        workflow.add_edge(END, END)
        
        return workflow
    
    @staticmethod
    def _compile_state_machine(
        ir: WorkflowIR,
        context: Dict[str, Any]
    ) -> "SimpleStateMachine":
        """
        编译到自研简单状态机
        
        适用于不需要LangGraph依赖的场景。
        """
        
        class SimpleStateMachine:
            """简单状态机"""
            
            def __init__(self, workflow_ir: WorkflowIR):
                self.ir = workflow_ir
                self.current_step: Optional[str] = None
                self.state: Dict[str, Any] = {}
                self._step_handlers: Dict[str, Callable] = {}
                
                # 初始化步骤处理器
                self._init_handlers(context)
            
            def _init_handlers(self, context: Dict[str, Any]):
                """初始化每个步骤的处理函数"""
                for step in self.ir.steps:
                    if step.step_type == StepType.ACTION:
                        self._step_handlers[step.id] = self._make_action_handler(step, context)
                    elif step.step_type == StepType.CONDITION:
                        self._step_handlers[step.id] = self._make_condition_handler(step, context)
                    elif step.step_type == StepType.END:
                        self._step_handlers[step.id] = lambda s: {**s, "done": True}
            
            def _make_action_handler(
                self,
                step: WorkflowStep,
                context: Dict[str, Any]
            ) -> Callable:
                """创建动作处理器"""
                action = step.action or {}
                action_type = action.get("type", "noop")
                
                def handler(state: Dict[str, Any]) -> Dict[str, Any]:
                    if action_type == "noop":
                        return state
                    elif action_type == "update":
                        # 更新状态
                        updates = action.get("updates", {})
                        return {**state, **updates}
                    elif action_type == "call":
                        # 调用函数
                        fn = context.get("functions", {}).get(action.get("fn"))
                        if fn:
                            return fn(state, **action.get("params", {}))
                    return state
                
                return handler
            
            def _make_condition_handler(
                self,
                step: WorkflowStep,
                context: Dict[str, Any]
            ) -> Callable:
                """创建条件处理器"""
                condition = step.condition or {}
                evaluator = context.get("condition_evaluator")
                
                def handler(state: Dict[str, Any]) -> Dict[str, Any]:
                    if evaluator:
                        result = evaluator(condition, state)
                    else:
                        # 默认总是返回true
                        result = True
                    
                    # 根据结果决定下一步
                    next_id = step.then_step if result else step.else_step
                    return {**state, "_next_step": next_id}
                
                return handler
            
            def run(self, initial_state: Dict[str, Any] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
                """
                执行工作流

                Args:
                    initial_state: 初始状态
                    context: 执行上下文

                Returns:
                    最终状态
                """
                context = context or {}
                self.state = initial_state or {}
                self.current_step = self.ir.entry_step

                max_iterations = context.get("max_iterations", 1000)
                iterations = 0

                while self.current_step and iterations < max_iterations:
                    step = self.ir.get_step(self.current_step)
                    if not step:
                        logger.warning(f"Step not found: {self.current_step}")
                        break

                    handler = self._step_handlers.get(step.id)
                    if handler:
                        self.state = handler(self.state)

                    # 决定下一步
                    if step.step_type == StepType.END:
                        break
                    elif step.step_type == StepType.CONDITION:
                        self.current_step = self.state.get("_next_step", step.else_step)
                    else:
                        self.current_step = step.next_step

                    iterations += 1

                return self.state
            
            def get_current_step(self) -> Optional[str]:
                return self.current_step
        
        return SimpleStateMachine(ir)
    
    @staticmethod
    def _compile_rules(ir: WorkflowIR) -> List[Dict[str, Any]]:
        """
        编译到规则引擎facts
        
        将workflow分解为多个LogicPattern (RULE类型)，
        存入LogicLayer执行。
        """
        from .unified_logic import LogicPattern, LogicType
        
        patterns = []
        
        for step in ir.steps:
            if step.step_type == StepType.ACTION and step.action:
                pattern = LogicPattern(
                    id=f"{ir.id}:{step.id}",
                    logic_type=LogicType.RULE,
                    name=f"{ir.name}:{step.id}",
                    description=step.description or f"Workflow step: {step.id}",
                    conditions=[step.condition] if step.condition else [],
                    actions=[step.action],
                    confidence=ir.confidence,
                    source="workflow_ir",
                    domain=ir.domain
                )
                patterns.append(pattern)
        
        return patterns


class WorkflowEngine:
    """
    工作流引擎
    
    统一接口，执行WorkflowIR定义的流程。
    """
    
    def __init__(self, runtime: TargetRuntime = TargetRuntime.STATE_MACHINE):
        self.runtime = runtime
        self._compiled: Optional[Any] = None
        self._ir: Optional[WorkflowIR] = None
    
    def load(self, ir: WorkflowIR) -> None:
        """加载工作流"""
        self._ir = ir
        self._compiled = WorkflowCompiler.compile(ir, self.runtime)
    
    def load_from_json(self, json_str: str) -> None:
        """从JSON加载工作流"""
        ir = WorkflowIR.from_json(json_str)
        self.load(ir)
    
    def execute(
        self,
        initial_state: Dict[str, Any] = None,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        执行工作流

        Args:
            initial_state: 初始状态
            context: 执行上下文
        """
        if not self._compiled:
            raise ValueError("No workflow loaded. Call load() first.")

        context = context or {}

        if self.runtime == TargetRuntime.STATE_MACHINE:
            # 需要把context传给状态机
            return self._compiled.run(initial_state, context)
        elif self.runtime == TargetRuntime.LANGGRAPH:
            # LangGraph需要先编译
            app = self._compiled.compile()
            return app.invoke(initial_state)
        elif self.runtime == TargetRuntime.RULES:
            return {"patterns": self._compiled}
        else:
            raise ValueError(f"Unsupported runtime: {self.runtime}")


# 便捷函数
def create_workflow_engine(
    runtime: str = "state_machine"
) -> WorkflowEngine:
    """创建工作流引擎"""
    return WorkflowEngine(TargetRuntime(runtime))


# 示例工作流JSON
EXAMPLE_WORKFLOW_JSON = """
{
    "id": "wf_user_onboarding",
    "name": "用户入职流程",
    "description": "新用户注册后的引导流程",
    "entry": "welcome",
    "domain": "user_management",
    "steps": [
        {
            "id": "welcome",
            "type": "action",
            "action": {
                "type": "call",
                "fn": "send_welcome_message"
            },
            "next": "check_admin"
        },
        {
            "id": "check_admin",
            "type": "condition",
            "condition": {
                "subject": "?user",
                "predicate": "is_admin",
                "object": true
            },
            "then": "setup_admin",
            "else": "setup_regular"
        },
        {
            "id": "setup_admin",
            "type": "action",
            "action": {
                "type": "call",
                "fn": "create_admin_account"
            },
            "next": "end"
        },
        {
            "id": "setup_regular",
            "type": "action",
            "action": {
                "type": "call",
                "fn": "create_regular_account"
            },
            "next": "end"
        },
        {
            "id": "end",
            "type": "end",
            "description": "流程结束"
        }
    ]
}
"""
