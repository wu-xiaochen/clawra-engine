# Clawra: 动力学本体认知引擎 (Agent Growth SDK)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](blob/main/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Neo4j](https://img.shields.io/badge/Neo4j-Active-green.svg)](https://neo4j.com/)

**Clawra** 是一款专为工业与复杂业务场景设计的**神经符号 (Neuro-Symbolic) 认知代理框架**。它突破了传统 LLM 仅依赖概率预测的局限，通过**本体约束 (Ontology Constraints)**、**确定性规则引擎 (Rule Engine)** 以及 **GraphRAG (图增强检索)**，实现了具备逻辑自洽性、零幻觉特征的智能体生长系统。

---

## 核心特性

- 🧠 **神经符号架构**: 结合了大模型的语义理解力与符号逻辑的严谨性。
- 🕸️ **动力学本体**: 建立在 Neo4j 之上的 10,000+ 工业事实底座，支持实时知识抽取与关联推理。
- 🛡️ **规则引擎 (RuleEngine)**: 内置 AST 级数学沙盒，强制校验由于模型幻觉引发的参数偏差（如压力、流量级别）。
- 🔍 **GraphRAG**: 深度整合向量库 (ChromaDB) 与图数据库 (Neo4j)，提供基于关联路径的长短期记忆。
- 🤖 **认知中枢 (Orchestrator)**: 具备自省与审计能力的编排引擎，支持对决策链的全程追溯。

---

## 快速开始

### 1. 环境准备
确保您的环境中已安装 Python 3.10+ 及 Neo4j。

```bash
git clone https://github.com/wu-xiaochen/ontology-platform.git
cd ontology-platform
pip install -r requirements.txt
```

### 2. 配置文件
在项目根目录创建 `.env` 文件，配置您的 API 密钥与数据库：

```env
OPENAI_API_KEY=your_volcengine_ark_key
OPENAI_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
OPENAI_MODEL=doubao-seed-2-0-pro-260215

# Neo4j 配置
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### 3. 启动演示端
Clawra 提供了一个全功能的 Streamlit 控制台，用于可视化推理过程。

```bash
streamlit run examples/streamlit_app.py
```

---

## 项目架构

项目采用模块化分层设计，确保各组件的高内聚低耦合：

- `src/agents`: 认知编排器，负责 LLM 规划与工具决策。
- `src/core`: 核心逻辑层，包含 `Reasoner` (推理机) 与 `RuleEngine` (规则引擎)。
- `src/memory`: 存储层，封装了 Neo4j 三元组操作与 ChromaDB 向量检索。
- `src/perception`: 感知层，负责从非结构化文档中提取结构化知识。
- `docs/`: 详细的架构方案与 API 参考手册。

---

## 开发规范

为了保持认知引擎的严谨性，开发者应遵循以下准则：
1. **语义自足**: 所有提取出的事实必须符合本体语义，优先使用 `src/core/ontology` 中定义的公理。
2. **审计优先**: 任何关键决策必须记录 Trace 链路，供 `AdutiingEngine` 实时回溯。
3. **零幻觉原则**: 涉及数值计算时，必须通过 `RuleEngine` 过滤，禁止让 LLM 直接输出计算结果。

---

## 路线图 (Roadmap)
- [x] 迁移至火山引擎 Ark (Doubao Pro)。
- [x] 实现 10,000+ 工业事实的 GraphRAG 闭环。
- [ ] 支持多模态本体抽取。
- [ ] 引入联邦式本体协作。

---

## 许可证
本项目采用 Apache 2.0 许可证。
