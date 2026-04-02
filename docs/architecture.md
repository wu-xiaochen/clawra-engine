# Clawra 项目架构指南

## 1. 总体设计思想
Clawra 遵循 **“本体即指令，规则即法律”** 的设计原则。系统通过解构非结构化文本，将其转化为高维本体张量，并利用确定性引擎执行逻辑闭环。

---

## 2. 核心层级说明

### 2.1 认知编排层 (src/agents)
*   **Orchestrator**: 系统的“前额叶”。负责任务拆解、工具选择（Tool Calling）以及元认知（Metacognition）审计。
*   **AdutingEngine**: 实时监控 LLM 的中间思考过程，防止发散过度。

### 2.2 逻辑处理层 (src/core)
*   **Reasoner**: 基于 OWA (开世界假设) 的符号推理机。支持前向链接逻辑推导，可自动补全本体关系网。
*   **RuleEngine**: 基于 Python AST 的沙盒环境。用于执行绝对精确的数学公式校验，是防御 LLM 幻觉的核心关口。

### 2.3 存储与检索层 (src/memory)
*   **SemanticMemory**: 混合存储模式。
    *   **Neo4j**: 存储结构化本体事实 (Subject-Predicate-Object)。
    *   **ChromaDB**: 存储语义向量块，用于关联性上下文召回。
*   **Base Adapter**: 统一了异构数据库的操作接口。

### 2.4 感知提取层 (src/perception)
*   **Extractor**: 利用 LLM 针对性地从庞杂文档中抽丝剥茧。内置中文化分块 (Hierarchical Chunker)，支持超大规模技术规范的高保真解析。

---

## 3. 开发规范与规则

1.  **Facts 唯一性**: 任何 `Fact` 对象必须包含 `confidence` 维度，低于 0.8 的事实在进入本体库前必须经过审计。
2.  **异步支持**: IO 密集型操作（如 API 调用、数据库写入）必须优先使用异步模式，以适配高并发场景。
3.  **解耦原则**: 禁止在 `src/core` 中直接调用具体的大模型 API，所有 LLM 交互必须通过 `src/agents` 层的适配器。
4.  **本体演化**: 对本体架构的新增修改必须同步更新 `data/ontology/schema.json`。
