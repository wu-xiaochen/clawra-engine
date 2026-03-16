# 本体Ontology平台 - 技术规格文档

> **版本**: v1.0.0  
> **更新时间**: 2026-03-16  
> **状态**: 草稿

---

## 1. API规格 (OpenAPI/Swagger)

### 1.1 API版本控制

| 版本 | 路径前缀 | 状态 |
|------|----------|------|
| v1 | `/api/v1` | 当前活跃 |
| v2 | `/api/v2` | 开发中 |

### 1.2 通用头部

```yaml
headers:
  Content-Type: application/json
  Accept: application/json
  Authorization: Bearer <token>
  X-Request-ID: uuid-string
  X-Correlation-ID: uuid-string
```

### 1.3 核心API端点

#### 1.3.1 本体管理

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/ontologies` | 获取本体列表 |
| POST | `/api/v1/ontologies` | 创建本体 |
| GET | `/api/v1/ontologies/{id}` | 获取本体详情 |
| PUT | `/api/v1/ontologies/{id}` | 更新本体 |
| DELETE | `/api/v1/ontologies/{id}` | 删除本体 |

#### 1.3.2 实体管理

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/entities` | 获取实体列表 |
| POST | `/api/v1/entities` | 创建实体 |
| GET | `/api/v1/entities/{id}` | 获取实体详情 |
| PUT | `/api/v1/entities/{id}` | 更新实体 |
| DELETE | `/api/v1/entities/{id}` | 删除实体 |
| GET | `/api/v1/entities/{id}/history` | 获取实体变更历史 |

#### 1.3.3 关系管理

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/relations` | 获取关系列表 |
| POST | `/api/v1/relations` | 创建关系 |
| GET | `/api/v1/relations/{id}` | 获取关系详情 |
| DELETE | `/api/v1/relations/{id}` | 删除关系 |

#### 1.3.4 知识查询

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/query` | SPARQL查询接口 |
| POST | `/api/v1/query/explain` | 查询解释 |

#### 1.3.5 分类与标签

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/taxonomies` | 获取分类列表 |
| POST | `/api/v1/taxonomies` | 创建分类 |
| GET | `/api/v1/tags` | 获取标签列表 |
| POST | `/api/v1/tags` | 创建标签 |

### 1.4 API响应格式

**成功响应**:

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "requestId": "uuid",
    "timestamp": "2026-03-16T13:57:00Z",
    "page": 1,
    "pageSize": 20,
    "total": 100
  }
}
```

**分页参数**:

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| page | integer | 1 | 页码 |
| pageSize | integer | 20 | 每页数量 (最大100) |
| sortBy | string | createdAt | 排序字段 |
| sortOrder | string | desc | 排序方向 (asc/desc) |

---

## 2. 数据模型规格

### 2.1 本体 (Ontology)

```typescript
interface Ontology {
  id: string;                    // UUID
  name: string;                  // 本体名称 (必需, 1-100字符)
  version: string;               // 版本号 (语义化版本)
  description: string;          // 描述 (可选, 最大500字符)
  namespace: string;            // 命名空间 URI
  status: OntologyStatus;       // 状态: draft | active | deprecated
  schema: OntologySchema;       // 本体schema定义
  metadata: Metadata;           // 元数据
  createdAt: string;            // 创建时间 (ISO 8601)
  updatedAt: string;            // 更新时间
  createdBy: string;            // 创建者ID
}

enum OntologyStatus {
  DRAFT = "draft"
  ACTIVE = "active"
  DEPRECATED = "deprecated"
}

interface OntologySchema {
  classes: ClassDefinition[];   // 类定义列表
  properties: PropertyDefinition[];  // 属性定义列表
  restrictions: Restriction[];  // 约束定义
}

interface ClassDefinition {
  id: string;
  name: string;
  label: string;                // 显示名称
  description: string;
  parentClasses: string[];      // 父类ID列表
  properties: string[];         // 属性ID列表
}

interface PropertyDefinition {
  id: string;
  name: string;
  label: string;
  description: string;
  domain: string;               // 定义域 (类ID)
  range: string;               // 值域 (数据类型或类ID)
  propertyType: PropertyType;  // 属性类型
  cardinality: Cardinality;     // 基数约束
  isFunctional: boolean;        // 是否为函数属性
}

enum PropertyType {
  OBJECT = "object"             // 对象属性
  DATATYPE = "datatype"        // 数据类型属性
  ANNOTATION = "annotation"    // 注解属性
}

enum Cardinality {
  ONE = "1"                     // 恰好一个
  ZERO_OR_ONE = "0..1"          // 零或一个
  MANY = "*"                    // 任意数量
  ONE_OR_MANY = "1..*"          // 至少一个
}
```

### 2.2 实体 (Entity)

```typescript
interface Entity {
  id: string;                    // UUID
  ontologyId: string;           // 所属本体ID
  classId: string;              // 所属类ID
  identifier: string;           // 唯一标识符 (URI)
  properties: PropertyValue[];  // 属性值列表
  labels: MultiLangString;      // 多语言标签
  descriptions: MultiLangString; // 多语言描述
  externalIds: ExternalId[];    // 外部ID映射
  tags: string[];               // 标签列表
  taxonomyIds: string[];        // 分类ID列表
  metadata: Metadata;
  createdAt: string;
  updatedAt: string;
  createdBy: string;
}

interface PropertyValue {
  propertyId: string;
  value: any;
  language?: string;            // 语言标签
  datatype?: string;           // 数据类型
}

interface MultiLangString {
  [lang: string]: string;       // 语言代码 -> 文本
}

interface ExternalId {
  system: string;              // 外部系统标识
  id: string;                  // 外部系统中的ID
  url?: string;                 // 外部链接
}
```

### 2.3 关系 (Relation)

```typescript
interface Relation {
  id: string;
  ontologyId: string;
  relationType: string;         // 关系类型ID
  sourceEntityId: string;       // 源实体ID
  targetEntityId: string;      // 目标实体ID
  properties: PropertyValue[];  // 关系属性
  validFrom?: string;          // 生效开始时间
  validUntil?: string;          // 生效结束时间
  metadata: Metadata;
  createdAt: string;
  createdBy: string;
}
```

### 2.4 分类与标签

```typescript
interface Taxonomy {
  id: string;
  name: string;
  label: string;
  description: string;
  parentId?: string;            // 父分类ID
  ontologyId?: string;          // 关联本体 (可选)
  order: number;                // 排序序号
  metadata: Metadata;
}

interface Tag {
  id: string;
  name: string;
  color?: string;               // 颜色代码
  description?: string;
  metadata: Metadata;
}
```

### 2.5 元数据

```typescript
interface Metadata {
  createdAt: string;
  updatedAt: string;
  createdBy: string;
  modifiedBy?: string;
  version: number;              // 乐观锁版本号
  status?: string;
  customFields?: Record<string, any>;
}
```

---

## 3. 错误码定义

### 3.1 错误响应格式

```json
{
  "success": false,
  "error": {
    "code": "ERR_XXX",
    "message": "错误描述",
    "details": { ... },
    "requestId": "uuid"
  }
}
```

### 3.2 错误码分类

#### 3.2.1 客户端错误 (4xx)

| 错误码 | HTTP状态码 | 描述 | 解决方案 |
|--------|------------|------|----------|
| ERR_BAD_REQUEST | 400 | 请求参数错误 | 检查请求参数格式和必填项 |
| ERR_UNAUTHORIZED | 401 | 未认证 | 提供有效的认证令牌 |
| ERR_FORBIDDEN | 403 | 无权限 | 检查用户权限设置 |
| ERR_NOT_FOUND | 404 | 资源不存在 | 确认资源ID是否正确 |
| ERR_CONFLICT | 409 | 资源冲突 | 检查唯一性约束 |
| ERR_VALIDATION_FAILED | 422 | 数据验证失败 | 检查字段约束 |
| ERR_RATE_LIMITED | 429 | 请求频率超限 | 降低请求频率 |

#### 3.2.2 服务端错误 (5xx)

| 错误码 | HTTP状态码 | 描述 | 解决方案 |
|--------|------------|------|----------|
| ERR_INTERNAL | 500 | 内部服务器错误 | 联系技术支持 |
| ERR_NOT_IMPLEMENTED | 501 | 功能未实现 | 等待功能上线 |
| ERR_SERVICE_UNAVAILABLE | 503 | 服务不可用 | 稍后重试 |
| ERR_TIMEOUT | 504 | 服务超时 | 增加超时时间后重试 |

#### 3.2.3 业务错误 (6xx)

| 错误码 | HTTP状态码 | 描述 | 解决方案 |
|--------|------------|------|----------|
| ERR_ONTOLOGY_NOT_FOUND | 600 | 本体不存在 | 检查本体ID |
| ERR_CLASS_NOT_FOUND | 601 | 类定义不存在 | 检查类ID |
| ERR_ENTITY_NOT_FOUND | 602 | 实体不存在 | 检查实体ID |
| ERR_RELATION_NOT_FOUND | 603 | 关系不存在 | 检查关系ID |
| ERR_INVALID_ONTOLOGY | 610 | 本体定义无效 | 检查本体schema |
| ERR_CIRCULAR_INHERITANCE | 611 | 循环继承检测 | 检查类继承链 |
| ERR_INVALID_RELATION | 612 | 关系类型无效 | 检查关系定义 |
| ERR_QUERY_TIMEOUT | 620 | 查询超时 | 优化查询或增加超时 |

#### 3.2.4 第三方错误 (8xx)

| 错误码 | HTTP状态码 | 描述 | 解决方案 |
|--------|------------|------|----------|
| ERR_EXTERNAL_SERVICE | 800 | 外部服务错误 | 检查外部服务状态 |
| ERR_STORAGE_ERROR | 801 | 存储服务错误 | 检查存储服务 |
| ERR_CACHE_ERROR | 802 | 缓存服务错误 | 检查缓存服务 |

### 3.3 错误码命名规范

```
ERR_{模块}_{类型}
```

- **模块**: ONTOLOGY, ENTITY, RELATION, QUERY, TAXONOMY, TAG, SYSTEM
- **类型**: NOT_FOUND, INVALID, CONFLICT, EXCEEDED, TIMEOUT, UNAVAILABLE

示例:
- `ERR_ENTITY_NOT_FOUND` - 实体未找到
- `ERR_ONTOLOGY_INVALID_SCHEMA` - 本体Schema无效
- `ERR_QUERY_TIMEOUT` - 查询超时

---

## 附录

### A. 数据类型映射

| RDF数据类型 | JSON类型 | 说明 |
|------------|----------|------|
| xsd:string | string | 字符串 |
| xsd:integer | number | 整数 |
| xsd:decimal | number | 小数 |
| xsd:boolean | boolean | 布尔值 |
| xsd:dateTime | string | ISO 8601 日期时间 |
| xsd:date | string | ISO 8601 日期 |
| xsd:anyURI | string | URI字符串 |
| rdf:langString | object | 带语言标签的字符串 |

### B. 版本历史

| 版本 | 日期 | 修改内容 |
|------|------|----------|
| v1.0.0 | 2026-03-16 | 初始版本 |

---

*文档生成工具: OpenClaw*