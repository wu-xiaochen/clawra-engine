# ontology-platform

**The first agent framework with a built-in bullshit detector.**

[![PyPI Version](https://img.shields.io/pypi/v/ontology-platform?color=blue)](https://pypi.org/project/ontology-platform/)
[![5-Minute Quickstart](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wu-xiaochen/ontology-platform/blob/main/ontology_platform_quickstart.ipynb)

---

## 🎯 The Problem

Your AI agent is hallucinating. **And it doesn't even know it.**

Traditional frameworks (LangChain, Mem0, RAG) give your agent memory, but not judgment. They retrieve information and generate confident-sounding answers—even when they're completely wrong.




Traditional Agent:
Q: "Should we trust Supplier_C?"
A: "Yes, they have a good track record."  ← Hallucinated. Actually has 40% defect rate.
Confidence: Unknown (LLM just sounds confident)

---
## 💡 The Solution
**ontology-platform** is the only agent framework with **metacognition**—it knows what it knows, and more importantly, what it *doesn't* know.


python
from ontology import Agent

agent = Agent()

result = agent.ask("Should we trust Supplier_C?")

print(f"Verdict: {result.conclusion}")
→ "HIGH_RISK: Do not proceed without backup supplier"
print(f"Confidence: {result.confidence:.2f}")
→ 0.89 (CONFIRMED)
print(f"Reasoning:")
for step in result.reasoning_chain:
print(f"  • {step}")
→ • on_time_rate = 0.72 < 0.85 threshold

→ • quality_score = 0.61 < 0.80 threshold
→ • Rule "combined_risk" triggered
When the agent is uncertain, **it tells you**:


python
result = agent.ask("What's the quantum computing outlook for 2027?")

print(f"Confidence: {result.confidence:.2f}")
→ 0.43 (SPECULATIVE)
print(f"Agent says: {result.verdict}")
→ "I don't have enough reliable information. Consult domain expert."
---
## ⚡ Quick Start
**Try it now (5 minutes):** [Open in Colab](https://colab.research.google.com/github/wu-xiaochen/ontology-platform/blob/main/ontology_platform_quickstart.ipynb)
### Installation


bash
pip install ontology-platform

### Hello World


python
from ontology import Agent

agent = Agent()
Teach the agent something
agent.learn({
"type": "Supplier",
"id": "SUP001",
"properties": {
"name": "Acme Components",
"on_time_rate": 0.91,
"quality_score": 0.88
}
})
Add reasoning rules
agent.add_rule({
"id": "quality_threshold",
"condition": "quality_score < 0.80",
"conclusion": "Supplier poses quality risk",
"confidence": 0.9
})
Ask questions
result = agent.ask("Is SUP001 safe to use?")
print(result)

---
## 🔥 Why It's Different
| Capability | LangChain | Mem0 | Traditional RAG | **ontology-platform** |
|------------|-----------|------|-----------------|----------------------|
| Memory persistence | ❌ | ✅ | ✅ | ✅ |
| Structured knowledge | ❌ | ❌ | ❌ | ✅ |
| **Causal reasoning** | ❌ | ❌ | ❌ | ✅ |
| **Confidence scoring** | ❌ | ❌ | ❌ | ✅ |
| **Reasoning trace** | ❌ | ❌ | ❌ | ✅ |
| **Knows when uncertain** | ❌ | ❌ | ❌ | ✅ |
| Runtime learning | ❌ | ❌ | ❌ | ✅ |
**The bottom line:** Other frameworks help your agent *remember*. We help it *think*.
---
## 🎭 Real-World Examples
### 1. AI Hiring Assistant


python
agent.ask("Should we hire this candidate?")
→ Confidence: 0.76 (ASSUMED)

→ "Recommendation: Proceed, but check 2 more references"
→ Reasoning: Strong technical skills, but limited leadership evidence
### 2. Medical Second Opinion


python
回复 吴晓辰: 
你说的 这几个文件/tmp/ontology-platform目录在我本地吗 我没找到
agent.ask("Could these symptoms indicate diabetes?")
→ Confidence: 0.58 (SPECULATIVE)

→ "Possible, but insufficient data. Recommend medical consultation."
→ Knowledge gaps: Blood test results, family history, BMI
### 3. Investment Risk Analysis


python
agent.ask("Is $TSLA a buy at current price?")
→ Confidence: 0.45 (SPECULATIVE)

→ "Too many unknown variables. Consult financial advisor."
→ Uncertainty sources: Market volatility, earnings report pending
---
## 📚 Documentation
- **[Quickstart Guide](docs/quickstart.md)** - Get started in 5 minutes
- **[API Reference](docs/api.md)** - Full API documentation
- **[Architecture](docs/architecture.md)** - How it works under the hood
- **[Examples](examples/)** - Real-world use cases
---
## 🤝 Contributing
We welcome contributors! Here's how to help:


bash
git clone https://github.com/wu-xiaochen/ontology-platform.git
cd ontology-platform
pip install -e ".[dev]"
PYTHONPATH=src python examples/demo_supplier_monitor.py

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
---
## 💬 Community
- **Discussions:** [GitHub Discussions](https://github.com/wu-xiaochen/ontology-platform/discussions)
- **Issues:** [Report bugs or request features](https://github.com/wu-xiaochen/ontology-platform/issues)
- **Twitter:** [@ontology_platform](https://twitter.com/ontology_platform) (coming soon)
---
## 📄 License
MIT License - See [LICENSE](LICENSE) file.
---
## 🙏 Acknowledgments
Built with inspiration from:
- OWL/RDF semantic web standards
- Judea Pearl's causal inference work
- The open-source AI community
---
**Ready to build agents that think before they speak?**
[Get Started →](docs/quickstart.md)

---

## 🆕 最新优化（2026-03）

### 短期优化
- ✅ 统一包入口：`src/ontology_platform/` 
- ✅ 分层上下文分块：`src/chunking/` 模块
- ✅ OWL 语义增强：增加 OWA 说明文档 (`OWL_ SEMANTICS. md`)

### 中期优化
- ✅ Docker 一键部署：`Dockerfile` + `docker-compose. yml`
- ✅ GitHub Actions 本体校验：`.github/workflows/ontology-validate. yml`

### 长期优化
- ✅ Agent 记忆治理模块：`src/memory/` - 实现语义漂移检测与目标稳定性校验

### 使用示例

```python
# 1. 使用分层分块处理长文档
from ontology_platform.chunking import HierarchicalChunker

chunker = HierarchicalChunker(max_tokens=4096)
chunks = chunker.chunk(long_document)

# 2. 使用记忆治理检测语义漂移
from ontology_platform.memory import MemoryGovernance

gov = MemoryGovernance(agent_ontology)
health = gov.check_health()
print(f"Health: {health.overall_score}")
```

### 容器化部署

```bash
# 一键启动所有服务
docker-compose up -d

# 访问 API
curl http://localhost:8000/health
```
