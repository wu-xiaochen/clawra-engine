# Clawra API 接口手册

本文档定义了 Clawra 核心组件的公开接口规范，供二次开发与集成使用。

---

## 1. 认知编排器 (CognitiveOrchestrator)
路径: `src/agents/orchestrator.py`

### `execute_task(task: str) -> Dict`
*   **功能**: 执行用户输入的复杂自然语言任务。
*   **参数**: `task` (字符串) - 用户的目标或问题。
*   **返回**: 
    - `intent`: 意图识别结果 (INGEST/QUERY/ACTION)。
    - `message`: AI 的最终自然语言回复。
    - `trace`: 详细的推理链条与工具调用链路。

---

## 2. 知识抽取器 (KnowledgeExtractor)
路径: `src/perception/extractor.py`

### `extract_from_text(text: str) -> List[Fact]`
*   **功能**: 从长文本中自动提取本体三元组。
*   **参数**: `text` (字符串) - 工业技术规范或业务文档。
*   **返回**: 结构化的事实对象列表。

---

## 3. 语义存储 (SemanticMemory)
路径: `src/memory/base.py`

### `store_fact(fact: Fact)`
*   **功能**: 将事实同步持久化至 Neo4j 与 ChromaDB。

### `query_subgraph(entity: str, depth: int = 1) -> GraphTraversalResult`
*   **功能**: 从图数据库中检索特定实体的邻域子图，常用于 GraphRAG 上下文注入。

---

## 4. 推理机 (Reasoner)
路径: `src/core/ontology/reasoner.py`

### `forward_chain(max_depth: int = 5) -> ReasoningResult`
*   **功能**: 基于已加载的公理与规则，执行前向逻辑推导。

---

## 5. 通用数据结构 (Data Models)

### `Fact` 对象
```python
{
    "subject": str,   # 主体
    "predicate": str, # 谓词/属性
    "object": str,    # 客体/值
    "confidence": float, # 置信度 (0.0 - 1.0)
    "source": str     # 来源标识
}
```

---

## 接口调用规范
1. **认证**: 所有 API 调用通过环境变量 `OPENAI_API_KEY` 进行鉴权。
2. **频率**: 建议在生产环境中对模型调用进行熔断保护，框架内置了指数退避重试 (Exponential Backoff)。
3. **格式**: 内部数据交换采用 Python 标准字典，对外导出建议使用 JSON 格式。
