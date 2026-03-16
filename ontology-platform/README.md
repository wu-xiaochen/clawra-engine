# ontology-platform

垂直领域可信AI推理引擎平台

## 核心特性

- 🔥 消除AI幻觉 - 每步推理有据可查
- ⚡ 可解释推理 - 透明推理过程
- 📚 领域知识库 - 燃气工程、采购供应链、安全生产、金融风控
- 🏢 企业级可靠 - 可审计、可追溯

## 已覆盖领域

- ✅ 燃气工程
- ✅ 采购供应链
- ✅ 安全生产
- ✅ 金融风控
- ⏳ 医疗健康

## 系统要求

- Python 3.11+
- Redis 6.0+ (可选，用于缓存)
- Neo4j 5.0+ (可选，用于图存储)

## 安装

### 1. 克隆项目

```bash
git clone https://github.com/wu-xiaochen/ontology-platform.git
cd ontology-platform
```

### 2. 创建虚拟环境（推荐）

```bash
# 使用 venv
python -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装可选依赖

```bash
# Neo4j 图数据库支持（可选）
pip install neo4j

# 向量搜索支持（可选）
pip install sentence-transformers faiss-cpu
```

## 配置

### 环境变量

创建 `.env` 文件：

```bash
# API 配置
API_HOST=0.0.0.0
API_PORT=8000

# Redis 配置（可选）
REDIS_HOST=localhost
REDIS_PORT=6379

# Neo4j 配置（可选）
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### 配置文件

编辑 `config.yaml`：

```yaml
api:
  host: "0.0.0.0"
  port: 8000

redis:
  enabled: true
  host: "localhost"
  port: 6379

neo4j:
  enabled: false
  uri: "bolt://localhost:7687"
  user: "neo4j"
  password: ""

ontology:
  base_uri: "http://example.org/"
  confidence_threshold: 0.7
```

## 快速开始

### 方式1：运行API服务

```bash
python src/api.py
```

或使用 uvicorn：

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### 方式2：运行示例

```bash
python examples/demo.py
```

### 方式3：使用CLI

```bash
python cli.py --help
```

## Docker 部署

### 构建镜像

```bash
docker build -t ontology-platform .
```

### 运行容器

```bash
docker run -d -p 8000:8000 \
  --env REDIS_HOST=redis \
  --env NEO4J_URI=bolt://neo4j:7687 \
  ontology-platform
```

### 使用 Docker Compose

```bash
docker-compose up -d
```

这将启动：
- ontology-platform API 服务
- Redis 缓存
- Neo4j 图数据库

## 核心模块

### RDF适配器 (`src/ontology/rdf_adapter.py`)

实现JSONL到RDF/OWL的转换：

```python
from ontology.rdf_adapter import RDFAdapter

adapter = RDFAdapter("http://example.org/")
adapter.load_jsonl("knowledge.jsonl")
adapter.save_turtle("knowledge.ttl")
```

### Neo4j客户端 (`src/ontology/neo4j_client.py`)

图数据库集成：

```python
from ontology.neo4j_client import Neo4jClient

client = Neo4jClient("bolt://localhost:7687", "neo4j", "password")
client.connect()
client.create_entity("Alice", "Person")
```

### 置信度传播

```python
# RDF内存模式
result = adapter.propagate_confidence("EntityA", max_depth=3)

# Neo4j模式
result = client.propagate_confidence("EntityA", max_depth=3)
```

## 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_ontology.py -v

# 运行特定测试
python -m pytest tests/test_ontology.py::TestRDFAdapter::test_confidence_propagation -v
```

## 文档

- [技术架构](cto/architecture.md)
- [产品路线图](pm/roadmap.md)
- [本体设计](domain_expert/ontology_design.md)
- [推理引擎](reasoner/engine_design.md)

## GitHub

https://github.com/wu-xiaochen/ontology-platform
