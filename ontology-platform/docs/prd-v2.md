# ontology-platform 产品需求文档 (V2.0 生产级)

**文档版本**: V2.0  
**创建日期**: 2026-03-16  
**状态**: 规划中  
**基于**: ontology-clawra v3.3

---

## 一、产品概述

### 1.1 产品背景

ontology-platform 是基于 ontology-clawra v3.3 构建的垂直领域可信AI推理引擎平台。产品核心价值在于：

- **消除AI幻觉**: 每步推理有据可查
- **可解释推理**: 透明推理过程，支持追溯
- **领域知识库**: 燃气工程、采购供应链、安全生产、金融风控
- **企业级可靠**: 可审计、可追溯、可扩展

### 1.2 产品定位

| 维度 | 定位 |
|------|------|
| 目标用户 | 企业决策者、领域专家、开发者 |
| 产品形态 | Web平台 + API服务 + CLI工具 |
| 部署方式 | 私有化部署 / SaaS |
| 核心能力 | 本体管理 + 推理引擎 + 知识图谱 |

### 1.3 核心功能架构

```
┌─────────────────────────────────────────────────────────────┐
│                      用户交互层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Web界面   │  │ REST API │  │GraphQL   │  │ CLI工具  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      推理服务层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ 推理引擎  │  │置信度评估│  │可解释输出│  │链式推理 │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      本体管理层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │OWL/RDF   │  │版本管理  │  │可视化编辑│  │校验合并 │  │
│  │导入导出  │  │          │  │          │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      知识图谱层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Neo4j   │  │ 图查询   │  │可视化    │  │统计分析 │  │
│  │ 图数据库 │  │          │  │          │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
├─────────────────────────────────────────────────────────────┤
│                      数据存储层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ 本体文件  │  │图数据库  │  │推理日志  │  │用户数据  │  │
│  │ (YAML)  │  │ (Neo4j)  │  │          │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、用户故事

### 2.1 主要用户角色

| 角色 | 职责 | 痛点 |
|------|------|------|
| **领域专家** | 构建和维护领域本体 | 缺乏可视化编辑工具，本体版本混乱 |
| **业务决策者** | 获取推理结论辅助决策 | 不信任AI结论，无法追溯推理过程 |
| **开发者** | 集成推理能力到业务系统 | API能力不足，缺乏灵活查询接口 |
| **平台管理员** | 管理平台运维和权限 | 缺乏审计和权限控制 |

### 2.2 用户故事列表

#### 故事1: 领域专家维护本体
> 作为领域专家，我需要导入现有的OWL本体文件，以便利用已有的知识积累。

#### 故事2: 本体版本管理
> 作为领域专家，我需要查看本体版本历史并回滚到旧版本，以便在出错时快速恢复。

#### 故事3: 推理结果可信度
> 作为业务决策者，我需要看到每个推理结论的置信度标注，以便判断结论是否可靠。

#### 故事4: 推理过程追溯
> 作为业务决策者，我需要追溯每步推理的依据，以便向领导解释决策来源。

#### 故事5: 假设确认流程
> 作为系统，我需要在推理依赖关键假设时暂停，向用户确认假设是否成立，再输出最终结论。

#### 故事6: 图谱可视化探索
> 作为领域专家，我需要通过可视化方式探索知识图谱，以便发现实体间隐藏的关系。

#### 故事7: 灵活查询本体
> 作为开发者，我需要通过GraphQL灵活查询本体数据，以便定制化获取所需信息。

#### 故事8: 导出推理报告
> 作为业务决策者，我需要导出推理报告（PDF/Markdown），以便存档和汇报。

---

## 三、功能需求

### 3.1 本体管理模块

#### 3.1.1 OWL/RDF本体导入导出

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| ONT-001 | 支持OWL格式本体文件导入 | P0 | 导入标准OWL文件不报错 |
| ONT-002 | 支持RDF/XML格式本体导入 | P0 | 导入RDF文件正确解析 |
| ONT-003 | 支持导出为OWL格式 | P0 | 导出后可重新导入且数据一致 |
| ONT-004 | 支持导出为RDF格式 | P0 | 导出后语义保持一致 |
| ONT-005 | 支持YAML/JSON格式互转 | P0 | 与现有系统兼容 |

#### 3.1.2 本体版本管理

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| ONT-006 | 本体版本自动记录 | P0 | 每次修改自动创建版本 |
| ONT-007 | 版本历史查看 | P0 | 查看所有历史版本列表 |
| ONT-008 | 版本回滚 | P0 | 回滚到指定版本 |
| ONT-009 | 版本对比 | P1 | 显示两个版本的差异 |
| ONT-010 | 版本分支 | P1 | 支持创建分支并行开发 |

#### 3.1.3 本体可视化编辑

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| ONT-011 | 实体关系图可视化 | P0 | Web界面展示本体图谱 |
| ONT-012 | 实体CRUD操作 | P0 | 可视化创建/编辑/删除实体 |
| ONT-013 | 关系连线操作 | P0 | 可视化创建实体间关系 |
| ONT-014 | 本体树形结构展示 | P1 | 层级视图展示分类关系 |
| ONT-015 | 批量导入 | P1 | 支持CSV/Excel批量导入实体 |

#### 3.1.4 本体校验与合并

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| ONT-016 | OWL完整性检查 | P0 | 检查必需属性是否完备 |
| ONT-017 | 一致性验证 | P0 | 检测逻辑矛盾 |
| ONT-018 | 多源本体合并 | P1 | 合并两个本体并处理冲突 |
| ONT-019 | 重复实体检测 | P1 | 识别并标记重复实体 |

### 3.2 推理引擎服务

#### 3.2.1 RESTful API设计

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| REA-001 | 推理查询接口 | P0 | POST /api/v1/reason 返回推理结果 |
| REA-002 | 置信度获取 | P0 | 返回置信度标注 |
| REA-003 | 推理链获取 | P0 | 返回完整推理链路 |
| REA-004 | 本体查询接口 | P0 | GET /api/v1/ontology 查询本体 |
| REA-005 | 批量推理 | P1 | 批量提交多个推理任务 |

#### 3.2.2 GraphQL查询接口

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| REA-006 | GraphQL端点 | P0 | POST /graphql 支持GraphQL查询 |
| REA-007 | 实体查询 | P0 | query { entities {...} } |
| REA-008 | 关系查询 | P0 | query { relations {...} } |
| REA-009 | 推理结果查询 | P0 | query { reasoning {...} } |
| REA-010 | 订阅推理事件 | P1 | 支持实时推理进度推送 |

#### 3.2.3 推理结果可解释性输出

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| REA-011 | 推理依据展示 | P0 | 每步展示匹配规则ID和内容 |
| REA-012 | 置信度标注 | P0 | CONFIRMED/ASSUMED/SPECULATIVE/UNKNOWN |
| REA-013 | 假设声明 | P0 | 明确标注哪些是假设 |
| REA-014 | 推理步骤可视化 | P0 | 图形化展示推理链路 |
| REA-015 | 推理报告生成 | P1 | 生成PDF/Markdown推理报告 |

#### 3.2.4 高级推理能力

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| REA-016 | 链式推理 | P1 | 支持多步推理链 |
| REA-017 | 反向推理 | P1 | 从结论反向推导条件 |
| REA-018 | 推理缓存 | P1 | 相同条件推理结果缓存 |
| REA-019 | 并行推理 | P1 | 多推理任务并行处理 |

### 3.3 知识图谱模块

#### 3.3.1 Neo4j图数据库集成

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| KG-001 | Neo4j连接 | P0 | 成功连接Neo4j并执行查询 |
| KG-002 | 实体同步 | P0 | 本体实体同步到Neo4j |
| KG-003 | 关系同步 | P0 | 本体关系同步到Neo4j |
| KG-004 | 增量更新 | P0 | 实时同步增量变化 |
| KG-005 | 数据备份 | P1 | 图数据库定期备份 |

#### 3.3.2 图可视化查询

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| KG-006 | 图谱可视化 | P0 | Web界面展示知识图谱 |
| KG-007 | 节点搜索 | P0 | 按名称/类型搜索实体 |
| KG-008 | 关系探索 | P0 | 点击节点显示关联关系 |
| KG-009 | 路径查询 | P1 | 查询两实体间最短路径 |
| KG-010 | 子图导出 | P1 | 导出选中子图 |

#### 3.3.3 实体关系管理

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| KG-011 | 实体CRUD | P0 | 通过API管理实体 |
| KG-012 | 关系CRUD | P0 | 通过API管理关系 |
| KG-013 | 批量操作 | P1 | 批量创建/更新/删除 |
| KG-014 | 导入导出 | P1 | CSV/JSON格式导入导出 |

#### 3.3.4 图谱统计分析

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| KG-015 | 实体统计 | P1 | 实体类型分布、数量统计 |
| KG-016 | 关系统计 | P1 | 关系类型分布、密度分析 |
| KG-017 | 图谱健康度 | P1 | 孤立节点、环路检测 |

### 3.4 用户交互

#### 3.4.1 置信度标注展示

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| UI-001 | 置信度标签 | P0 | 清晰展示四种置信度 |
| UI-002 | 置信度筛选 | P0 | 按置信度筛选结论 |
| UI-003 | 置信度颜色 | P0 | 绿/黄/红/灰颜色区分 |
| UI-004 | 置信度说明 | P0 | 悬停显示置信度含义 |

#### 3.4.2 假设声明与确认流程

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| UI-005 | 假设高亮 | P0 | 明确标识假设内容 |
| UI-006 | 确认弹窗 | P0 | 关键假设弹出确认 |
| UI-007 | 假设库 | P1 | 管理常用假设模板 |
| UI-008 | 假设历史 | P1 | 查看历史假设确认记录 |

#### 3.4.3 推理过程追溯

| 功能ID | 功能描述 | 优先级 | 验收标准 |
|--------|----------|--------|----------|
| UI-009 | 推理链展示 | P0 | 可视化展示推理步骤 |
| UI-010 | 步骤详情 | P0 | 点击查看每步详情 |
| UI-011 | 规则来源 | P0 | 展示匹配的规则ID和内容 |
| UI-012 | 回溯导航 | P0 | 支持跳转到任意步骤 |
| UI-013 | 导出推理链 | P1 | 导出推理链为图片/PDF |

---

## 四、非功能需求

### 4.1 性能需求

| 指标 | 目标值 | 说明 |
|------|--------|------|
| API响应时间 | < 500ms | 推理API P99响应时间 |
| 图查询响应 | < 500ms | 复杂查询P99响应时间 |
| 并发支持 | ≥ 100用户 | 正常负载 |
| 本体加载 | < 5秒 | 10万实体加载时间 |
| 图谱渲染 | < 2秒 | 千级节点渲染时间 |

### 4.2 可用性需求

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 系统可用性 | ≥ 99.5% | 月度可用性 |
| 故障恢复 | < 30分钟 | MTTR |
| 数据备份 | 每日 | 增量备份 |
| 监控告警 | 7x24 | 关键指标监控 |

### 4.3 安全需求

| 指标 | 要求 |
|------|------|
| 认证 | 支持API Key / OAuth2 |
| 权限 | RBAC角色权限控制 |
| 审计 | 记录所有操作日志 |
| 加密 | 敏感数据传输TLS加密 |

### 4.4 可扩展性需求

| 指标 | 要求 |
|------|------|
| 水平扩展 | 支持K8s自动扩缩容 |
| 存储扩展 | 支持分库分表 |
| 插件化 | 支持自定义推理引擎 |

---

## 五、技术架构

### 5.1 技术栈

| 层级 | 技术选型 |
|------|----------|
| 前端 | React + Ant Design + D3.js |
| 后端 | Python FastAPI + GraphQL (Strawberry) |
| 图数据库 | Neo4j |
| 本体存储 | RDFLib / OWL-RL |
| 消息队列 | Redis (缓存) |
| 部署 | Docker + K8s |

### 5.2 API设计

#### RESTful API

```
GET    /api/v1/ontologies              # 获取本体列表
POST   /api/v1/ontologies              # 创建本体
GET    /api/v1/ontologies/{id}        # 获取本体详情
PUT    /api/v1/ontologies/{id}        # 更新本体
DELETE /api/v1/ontologies/{id}        # 删除本体
POST   /api/v1/ontologies/import      # 导入本体(OWL/RDF)
GET    /api/v1/ontologies/{id}/export # 导出本体

GET    /api/v1/entities               # 获取实体列表
POST   /api/v1/entities               # 创建实体
GET    /api/v1/entities/{id}          # 获取实体详情
PUT    /api/v1/entities/{id}          # 更新实体
DELETE /api/v1/entities/{id}          # 删除实体

GET    /api/v1/relations              # 获取关系列表
POST   /api/v1/relations              # 创建关系

POST   /api/v1/reason                 # 推理查询
GET    /api/v1/reason/{id}           # 获取推理结果
GET    /api/v1/reason/{id}/chain     # 获取推理链

GET    /api/v1/graph                  # 图谱查询
GET    /api/v1/graph/stats            # 图谱统计
```

#### GraphQL Schema (核心)

```graphql
type Entity {
  id: ID!
  name: String!
  type: String!
  properties: JSON
  confidence: Confidence
  createdAt: DateTime
  updatedAt: DateTime
}

type Relation {
  id: ID!
  source: Entity!
  target: Entity!
  type: String!
  properties: JSON
}

type ReasoningStep {
  step: Int!
  input: String!
  rule: Rule
  conclusion: String!
  confidence: Confidence!
  evidence: [String!]
}

type ReasoningResult {
  id: ID!
  query: String!
  steps: [ReasoningStep!]!
  finalConclusion: String!
  confidence: Confidence!
  timestamp: DateTime!
}

enum Confidence {
  CONFIRMED
  ASSUMED
  SPECULATIVE
  UNKNOWN
}

type Query {
  entities(type: String, limit: Int): [Entity!]!
  entity(id: ID!): Entity
  relations(sourceId: ID, targetId: ID): [Relation!]!
  reasoning(id: ID!): ReasoningResult
  search(query: String!): [Entity!]!
  graph(limit: Int): [Entity!]!
}

type Mutation {
  createEntity(input: EntityInput!): Entity!
  updateEntity(id: ID!, input: EntityInput!): Entity!
  deleteEntity(id: ID!): Boolean!
  
  createRelation(input: RelationInput!): Relation!
  deleteRelation(id: ID!): Boolean!
  
  reason(query: String!, context: JSON): ReasoningResult!
}
```

---

## 六、数据模型

### 6.1 本体模型

```yaml
# 本体
Ontology:
  id: UUID
  name: String
  version: String
  format: Enum[OWL, RDF, YAML, JSON]
  content: Text
  created_by: User
  created_at: DateTime
  updated_at: DateTime

# 实体
Entity:
  id: UUID
  ontology_id: UUID
  name: String
  type: String (Person/Concept/Law/Rule/Task...)
  properties: JSON
  confidence: Enum[CONFIRMED, ASSUMED, SPECULATIVE, UNKNOWN]
  source: String
  created_at: DateTime
  updated_at: DateTime

# 关系
Relation:
  id: UUID
  ontology_id: UUID
  source_id: UUID (Entity)
  target_id: UUID (Entity)
  type: String (is_a/has_rule/triggers...)
  properties: JSON
  confidence: Float
  created_at: DateTime
```

### 6.2 推理模型

```yaml
# 推理结果
Reasoning:
  id: UUID
  query: String
  context: JSON
  steps: [ReasoningStep]
  conclusion: String
  confidence: Enum[CONFIRMED, ASSUMED, SPECULATIVE, UNKNOWN]
  execution_time: Int (ms)
  created_at: DateTime

# 推理步骤
ReasoningStep:
  step: Int
  input: String
  rule_id: UUID (可选)
  rule_content: String (可选)
  conclusion: String
  confidence: Enum
  is_assumption: Boolean
  needs_confirmation: Boolean

# 规则
Rule:
  id: UUID
  name: String
  condition: String
  action: String
  weight: Float
  source: String
  confidence: Enum
  enabled: Boolean
```

---

## 七、验收标准

### 7.1 本体管理模块

| 验收项 | 验收条件 |
|--------|----------|
| OWL导入 | 导入标准OWL文件，实体和关系正确解析 |
| RDF导入 | 导入RDF/XML文件，数据完整 |
| 版本管理 | 修改本体后自动创建版本，可回滚 |
| 可视化编辑 | Web界面创建实体和关系，数据正确保存 |

### 7.2 推理引擎服务

| 验收项 | 验收条件 |
|--------|----------|
| RESTful API | 所有端点正常响应，状态码正确 |
| GraphQL | 支持查询实体、关系、推理结果 |
| 置信度标注 | 推理结果包含四种置信度标注 |
| 推理链 | 返回完整推理步骤，每步有规则依据 |

### 7.3 知识图谱模块

| 验收项 | 验收条件 |
|--------|----------|
| Neo4j集成 | 本体变更实时同步到Neo4j |
| 图可视化 | Web界面展示知识图谱，支持缩放拖拽 |
| 图查询 | 支持按类型/名称搜索，支持路径查询 |

### 7.4 用户交互

| 验收项 | 验收条件 |
|--------|----------|
| 置信度展示 | 四种置信度用不同颜色标注 |
| 假设确认 | 关键假设暂停推理，弹出确认框 |
| 推理追溯 | 可视化展示推理链，支持点击查看详情 |

---

## 八、交付计划

### 8.1 迭代规划

| 迭代 | 时间 | 交付内容 |
|------|------|----------|
| Sprint 1 | 1-2周 | 项目初始化、基础框架搭建 |
| Sprint 2 | 3-4周 | OWL/RDF解析器、基础本体加载 |
| Sprint 3 | 5-6周 | 本体版本管理、RESTful API |
| Sprint 4 | 7-8周 | Neo4j集成、图查询API |
| Sprint 5 | 9-10周 | GraphQL API、推理可解释性 |
| Sprint 6 | 11-12周 | Web界面、测试优化 |
| Sprint 7 | 13-14周 | 完整功能集成、文档 |
| Sprint 8 | 15-16周 | Beta测试、Bug修复 |

### 8.2 里程碑

| 里程碑 | 计划日期 | 交付内容 |
|--------|----------|----------|
| M1 - 基础框架 | 第2周 | 项目架构、技术选型 |
| M2 - 本体管理 | 第4周 | OWL/RDF导入导出、版本管理 |
| M3 - 图数据库 | 第6周 | Neo4j集成、图查询 |
| M4 - 推理引擎 | 第8周 | RESTful + GraphQL API |
| M5 - 可解释性 | 第10周 | 推理过程追溯、置信度展示 |
| M6 - Web界面 | 第12周 | 本体编辑、图谱可视化 |
| M7 - Beta | 第14周 | Beta版本、测试反馈 |
| **V2.0 发布** | **第16周** | **正式版本发布** |

---

## 九、风险分析

### 9.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| OWL解析复杂度 | 高 | 调研成熟库(RDFLib)，预留缓冲时间 |
| Neo4j性能 | 中 | 预先性能测试，优化查询 |
| GraphQL复杂性 | 中 | 使用成熟框架(Strawberry) |

### 9.2 产品风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 用户对可解释性接受度 | 中 | 收集早期用户反馈 |
| 本体构建门槛 | 中 | 提供模板和示例 |

---

## 十、附录

### 10.1 参考文档

- ontology-clawra SKILL.md (v3.3)
- 技术架构文档 (cto/architecture.md)
- API接口文档

### 10.2 术语表

| 术语 | 定义 |
|------|------|
| OWL | Web Ontology Language，网络本体语言 |
| RDF | Resource Description Framework，资源描述框架 |
| 本体 | 领域概念模型及其关系 |
| 置信度 | 推理结论的可信程度 |
| 推理链 | 从输入到结论的推理步骤序列 |

---

**文档版本**: V2.0  
**创建日期**: 2026-03-16  
**最后更新**: 2026-03-16  
**状态**: 已完成
