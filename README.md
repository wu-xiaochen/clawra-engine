# 🧠 Clawra Engine

> **让 AI 真正自己学会规则，而不是你替它写规则。**
> 元学习 × 知识图谱 × 神经符号融合 — 自主进化的 Agent 认知引擎

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/wu-xiaochen/clawra-engine/blob/main/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-433%20%25%20passing-brightgreen)](https://github.com/wu-xiaochen/clawra-engine/actions)
[![GitHub Stars](https://img.shields.io/github/stars/wu-xiaochen/clawra-engine?style=social)](https://github.com/wu-xiaochen/clawra-engine/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/wu-xiaochen/clawra-engine?style=social)](https://github.com/wu-xiaochen/clawra-engine/network)
[![Discord](https://img.shields.io/badge/Discord-Join-blue?logo=discord)](https://discord.gg/clawra)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-blue?logo=twitter)](https://twitter.com/clawra_ai)

---

## ⚡ 5 分钟上手（无需 API Key，离线可跑 demo）

```bash
git clone https://github.com/wu-xiaochen/clawra-engine.git
cd clawra-engine
pip install -e .                    # 安装（含全部依赖）
python examples/demo_basic.py        # 跑！← **无需配置，立即出结果**
```

---

### 🔥 demo_basic.py 运行效果

```
============================================================
🤖 Clawra 自主进化智能体 — 基础演示
============================================================

[Step 1] 初始化 Clawra（无记忆层）...
  ✓ Clawra 初始化完成

[Step 2] 从文本学习知识...
  ✓ 学习完成: success=True
    - 自动生成事实数: 1
    - 学习到的模式: ['learned:llm_entity:gas_equipment:ep_xxx:0']

[Step 3] 手动添加事实三元组...
  ✓ 添加了 4 条事实三元组

[Step 4] 执行前向链推理...
  ✓ 推理完成，发现 2 条结论（传递性规则）
    → 调压箱A is_a 概念 (置信度 0.99)
    → 调压箱A is_a 城市燃气输配系统中的关键设备 (置信度 0.99)

[Step 5] 查询学习到的模式...
  ✓ 找到 1 个相关模式

[Step 6] GraphRAG 知识检索...
  ✓ 检索到 5 条相关知识

[Step 7] 系统统计信息...
  ✓ 事实总数: 10 | 实体: 13 | 模式: 3

✅ demo_basic.py 完成！
```

**10 个完整示例，全部能跑：**

```bash
python examples/demo_basic.py                 # 基础演示（离线可跑）
python examples/demo_graphrag.py              # GraphRAG 检索
python examples/demo_leiden_community.py       # Leiden 社区检测
python examples/demo_pattern_versioning.py     # Pattern 版本控制
python examples/demo_confidence_reasoning.py   # 置信度推理
python examples/demo_case_based_reasoner.py    # 案例推理
python examples/demo_evolution_loop.py         # 进化闭环
python examples/demo_supplier_monitor.py       # 供应商监控 Agent
python examples/demo_clawra_e2e.py             # E2E 端到端
PYTHONPATH=. streamlit run examples/web_demo.py  # Web 界面
```

> 💡 带 LLM 的示例（`learn()`、`evolution_loop`）需要配置 `MINIMAX_API_KEY`，纯逻辑示例完全离线可跑。

---

## 🎯 这是什么？

**Clawra** 是一款具备**自主进化能力**的神经符号认知代理框架。

```
传统 Agent:  你写 1000 条 if-else → AI 只能按你的剧本走
Clawra:       给它文本/案例/反馈 → 它自己学会规则并进化
```

---

## ⚔️ 核心能力 vs 传统框架

| | LangChain / LangGraph | Clawra Engine |
|---|---|---|
| 规则来源 | 你手写（hardcode） | **AI 从文本自动学习** |
| 幻觉防护 | 无 | **符号逻辑双重拦截** |
| 计算安全 | 无 | **AST 沙盒防 DoS** |
| 知识检索 | 纯向量 RAG | **GraphRAG 混合检索** |
| 自我进化 | 静态 | **8 阶段进化闭环** |
| 架构 | 重（依赖 LangChain） | **轻量内置（无 LangChain）** |

---

## 🧠 核心理念：零硬编码规则

传统 Agent 框架让开发者写大量规则来控制 AI 行为，但：

- 每个新领域 = 写新的规则集 = 维护噩梦
- 规则之间互相冲突时，调试地狱
- 规则是静态的，无法从错误中学习

**Clawra 的答案：** 让 AI 自己发现规则、自己验证规则、自己更新规则。

```
你输入: "燃气调压箱出口压力不得超过 0.4MPa，超压有爆炸风险"
         ↓
Clawra 自动学习:
  ✓ 提取实体: 调压箱、出口压力、0.4MPa、爆炸风险
  ✓ 提取约束: pressure ≤ 0.4MPa
  ✓ 提取风险等级: HIGH
  ✓ 注册为硬性规则进入推理引擎
  ✓ 生成反向推理链用于验证
         ↓
  LLM 建议: pressure = 0.8MPa → Clawra 拦截 → 🚫 FAIL
  LLM 建议: pressure = 0.35MPa → Clawra 通过 → ✅ OK
```

这就是**神经符号融合** — LLM 的语义理解 + 符号逻辑的精确推理。

---

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────┐
│              Meta Learner (元学习层)                      │
│         学习如何学习 · 从错误中进化 · 策略自适应              │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
┌─────────────┐  ┌──────────────┐  ┌────────────────┐
│ Unified     │  │ Rule         │  │ Self           │
│ Logic Layer │  │ Discovery    │  │ Evaluator      │
│ 统一逻辑层    │  │ 规则发现引擎   │  │ 自我评估器      │
├─────────────┤  ├──────────────┤  ├────────────────┤
│ • Rule      │  │ • 从文本抽取  │  │ • 学习质量评估  │
│ • Behavior  │  │ • 归纳学习    │  │ • 反馈优化     │
│ • Policy    │  │ • 冲突检测    │  │ • 漂移检测     │
│ • Constraint│  │ • 版本控制    │  │ • 规则修订     │
└──────┬──────┘  └───────┬──────┘  └───────┬────────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
┌─────────────┐  ┌──────────────┐  ┌────────────────┐
│  Reasoner   │  │    Memory    │  │  Perception    │
│  推理引擎     │  │  记忆系统     │  │  感知提取层     │
├─────────────┤  ├──────────────┤  ├────────────────┤
│ • 前向链     │  │ • Neo4j 图谱 │  │ • LLM 知识抽取  │
│ • 后向链     │  │ • ChromaDB   │  │ • 实体识别     │
│ • 混合推理    │  │ • 时序记忆    │  │ • 关系抽取     │
│ • 置信度传播 │  │              │  │                │
└─────────────┘  └──────────────┘  └────────────────┘
```

**进化闭环（8 阶段）：**

```
感知 → 学习 → 推理 → 执行 → 评估 → 漂移检测 → 规则修订 → 知识更新
 ↑__________________________________________________|
                        (从错误中学习)
```

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🧠 **自主规则学习** | 从自然语言文本/案例中自动提取规则，无需手写 |
| 🔄 **进化闭环** | 8 阶段持续学习：感知→学习→推理→执行→评估→漂移检测→修订→更新 |
| 🔍 **GraphRAG** | 向量+图谱双通道检索，上下文质量显著优于纯 RAG |
| 🛡️ **SafeMath 沙盒** | AST 级数学沙盒，阻断 LLM 产生的指数级 DoS 攻击 |
| 📊 **Pattern 版本控制** | 规则/策略版本历史 + diff 对比 + 一键回滚 |
| 🧩 **Leiden 社区检测** | 保证连接性的精确社区划分，用于全局推理 |
| 🔀 **规则去重合并** | 向量相似度检测冗余规则，自动合并 |
| ⚡ **异步 ReAct** | 纯异步非阻塞编排，毫秒级并发响应 |
| 🚀 **Skill 可执行性** | SafeExecutor 沙盒执行，支持 `execute(params)` 调用 |

---

## 📂 项目结构

```
clawra-engine/
├── src/
│   ├── clawra.py                 # 核心入口
│   ├── agents/                   # Agent 编排层
│   │   ├── orchestrator.py       # ReAct 异步编排器
│   │   └── metacognition.py      # 元认知监控
│   ├── core/
│   │   ├── reasoner.py           # 神经符号推理引擎
│   │   ├── retriever.py          # GraphRAG 检索器
│   │   ├── rule_engine.py        # AST 规则引擎
│   │   └── lineage.py            # 血缘追踪
│   ├── evolution/                # ⭐ 自主进化层
│   │   ├── evolution_loop.py     # 8 阶段进化闭环
│   │   ├── unified_logic.py      # 统一逻辑表达层
│   │   ├── meta_learner.py       # 元学习器
│   │   ├── rule_discovery.py     # 规则发现引擎
│   │   └── skill_library.py      # 可执行技能库
│   ├── memory/                    # 记忆系统
│   │   ├── neo4j_adapter.py      # Neo4j 图谱存储
│   │   ├── vector_adapter.py     # ChromaDB 向量存储
│   │   └── episodic_enhanced.py  # 情节记忆
│   └── perception/               # 感知层
│       └── extractor.py          # LLM 知识抽取
├── examples/                      # 10 个完整可运行示例
│   ├── demo_basic.py             # 入门（离线可跑）
│   ├── demo_graphrag.py          # GraphRAG 演示
│   ├── demo_leiden_community.py  # 社区检测演示
│   ├── demo_pattern_versioning.py # 版本控制演示
│   ├── demo_evolution_loop.py    # 进化闭环演示
│   ├── demo_clawra_e2e.py        # 端到端演示
│   └── web_demo.py               # Streamlit Web 界面
├── tests/                         # 433 个测试（覆盖率导向）
└── docs/                          # 完整文档
```

---

## 🌟 为什么值得给 Star？

如果你认同以下任意一点，这个项目值得你的 ⭐：

**🔓 不想再写硬编码规则**
每个新领域都要从头写 if-else？Clawra 从文本/案例中自动学习规则，你只需关注业务逻辑本身。

**🛡️ 需要企业级 LLM 安全防护**
LLM 会产生数值幻觉（推荐 pressure = 0.8MPa），Clawra 用符号逻辑双重拦截，永远不会执行危险操作。

**📈 希望 AI 从生产环境持续进化**
Clawra 的 8 阶段进化闭环让 AI 自动从错误中学习，无需人工干预。

**🧠 对神经符号 AI 感兴趣**
"大模型语义理解 + 符号逻辑精确推理" — 不是噱头，是真实架构。

**⚡ 需要高性能异步 Agent**
纯 `async/await` 非阻塞架构，支持毫秒级并发，不被 LangChain 的同步逻辑绑架。

---

## 🗺️ 路线图

### ✅ 已完成
- [x] 自主进化架构（零硬编码规则学习）
- [x] 元学习器 + 规则发现引擎
- [x] 统一逻辑表达层（Rule/Behavior/Policy/Constraint）
- [x] GraphRAG 混合检索
- [x] SafeMath AST 沙盒
- [x] 规则版本控制 + diff + Rollback
- [x] Leiden 社区检测
- [x] 置信度推理网络
- [x] 10 个可运行示例（含 Web 界面）
- [x] 433 个测试

### 🚧 进行中
- [ ] Claude Code 集成
- [ ] LangChain 适配层
- [ ] 多模态知识抽取（图→规则）

### 📋 规划
- [ ] 强化学习策略优化
- [ ] 可视化规则编辑器
- [ ] 多 Agent 协作进化
- [ ] 插件市场

---

## 👥 贡献

欢迎提交 Issue 和 PR！请先阅读 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) 和 [docs/TESTING_STRATEGY.md](docs/TESTING_STRATEGY.md)。

[![Star Us](https://img.shields.io/badge/⭐_Star_This_Repo-Time_to_build_something_amazing!-blue?logo=github)](https://github.com/wu-xiaochen/clawra-engine/stargazers)

---

## 📖 文档

| 文档 | 说明 |
|------|------|
| [QUICKSTART.md](docs/QUICKSTART.md) | 5 分钟上手指南 |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | 系统架构详解 |
| [EVOLUTION_LOOP.md](docs/EVOLUTION_LOOP.md) | 进化闭环设计 |
| [SDK_GUIDE.md](docs/SDK_GUIDE.md) | SDK 使用指南 |
| [CHANGELOG.md](docs/CHANGELOG.md) | 版本变更记录 |

---

<p align="center">
  <strong>MIT License</strong> · Built with 🧠 by the Clawra community
</p>
