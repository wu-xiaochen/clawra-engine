# 🧠 Clawra Engine

> **Let AI truly learn rules on its own — not you writing them for it.**
> Meta-Learning × Knowledge Graph × Neurosymbolic Fusion — Autonomous Evolving Agent Cognitive Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/wu-xiaochen/clawra-engine/blob/main/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-433%20%25%20passing-brightgreen)](https://github.com/wu-xiaochen/clawra-engine/actions)
[![GitHub Stars](https://img.shields.io/github/stars/wu-xiaochen/clawra-engine?style=social)](https://github.com/wu-xiaochen/clawra-engine/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/wu-xiaochen/clawra-engine?style=social)](https://github.com/wu-xiaochen/clawra-engine/network)

---

## ⚡ 5-Minute Quick Start (No API Key needed, offline demo works)

```bash
git clone https://github.com/wu-xiaochen/clawra-engine.git
cd clawra-engine
pip install -e .                    # Install (all dependencies included)
python examples/demo_basic.py        # Run! ← **No config needed, results immediately**
```

---

### 🔥 demo_basic.py Output

```
============================================================
🤖 Clawra Autonomous Evolution Agent — Basic Demo
============================================================

[Step 1] Initialize Clawra (no memory layer)...
  ✓ Clawra initialization complete

[Step 2] Learn knowledge from text...
  ✓ Learning complete: success=True
    - Auto-generated facts: 1
    - Learned patterns: ['learned:llm_entity:gas_equipment:ep_xxx:0']

[Step 3] Manually add fact triples...
  ✓ Added 4 fact triples

[Step 4] Execute forward chaining reasoning...
  ✓ Reasoning complete, discovered 2 conclusions (transitivity rules)
    → PressureRegulatorA is_a Concept (confidence 0.99)
    → PressureRegulatorA is_a Key Equipment in Urban Gas Distribution (confidence 0.99)

[Step 5] Query learned patterns...
  ✓ Found 1 relevant pattern

[Step 6] GraphRAG knowledge retrieval...
  ✓ Retrieved 5 related knowledge items

[Step 7] System statistics...
  ✓ Total facts: 10 | Entities: 13 | Patterns: 3

✅ demo_basic.py complete!
```

**10 complete examples, all runnable:**

```bash
python examples/demo_basic.py                 # Basic demo (offline works)
python examples/demo_graphrag.py              # GraphRAG retrieval
python examples/demo_leiden_community.py       # Leiden community detection
python examples/demo_pattern_versioning.py     # Pattern version control
python examples/demo_confidence_reasoning.py   # Confidence reasoning
python examples/demo_case_based_reasoner.py    # Case-based reasoning
python examples/demo_evolution_loop.py         # Evolution loop
python examples/demo_supplier_monitor.py       # Supplier monitoring Agent
python examples/demo_clawra_e2e.py             # E2E end-to-end
PYTHONPATH=. streamlit run examples/web_demo.py  # Web interface
```

> 💡 Examples with LLM (`learn()`, `evolution_loop`) require `MINIMAX_API_KEY`. Pure logic examples run fully offline.

---

## 🎯 What Is This?

**Clawra** is a neurosymbolic cognitive agent framework with **autonomous evolution capabilities**.

```
Traditional Agent:  You write 1000 if-else rules → AI can only follow your script
Clawra:             Give it text/cases/feedback → It learns rules and evolves on its own
```

---

## ⚔️ Core Capabilities vs Traditional Frameworks

| | LangChain / LangGraph | Clawra Engine |
|---|---|---|
| Rule Source | You write (hardcode) | **AI learns from text automatically** |
| Hallucination Protection | None | **Symbolic logic dual interception** |
| Computation Safety | None | **AST sandbox prevents DoS** |
| Knowledge Retrieval | Pure vector RAG | **GraphRAG hybrid retrieval** |
| Self-Evolution | Static | **8-stage evolution loop** |
| Architecture | Heavy (depends on LangChain) | **Lightweight built-in (no LangChain)** |

---

## 🧠 Core Philosophy: Zero Hardcoded Rules

Traditional Agent frameworks require developers to write massive rule sets to control AI behavior, but:

- Each new domain = write new rule set = maintenance nightmare
- When rules conflict with each other, debugging becomes hell
- Rules are static, unable to learn from mistakes

**Clawra's Answer:** Let AI discover rules, validate rules, and update rules on its own.

```
You input: "Gas pressure regulator outlet pressure must not exceed 0.4MPa, overpressure has explosion risk"
         ↓
Clawra automatically learns:
  ✓ Extracts entities: pressure regulator, outlet pressure, 0.4MPa, explosion risk
  ✓ Extracts constraint: pressure ≤ 0.4MPa
  ✓ Extracts risk level: HIGH
  ✓ Registers as hard rule in reasoning engine
  ✓ Generates reverse reasoning chain for validation
         ↓
  LLM suggests: pressure = 0.8MPa → Clawra intercepts → 🚫 FAIL
  LLM suggests: pressure = 0.35MPa → Clawra passes → ✅ OK
```

This is **Neurosymbolic Fusion** — LLM's semantic understanding + symbolic logic's precise reasoning.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Meta Learner                                │
│         Learn how to learn · Evolve from errors · Adaptive strategy │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
┌─────────────┐  ┌──────────────┐  ┌────────────────┐
│ Unified     │  │ Rule         │  │ Self           │
│ Logic Layer │  │ Discovery    │  │ Evaluator      │
├─────────────┤  ├──────────────┤  ├────────────────┤
│ • Rule      │  │ • Extract    │  │ • Learning     │
│ • Behavior  │  │   from text  │  │   quality      │
│ • Policy    │  │ • Inductive  │  │   evaluation   │
│ • Constraint│  │   learning   │  │ • Feedback     │
│             │  │ • Conflict   │  │   optimization │
│             │  │   detection  │  │ • Drift        │
│             │  │ • Version    │  │   detection   │
│             │  │   control    │  │ • Rule         │
│             │  │              │  │   revision    │
└──────┬──────┘  └───────┬──────┘  └───────┬────────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
┌─────────────┐  ┌──────────────┐  ┌────────────────┐
│  Reasoner   │  │    Memory    │  │  Perception    │
├─────────────┤  ├──────────────┤  ├────────────────┤
│ • Forward   │  │ • Neo4j      │  │ • LLM knowledge│
│   chaining  │  │   graph      │  │   extraction   │
│ • Backward  │  │ • ChromaDB   │  │ • Entity       │
│   chaining  │  │ • Temporal   │  │   recognition  │
│ • Hybrid    │  │   memory    │  │ • Relation     │
│   reasoning │  │              │  │   extraction   │
│ • Confidence│  │              │  │                │
│   propagation│  │              │  │                │
└─────────────┘  └──────────────┘  └────────────────┘
```

**Evolution Loop (8 Stages):**

```
Perception → Learning → Reasoning → Execution → Evaluation → Drift Detection → Rule Revision → Knowledge Update
 ↑__________________________________________________|
                        (Learn from errors)
```

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🧠 **Autonomous Rule Learning** | Automatically extract rules from natural language text/cases, no manual writing |
| 🔄 **Evolution Loop** | 8-stage continuous learning: perception → learning → reasoning → execution → evaluation → drift detection → revision → update |
| 🔍 **GraphRAG** | Vector + graph dual-channel retrieval, significantly better context quality than pure RAG |
| 🛡️ **SafeMath Sandbox** | AST-level math sandbox, blocks exponential DoS attacks from LLM generation |
| 📊 **Pattern Version Control** | Rule/strategy version history + diff comparison + one-click rollback |
| 🧩 **Leiden Community Detection** | Precise community detection with connectivity guarantee, for global reasoning |
| 🔀 **Rule Deduplication & Merge** | Vector similarity detection for redundant rules, automatic merging |
| ⚡ **Async ReAct** | Pure async non-blocking orchestration, millisecond-level concurrent response |
| 🚀 **Skill Executability** | SafeExecutor sandbox execution, supports `execute(params)` calls |

---

## 📂 Project Structure

```
clawra-engine/
├── src/
│   ├── clawra.py                 # Core entry point
│   ├── agents/                   # Agent orchestration layer
│   │   ├── orchestrator.py       # ReAct async orchestrator
│   │   └── metacognition.py      # Metacognition monitor
│   ├── core/
│   │   ├── reasoner.py           # Neurosymbolic reasoning engine
│   │   ├── retriever.py          # GraphRAG retriever
│   │   ├── rule_engine.py        # AST rule engine
│   │   └── lineage.py            # Lineage tracking
│   ├── evolution/                # ⭐ Autonomous evolution layer
│   │   ├── evolution_loop.py     # 8-stage evolution loop
│   │   ├── unified_logic.py      # Unified logic expression layer
│   │   ├── meta_learner.py       # Meta learner
│   │   ├── rule_discovery.py     # Rule discovery engine
│   │   └── skill_library.py      # Executable skill library
│   ├── memory/                    # Memory system
│   │   ├── neo4j_adapter.py      # Neo4j graph storage
│   │   ├── vector_adapter.py     # ChromaDB vector storage
│   │   └── episodic_enhanced.py  # Episodic memory
│   └── perception/               # Perception layer
│       └── extractor.py           # LLM knowledge extraction
├── examples/                      # 10 complete runnable examples
│   ├── demo_basic.py             # Getting started (offline works)
│   ├── demo_graphrag.py          # GraphRAG demo
│   ├── demo_leiden_community.py  # Community detection demo
│   ├── demo_pattern_versioning.py # Version control demo
│   ├── demo_evolution_loop.py     # Evolution loop demo
│   ├── demo_clawra_e2e.py         # E2E end-to-end demo
│   └── web_demo.py               # Streamlit Web interface
├── tests/                         # 433 tests (coverage-oriented)
└── docs/                          # Complete documentation
```

---

## 🌟 Why Star This Project?

If you agree with any of the following, this project deserves your ⭐:

**🔓 Don't want to write hardcoded rules anymore**
Need a new rule set for every new domain? Clawra learns rules automatically from text/cases, you just focus on business logic.

**🛡️ Need enterprise-grade LLM safety**
LLMs generate numerical hallucinations (recommending pressure = 0.8MPa). Clawra uses symbolic logic dual interception, never executes dangerous operations.

**📈 Want AI to continuously evolve from production**
Clawra's 8-stage evolution loop lets AI automatically learn from mistakes without human intervention.

**🧠 Interested in neurosymbolic AI**
"Large model semantic understanding + symbolic logic precise reasoning" — not a gimmick, a real architecture.

**⚡ Need high-performance async Agent**
Pure `async/await` non-blocking architecture, supports millisecond-level concurrency, not held back by LangChain's synchronous logic.

---

## 🗺️ Roadmap

### ✅ Completed
- [x] Autonomous evolution architecture (zero hardcoded rule learning)
- [x] Meta learner + rule discovery engine
- [x] Unified logic expression layer (Rule/Behavior/Policy/Constraint)
- [x] GraphRAG hybrid retrieval
- [x] SafeMath AST sandbox
- [x] Rule version control + diff + rollback
- [x] Leiden community detection
- [x] Confidence reasoning network
- [x] 10 runnable examples (with Web interface)
- [x] 433 tests

### 🚧 In Progress
- [ ] Claude Code integration
- [ ] LangChain adapter layer
- [ ] Multimodal knowledge extraction (image → rule)

### 📋 Planned
- [ ] Reinforcement learning strategy optimization
- [ ] Visual rule editor
- [ ] Multi-Agent collaborative evolution
- [ ] Plugin marketplace

---

## 👥 Contributing

Issues and PRs welcome! Please read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/TESTING_STRATEGY.md](docs/TESTING_STRATEGY.md) first.

[![Star Us](https://img.shields.io/badge/⭐_Star_This_Repo-Time_to_build_something_amazing!-blue?logo=github)](https://github.com/wu-xiaochen/clawra-engine/stargazers)

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](docs/QUICKSTART.md) | 5-minute getting started guide |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture details |
| [EVOLUTION_LOOP.md](docs/EVOLUTION_LOOP.md) | Evolution loop design |
| [SDK_GUIDE.md](docs/SDK_GUIDE.md) | SDK usage guide |
| [CHANGELOG.md](docs/CHANGELOG.md) | Version changelog |

---

<p align="center">
  <strong>MIT License</strong> · Built with 🧠 by the Clawra community
</p>
