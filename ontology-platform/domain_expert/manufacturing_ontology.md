# 制造业领域本体 (Manufacturing Ontology)

> 版本: 1.0  
> 领域: 制造业 (Manufacturing)  
> 描述: 制造业全流程领域的核心概念、实体、关系与属性定义

---

## 1. 核心实体 (Core Entities)

### 1.1 产品 (Product)

| 实体 | 英文 | 定义 | 关键属性 |
|------|------|------|----------|
| 产品 | Product | 制造业的最终产出物，可以是实体产品或服务 | `productId`, `name`, `category`, `specification`, `unit`, `lifecycle` |
| 零部件 | Component | 产品的组成单元，可进一步拆分为更小单元 | `componentId`, `name`, `parentProduct`, `material`, `version` |
| 原材料 | RawMaterial | 用于制造产品的原始物料 | `materialId`, `name`, `type`, `supplier`, `specification` |
| 半成品 | SemiFinishedProduct | 尚未完成全部制造工序的产品 | `semiProductId`, `name`, `processStage`, `completionRate` |
| 产成品 | FinishedProduct | 完成全部制造工序，可交付的产品 | `finishedProductId`, `name`, `qualityGrade`, `serialNumber` |

### 1.2 工艺 (Process)

| 实体 | 英文 | 定义 | 关键属性 |
|------|------|------|----------|
| 工艺路线 | ProcessRoute | 产品制造所经过的工序序列 | `routeId`, `productId`, `sequence`, `description` |
| 工序 | Operation | 工艺路线中的单个制造步骤 | `operationId`, `name`, `sequence`, `duration`, `equipment` |
| 工艺参数 | ProcessParameter | 工序执行时的关键控制参数 | `parameterId`, `operationId`, `name`, `value`, `unit`, `tolerance` |
| 工艺规程 | ProcessSpecification | 工序执行的详细操作规范 | `specId`, `operationId`, `content`, `standard`, `version` |

### 1.3 设备 (Equipment)

| 实体 | 英文 | 定义 | 关键属性 |
|------|------|------|----------|
| 设备 | Equipment | 用于制造、加工、检测的机械装置 | `equipmentId`, `name`, `type`, `model`, `status`, `location` |
| 设备能力 | EquipmentCapability | 设备能够完成的加工能力 | `capabilityId`, `equipmentId`, `processType`, `precision`, `capacity` |
| 设备状态 | EquipmentStatus | 设备的实时运行状态 | `equipmentId`, `status`, `utilization`, `nextMaintenance` |

### 1.4 资源 (Resource)

| 实体 | 英文 | 定义 | 关键属性 |
|------|------|------|----------|
| 人员 | Personnel | 制造企业的员工及其技能 | `personnelId`, `name`, `role`, `skills`, `certifications` |
| 工时 | WorkHour | 人员工作时间的分配与记录 | `workHourId`, `personnelId`, `date`, `duration`, `operation` |
| 能源 | Energy | 制造过程消耗的能源资源 | `energyType`, `consumption`, `cost`, `unit` |
| 工具 | Tool | 制造过程中使用的工装夹具 | `toolId`, `name`, `type`, `lifespan`, `status` |

### 1.5 质量 (Quality)

| 实体 | 英文 | 定义 | 关键属性 |
|------|------|------|----------|
| 质量标准 | QualityStandard | 产品与工序的质量要求规范 | `standardId`, `name`, `level`, `description` |
| 质检项 | InspectionItem | 质量检查的具体项目 | `itemId`, `name`, `standard`, `method`, `criteria` |
| 质量缺陷 | QualityDefect | 产品不符合质量标准的问题 | `defectId`, `type`, `severity`, `rootCause`, `location` |
| 质量报告 | QualityReport | 质量检查与评估的记录文档 | `reportId`, `date`, `inspector`, `results`, `conclusion` |

### 1.6 供应链 (Supply Chain)

| 实体 | 英文 | 定义 | 关键属性 |
|------|------|------|----------|
| 供应商 | Supplier | 提供原材料、零部件的企业 | `supplierId`, `name`, `rating`, `deliveryTime`, `certifications` |
| 采购订单 | PurchaseOrder | 向供应商采购物料的订单 | `poId`, `supplierId`, `items`, `date`, `status`, `deliveryDate` |
| 库存 | Inventory | 原材料、零部件、产品的库存状态 | `itemId`, `quantity`, `location`, `status`, `lastUpdate` |
| 仓库 | Warehouse | 存储物料与产品的设施 | `warehouseId`, `name`, `capacity`, `location`, `zones` |

### 1.7 生产 (Production)

| 实体 | 英文 | 定义 | 关键属性 |
|------|------|------|----------|
| 生产订单 | ProductionOrder | 安排生产任务的正式指令 | `orderId`, `productId`, `quantity`, `deadline`, `priority`, `status` |
| 生产计划 | ProductionPlan | 一段时间内的生产安排 | `planId`, `period`, `orders`, `resources`, `utilization` |
| 生产工单 | WorkOrder | 具体到工序级别的生产任务 | `workOrderId`, `productionOrderId`, `operation`, `quantity`, `status` |
| 生产进度 | ProductionProgress | 生产任务的实时执行状态 | `progressId`, `workOrderId`, `completedQty`, `scrapQty`, `efficiency` |

### 1.8 维护 (Maintenance)

| 实体 | 英文 | 定义 | 关键属性 |
|------|------|------|----------|
| 维护计划 | MaintenancePlan | 设备维护的定期计划 | `planId`, `equipmentId`, `frequency`, `type`, `tasks` |
| 维护工单 | MaintenanceWorkOrder | 具体的设备维修任务 | `mwoId`, `equipmentId`, `type`, `description`, `priority`, `status` |
| 故障记录 | FailureRecord | 设备故障的详细记录 | `recordId`, `equipmentId`, `failureTime`, `symptoms`, `rootCause` |

---

## 2. 核心关系 (Core Relations)

### 2.1 构成关系

```
产品 ──[由...组成]──> 零部件
零部件 ──[由...组成]──> 原材料
产品 ──[采用]──> 工艺路线
工艺路线 ──[包含]──> 工序
工序 ──[需要]──> 设备
工序 ──[需要]──> 工具
工序 ──[需要]──> 人员
```

### 2.2 执行关系

```
生产订单 ──[派生自]──> 产品
生产订单 ──[分解为]──> 生产工单
生产工单 ──[执行]──> 工序
生产工单 ──[消耗]──> 原材料
生产工单 ──[使用]──> 设备
```

### 2.3 质量关系

```
产品 ──[需符合]──> 质量标准
工序 ──[需符合]──> 质量标准
产品 ──[经历]──> 质检项
质检项 ──[产出]──> 质量报告
质量缺陷 ──[影响]──> 产品
```

### 2.4 供应链关系

```
原材料 ──[供应来自]──> 供应商
采购订单 ──[采购]──> 原材料
原材料 ──[存放于]──> 仓库
库存 ──[关联]──> 原材料/零部件/产品
```

### 2.5 维护关系

```
设备 ──[需要]──> 维护计划
维护计划 ──[产生]──> 维护工单
设备 ──[发生]──> 故障记录
故障记录 ──[导致]──> 维护工单
```

---

## 3. 属性 (Properties)

### 3.1 产品属性

| 属性 | 类型 | 描述 |
|------|------|------|
| productId | String | 产品唯一标识 |
| name | String | 产品名称 |
| category | Enum | 产品类别 (原材料/半成品/产成品) |
| specification | Object | 技术规格参数 |
| unit | String | 计量单位 |
| unitCost | Number | 单位成本 |
| lifecycle | Enum | 生命周期阶段 (研发/试产/量产/停产) |
| version | String | 版本号 |
| safetyStock | Number | 安全库存量 |

### 3.2 工艺属性

| 属性 | 类型 | 描述 |
|------|------|------|
| routeId | String | 工艺路线ID |
| sequence | Number | 工序顺序 |
| standardTime | Number | 标准工时(分钟) |
| setupTime | Number | 换型时间(分钟) |
| yieldRate | Number | 良品率 |
| description | String | 工艺描述 |

### 3.3 设备属性

| 属性 | 类型 | 描述 |
|------|------|------|
| equipmentId | String | 设备ID |
| name | String | 设备名称 |
| type | String | 设备类型 |
| model | String | 设备型号 |
| manufacturer | String | 制造商 |
| purchaseDate | Date | 采购日期 |
| status | Enum | 状态 (正常/维修/空闲/报废) |
| utilization | Number | 利用率(%) |
| location | String | 所在车间/产线 |

### 3.4 质量属性

| 属性 | 类型 | 描述 |
|------|------|------|
| inspectionDate | Date | 检验日期 |
| sampleSize | Number | 抽样数量 |
| defectiveQty | Number | 不合格数量 |
| defectRate | Number | 不合格率 |
| severity | Enum | 严重程度 (致命/严重/一般/轻微) |
| inspector | String | 检验员 |
| conclusion | Enum | 结论 (合格/不合格/待定) |

---

## 4. 子领域 (Sub-Domains)

### 4.1 生产制造 (Production Manufacturing)

- 生产计划与排程
- 生产订单管理
- 生产进度跟踪
- 工艺参数管理
- 生产效率分析

### 4.2 供应链管理 (Supply Chain Management)

- 供应商管理
- 采购管理
- 库存管理
- 仓储物流
- 物料配送

### 4.3 质量管理 (Quality Management)

- 质量标准制定
- 来料检验 (IQC)
- 过程检验 (IPQC)
- 最终检验 (FQC)
- 出货检验 (OQC)
- 质量分析与改进

### 4.4 设备管理 (Equipment Management)

- 设备台账
- 预防性维护
- 故障维修
- 备件管理
- 设备效率 (OEE)

### 4.5 工艺设计 (Process Design)

- 工艺路线规划
- 工序设计
- 参数优化
- 工装夹具设计
- 工艺文件管理

### 4.6 成本管理 (Cost Management)

- 成本核算
- 成本分析
- 预算管理
- 成本优化

---

## 5. 术语表 (Glossary)

| 术语 | 英文 | 定义 |
|------|------|------|
| 产能 | Capacity | 设备或产线在单位时间内能够生产的产品数量 |
| 产能利用率 | Utilization Rate | 实际产量与产能的比值 |
| 良品率 | Yield Rate | 合格产品数量与总产量的比值 |
| 生产节拍 | Takt Time | 满足客户需求的生产节奏时间 |
| 在制品 | WIP (Work In Progress) | 正在生产中尚未完成的半成品 |
| 拉动式生产 | Pull Production | 根据实际需求拉动生产的方式 |
| 推动式生产 | Push Production | 根据预测计划推动生产的方式 |
| 精益生产 | Lean Production | 消除浪费、持续改进的生产方式 |
| 看板 | Kanban | 精益生产中的可视化管理工具 |
| 设备综合效率 | OEE (Overall Equipment Effectiveness) | 可用率×性能率×良品率的乘积 |
| 准时制 | JIT (Just In Time) | 在需要时准时配送的物流方式 |
| 快速换模 | SMED (Single Minute Exchange of Die) | 快速更换工装的技法 |
| 持续改进 | Kaizen | 不断改进的企业文化 |
| 六大损失 | Six Big Losses | 影响OEE的六类损失 |
| 统计过程控制 | SPC (Statistical Process Control) | 用统计方法控制过程质量 |
| 全面生产维护 | TPM (Total Productive Maintenance) | 全员参与的生产维护体系 |

---

## 6. 本体扩展 (Extensions)

### 6.1 行业专用扩展

- **汽车制造业**: 汽车零部件、焊接、涂装、总装
- **电子制造业**: PCB组装、SMT、测试、封装
- **食品制造业**: 配方、批次追溯、保质期管理
- **医药制造业**: GMP、验证、洁净度、批次管理
- **纺织制造业**: 纺纱、织造、染整

### 6.2 智能制造扩展

- 数字孪生 (Digital Twin)
- 工业互联网 (IIoT)
- 边缘计算 (Edge Computing)
- 预测性维护 (Predictive Maintenance)
- 智能排程 (Smart Scheduling)

---

## 7. 参考标准

- ISO 9001 质量管理体系
- ISO/TS 16949 汽车行业质量管理体系
- ISO 14001 环境管理体系
- IEC 62264 企业控制系统集成
- ISA-95 企业-控制层集成
- GB/T 20719 企业生产过程管理

---

*本本体定义了制造业的核心概念与关系，可作为知识图谱构建、语义搜索、专家系统等应用的领域知识基础。*