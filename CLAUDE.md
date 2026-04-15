# Clawra Engine

> **让 AI Agent 自己学会规则，而不是你替它写规则。**

## 项目概述

Clawra 是一款具备**自主进化能力**的神经符号认知代理框架。

**核心特性：**
- 🧠 自主规则学习：从文本自动提取知识，无需手写规则
- 🔄 进化闭环：8 阶段持续学习，AI 从错误中进化
- 🔍 GraphRAG：向量+图谱双通道检索
- 🛡️ SafeMath 沙盒：AST 级数学沙盒防 DoS
- ⚡ 纯异步架构：毫秒级并发响应

## 快速开始

```bash
# 安装
pip install -e .

# 运行 demo
python examples/demo_basic.py

# 启动 Web 界面
PYTHONPATH=. streamlit run examples/web_demo.py
```

## 架构

```
Meta Learner (元学习层)
    ├── Unified Logic Layer (规则/行为/策略/约束)
    ├── Rule Discovery (规则发现引擎)
    └── Self Evaluator (自我评估器)
            ├── Reasoner (推理引擎)
            ├── Memory (Neo4j 图谱 + ChromaDB)
            └── Perception (LLM 知识抽取)
```

## 关键模块

| 模块 | 路径 | 说明 |
|------|------|------|
| 核心入口 | `src/clawra.py` | Clawra 主类 |
| 推理引擎 | `src/core/reasoner.py` | 神经符号推理 |
| 元学习器 | `src/evolution/meta_learner.py` | 从文本学习知识 |
| 规则发现 | `src/evolution/rule_discovery.py` | 自动提取规则 |
| MCP Server | `src/mcp/server.py` | Claude Code 集成 |

## MCP Server（Claude Code 集成）

Clawra 提供 MCP server，可以作为 Claude Code 的记忆和推理引擎。

**配置方法：** 在项目根目录创建 `.claude/mcp.json`：

```json
{
    "mcpServers": {
        "clawra": {
            "command": "python",
            "args": ["-m", "clawra.mcp.server"],
            "cwd": "/path/to/clawra-engine"
        }
    }
}
```

**可用工具：**
- `clawra_learn` - 从文本学习知识规则
- `clawra_add_fact` - 添加事实三元组
- `clawra_reason` - 执行神经符号推理
- `clawra_query_patterns` - 查询已学习的模式
- `clawra_retrieve` - GraphRAG 知识检索
- `clawra_evolve` - 触发 8 阶段自主进化
- `clawra_stats` - 获取系统统计

## 测试

```bash
# 运行所有测试
pytest tests/ -q

# 运行特定测试
pytest tests/core/test_reasoner.py -q

# 查看测试覆盖率
pytest tests/ --cov=src --cov-report=term-missing
```

## 环境变量

```bash
MINIMAX_API_KEY=xxx     # 用于 LLM 相关的功能
NEO4J_URI=bolt://localhost:7687  # Neo4j 图数据库
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=xxx
```
