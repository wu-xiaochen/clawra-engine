# Clawra 本体方法论 v1.0

> 让 AI Agent 从"知道规则"到"执行动作"的完整认知架构

---

## 1. 核心理念

**三层认知映射：**

```
描述层 (What)          →  推理层 (If-Then)     →  执行层 (Do)
KnowledgeGraph        →  LogicPattern         →  ActionRuntime
(RDF三元组)           →  (条件→动作)           →  (Skill执行)
```

| 层级 | 问题 | 回答 |
|------|------|------|
| **描述层** | 这个东西是什么？ | RDF三元组：`(?s, ?p, ?o)` |
| **推理层** | 满足条件时怎么办？ | LogicPattern：`conditions → actions` |
| **执行层** | 具体怎么动？ | ActionRuntime：`execute Skill` |

---

## 2. 本体表达（描述层）

### 2.1 节点类型 (NodeLabel)

```
Entity     — 具体实体（人、设备、文档）
Concept    — 抽象概念（安全策略、质量标准）
Rule       — 规则定义（作为节点存储）
Individual — 实例
Class      — 类定义
Property   — 属性定义
```

### 2.2 关系类型 (RelationshipType)

```
HAS_PROPERTY   — 拥有属性
INSTANCE_OF    — 是...的实例
SUB_CLASS_OF   — 是...的子类
SUB_PROPERTY_OF— 是...的子属性
EQUIVALENT_TO  — 等价于
RELATED_TO     — 相关于
CAUSED_BY      — 由...引起
DEPENDS_ON     — 依赖于
INFERRED_FROM  — 由...推断
```

### 2.3 三元组标准格式

```json
{
  "subject": "设备-A",
  "predicate": "HAS_PROPERTY",
  "object": "温度传感器",
  "confidence": 0.95,
  "source": "manual"
}
```

---

## 3. 逻辑表达（推理层）

### 3.1 LogicType 枚举

```python
class LogicType(Enum):
    RULE       = "rule"        # 推理规则：If A then B
    BEHAVIOR   = "behavior"     # 行为模式：If 触发 then 动作序列
    POLICY     = "policy"       # 策略决策：目标→路径选择
    CONSTRAINT = "constraint"   # 约束条件：必须满足的限制
    WORKFLOW   = "workflow"     # 工作流：多步骤过程
```

### 3.2 LogicPattern 数据类

```python
@dataclass
class LogicPattern:
    id: str                    # 唯一标识
    logic_type: LogicType      # 逻辑类型
    
    # 条件部分（前提）
    conditions: List[Dict]     # 三元组列表，支持变量
    # 例: [{"subject": "?X", "predicate": "is_a", "object": "device"}]
    
    # 动作部分（结论/行为）
    actions: List[Dict]        # 动作定义
    # 例: [{"type": "execute", "skill": "skill_check_safety", "args": {...}}]
    
    # 元信息
    confidence: float = 0.8
    source: str = "learned"    # learned | manual | inferred
    domain: str = "generic"
    
    # 学习反馈
    usage_count: int = 0
    success_count: int = 0
    failure_count: int = 0
```

### 3.3 条件-动作示例

**BEHAVIOR 类型：**
```json
{
  "id": "behavior:device_overheat",
  "logic_type": "behavior",
  "name": "设备过热处理",
  "conditions": [
    {"subject": "?device", "predicate": "HAS_PROPERTY", "object": "温度传感器"},
    {"subject": "?device", "predicate": "HAS_PROPERTY", "object": "温度"},
    {"subject": "?device", "predicate": "HAS_VALUE", "object": "> 80°C"}
  ],
  "actions": [
    {"type": "execute", "skill": "skill_alert_operator", "args": {"level": "critical"}},
    {"type": "execute", "skill": "skill_reduce_power", "args": {"device": "?device"}},
    {"type": "infer", "subject": "?device", "predicate": "HAS_STATUS", "object": "overheated"}
  ]
}
```

**CONSTRAINT 类型：**
```json
{
  "id": "constraint:max_temperature",
  "logic_type": "constraint",
  "name": "温度上限约束",
  "conditions": [],
  "actions": [
    {"type": "validate", "subject": "?device", "predicate": "temperature", "expected": "<= 80°C"}
  ]
}
```

---

## 4. 执行表达（执行层）

### 4.1 动作类型 (ActionType)

```python
class ActionType(Enum):
    INFER      = "infer"      # 推导新三元组
    NOTIFY     = "notify"      # 发送通知
    VALIDATE   = "validate"   # 校验约束
    TRANSFORM  = "transform"  # 数据转换
    EXECUTE    = "execute"    # 执行 Skill ← 核心
```

### 4.2 动作执行流程

```
LogicPattern.actions[action]
    ↓
ActionRuntime.execute_action(action, bindings)
    ↓
解析 action.type:
  - infer     → 写入 KnowledgeGraph
  - notify    → 触发事件处理器
  - validate  → 校验约束
  - transform → 数据转换
  - execute   → 执行 UnifiedSkillRegistry 中的 Skill
    ↓
Skill 执行结果 → ActionResult
    ↓
反馈到 SelfEvaluator → 更新 LogicPattern 置信度
```

### 4.3 动作与 Skill 绑定

```python
# action 定义示例
{
  "type": "execute",
  "skill": "skill_alert_operator",      # Skill ID
  "args": {
    "channel": "feishu",
    "message": "设备 ?device 温度异常: ?temp"
  }
}

# Skill 执行签名
def skill_alert_operator(channel: str, message: str, **kwargs) -> dict:
    """统一 Skill 签名：参数 + **kwargs（bindings 自动注入）"""
    ...
    return {"status": "sent", "recipient": channel}
```

---

## 5. Skill 生态系统

### 5.1 Skill 类型

```python
class SkillType(Enum):
    CODE      = "code"     # Python 代码技能
    PROMPT    = "prompt"   # Prompt 模板技能
    COMPOSITE = "composite"# 组合技能（多个子 Skill）
```

### 5.2 Skill 数据结构

```python
@dataclass
class Skill:
    id: str
    skill_type: SkillType
    name: str
    description: str
    
    # 代码技能
    code: Optional[str] = None
    
    # Prompt 技能
    prompt_template: Optional[str] = None
    
    # 元信息
    version: str = "1.0.0"
    author: str = "system"
    confidence: float = 0.8
    
    # 安全信息
    required_permissions: List[str] = field(default_factory=list)
    safety_level: str = "safe"  # safe | cautious | dangerous
    
    # 审计追踪
    created_at: str = field(default_factory=datetime.now().isoformat)
    usage_count: int = 0
    success_rate: float = 0.0
```

### 5.3 Skill 执行器

```python
class UnifiedSkillRegistry:
    """统一 Skill 注册与执行中心"""
    
    def register_skill(self, skill: Skill) -> bool:
        """注册 Skill"""
        ...
    
    def execute_skill(
        self,
        skill_id: str,
        args: Dict[str, Any],
        bindings: Dict[str, str] = None
    ) -> ActionResult:
        """执行 Skill，支持变量绑定替换"""
        ...
    
    def validate_skill(self, skill: Skill) -> ValidationResult:
        """Skill 上线前安全审查"""
        ...
```

---

## 6. 完整执行示例

### 6.1 场景：设备过热自动处理

**Step 1: 知识写入**
```
用户说: "设备-A 温度传感器检测到 85°C"
→ KnowledgeGraph 写入三元组
  (设备-A, HAS_PROPERTY, 温度传感器)
  (设备-A, HAS_VALUE, 85°C)
```

**Step 2: 事件触发推理**
```
KnowledgeGraph.on_triple_added() 触发
→ ActionRuntime._on_triple_added()
→ 匹配 LogicPattern: behavior:device_overheat
→ 提取 bindings: {"?device": "设备-A", "?temp": "85°C"}
```

**Step 3: Skill 执行**
```python
# Pattern actions 执行
actions = [
    {
        "type": "execute",
        "skill": "skill_alert_operator",
        "args": {"level": "critical", "device": "?device"}
    },
    {
        "type": "execute",
        "skill": "skill_reduce_power",
        "args": {"device": "?device", "target": "50%"}
    }
]

# ActionRuntime 解析 bindings 并执行
skill_result = skill_registry.execute_skill(
    "skill_alert_operator",
    args={"level": "critical", "device": "设备-A"}
)
```

**Step 4: 结果回写**
```python
# infer action 写入新三元组
infer_result = action_runtime.execute_action(
    {"type": "infer", "subject": "设备-A", "predicate": "HAS_STATUS", "object": "overheated"}
)
```

**Step 5: 自我评估**
```
SelfEvaluator 记录:
- LogicPattern(behavior:device_overheat) 被触发 1 次
- skill_alert_operator 执行成功
- success_count += 1
→ 更新 confidence 加权平均
```

---

## 7. 架构总览图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Clawra Engine                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐  │
│  │   Knowledge  │───▶│  ActionRuntime   │───▶│  SkillRegistry│  │
│  │    Graph     │    │  (条件匹配+执行)  │    │   (技能执行)  │  │
│  │  (RDF三元组) │    │                  │    │              │  │
│  └──────────────┘    └──────────────────┘    └──────────────┘  │
│         │                    │                     │          │
│         │                    │                     │          │
│         ▼                    ▼                     ▼          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  UnifiedLogicLayer                     │   │
│  │  ┌─────────┐  ┌───────────┐  ┌──────────┐             │   │
│  │  │ RULE    │  │ BEHAVIOR  │  │ CONSTRAINT│ ...        │   │
│  │  │ conditions               │                    │             │   │
│  │  │   ↓      │  │   ↓       │  │    ↓      │             │   │
│  │  │ actions  │  │  actions  │  │  actions  │             │   │
│  │  └─────────┘  └───────────┘  └──────────┘             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                 │
│                              ▼                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   SelfEvaluator                         │   │
│  │           (usage_count / success_rate)                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. 设计原则

### 8.1 零硬编码
- 所有逻辑通过 `LogicPattern` 表达
- 动作参数通过 `bindings` 变量绑定
- 配置从 `ConfigManager` 读取

### 8.2 安全优先
- Skill 执行前经过 `skill_vetter` 安全审查
- `dangerous` 级别 Skill 需要二次确认
- 所有执行记录审计日志

### 8.3 自我进化
- 执行结果反馈到 `SelfEvaluator`
- 成功/失败次数更新 `confidence`
- 低置信度 Pattern 触发重新学习

### 8.4 Skill 优先于 脚本
- 不用临时脚本，所有可执行能力封装为 Skill
- Skill 可复用、可审计、可组合
- Skill 失败时降级到 `infer` 类型

---

---

## 9. 缺陷诊断与修复 (Defect Analysis)

### Defect #1: ActionRuntime 初始化时未注入 SkillRegistry

**症状：** `ActionRuntime._execute_function` 优先走 SkillRegistry，但 `Clawra.__init__` 创建 ActionRuntime 时未传入 skill_registry。

**影响：** `action.type="execute"` 降级到兼容路径，找不到函数就报错了。

**修复：** `Clawra.__init__` 中创建 `UnifiedSkillRegistry` 并注入：
```python
self.skill_registry = UnifiedSkillRegistry(semantic_memory=None)
self.action_runtime = ActionRuntime(
    self.knowledge_graph,
    self.logic_layer,
    skill_registry=self.skill_registry
)
```

**状态：** 🟢 已修复 (v4.2.1)

---

### Defect #2: `_match_rules_for_triple` 只匹配 `RULE` 类型

**症状：** `ActionRuntime` 事件驱动只触发 `RULE` 类型 pattern，`BEHAVIOR` / `CONSTRAINT` / `POLICY` 被忽略。

**影响：** 行为模式（设备过热→发警报）和约束（温度上限校验）无法被事件自动触发。

**修复：** 扩展匹配范围：
```python
if pattern.logic_type.value not in ("rule", "behavior", "constraint", "policy", "workflow"):
    continue
```

**状态：** 🟢 已修复 (v3.1)

---

### Defect #3: Palantir 三层对照缺失 — Kinetic 层未对接 Ontology Objects

**症状：** Palantir Ontology 中，Action 作用在 **ObjectType**（如 `Regulator`, `Order`）上，有 Object-level 安全和验证。Clawra 的 ActionRuntime 执行时缺少这一层。

**影响：** Action 执行前没有 ObjectType 验证，Action 结果没有写回到 Ontology 的对象层。

**修复：** 在 `LogicPattern` 中添加 `object_type` 字段（默认 "Generic"），对标 Palantir ObjectType。在 `ActionRuntime` 中添加 `_validate_object_type()` 方法，在 `execute_rule` 开头执行前验证：Generic 直接放行，具体类型时从 bindings 提取主体查询 KnowledgeGraph 校验类型标签。同时在 `neo4j_client.py` 中新增 `ObjectType` 枚举（Regulator/Sensor/Order/Asset/User/Agent/Skill/Pattern）。验证失败则拒绝执行。

**状态：** 🟢 已修复 (v4.2.1)

### Defect #4: Action 执行链无原子性和 critical 语义

**症状：** Pattern 的 actions 列表顺序执行时，中间某个 action 失败后继续执行后续 action，没有 "critical" 语义。

**影响：** 错误的动作序列（如先发成功通知再执行回滚）导致状态不一致。

**修复：** 添加 `critical` 字段支持：
```python
if action.get("critical", False):
    logger.warning(f"关键动作失败，停止执行: {action}")
    break
```

**状态：** 🟢 已修复 (v3.1)

---

### Defect #5: Skill 执行结果未反馈到 SelfEvaluator

**症状：** `action.type="execute"` 执行后，Skill 的 success/failure 未写入 LogicPattern 的 `usage_count` / `success_count` / `failure_count`。

**影响：** 自我进化无法基于 Skill 执行结果调整置信度。

**修复：** 在 `execute_rule` 中，对 `execute` action 类型立即调用 `pattern.update_success_rate(result.success)`，不等待整条规则结束。修复后 execute action 统计独立，不被同规则其他 action 污染。

**状态：** 🟢 已修复 (v4.2.1)

---

### Defect #6: Skill 上线前未经过安全审查

**症状：** `UnifiedSkillRegistry.register_skill` 只做了静态 AST 安全检查，没有集成 `skill_vetter` 多扫描器审查流程。

**影响：** 恶意或高危 Skill 可能直接上线执行。

**修复：** 在 `register_skill` 中，对 `CODE / EXECUTABLE / SCRIPT` 类型调用新增的 `_run_skill_vetter()` 方法，将 Skill 内容写入临时目录生成 SKILL.md，再调用 `vett.sh` 多扫描器审查。`BLOCKED` 级别直接拒绝，`REVIEW` 级别警告后放行，`SAFE` 通过。同时保留原有的 AST 静态检查作为第二层防护。

**状态：** 🟢 已修复 (v4.2.1)

---

## 10. 与 Palantir Ontology 的架构对照

| Palantir 概念 | Clawra 实现 | 差距 |
|---------------|-------------|------|
| **Semantic Layer** | | |
| ObjectType | `NodeLabel.ENTITY` | ✅ 基础存在 |
| Property | `RelationshipType.HAS_PROPERTY` | ✅ 存在 |
| LinkType | 其他 `RelationshipType` | ✅ 基础存在 |
| **Kinetic Layer** | | |
| ActionType (on ObjectType) | `LogicPattern.actions` | ⚠️ 缺少 ObjectType 上下文 |
| Function (server-side logic) | `ActionRuntime.execute_skill()` | ✅ 已打通 |
| Object-level security | — | 🔴 缺失 |
| Validation (pre-condition) | `CONSTRAINT` type | ⚠️ 有类型，缺少验证执行 |
| **Dynamic Layer** | | |
| Ontology Sync (实时同步) | `KnowledgeGraph` 内存/Neo4j | ⚠️ 缺少增量同步 |
| Agent orchestration | `Orchestrator` | ✅ 存在 |
| **自我进化** | | |
| Usage → Confidence | `LogicPattern.success_count` | ⚠️ Skill 执行未反馈 |
| Skill Library | `UnifiedSkillRegistry` | ✅ 基础存在 |
| Skill 自生成 (distillation) | `SkillDistiller` | ⚠️ 缺少 Skill 执行反馈 |

---

## 11. 待办事项

| 优先级 | 任务 | 状态 |
|--------|------|------|
| P0 | ActionRuntime 与 UnifiedSkillRegistry 打通 | 🟢 已完成 (v4.2.1) |
| P0 | `_match_rules_for_triple` 匹配所有触发型 LogicType | 🟢 已完成 (v3.1) |
| P0 | `execute` action → `critical` 失败中断机制 | 🟢 已完成 (v3.1) |
| P0 | Skill 执行结果反馈到 SelfEvaluator (Defect #5) | 🟢 已完成 (v4.2.1) |
| P0 | `register_skill` 集成 `skill_vetter` 安全审查 (Defect #6) | 🟢 已完成 (v4.2.1) |
| P1 | Action 执行增加 ObjectType 验证层 (Defect #3) | 🟢 已完成 (v4.2.1) |
| P2 | 推理轨迹自动写入 Neo4j 形成执行链审计 | 🟡 规划中 |
| P2 | 完善 `distillation.py` 推理轨迹→Skill 流程 | 🟡 进行中 |

---

## 12. 参考文献

- Palantir Kinetic Ontology — 从描述型到可执行型知识
- Palantir Foundry API: Action Types — `POST /api/v2/ontologies/{ontology}/actions/{action}/apply`
- Voyager Skill Library — 技能自进化
- Clawra Engine v4.2 — 自主进化框架
