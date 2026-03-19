# 供应链本体 v2.0

采购供应链领域本体系统，包含业务规则、推理引擎和应用脚本。

## 项目结构

```
ontology-clawra/
├── scripts/
│   ├── supplier_risk_evaluation.py   # 供应商风险评估
│   ├── purchase_price_analysis.py    # 采购价格分析
│   └── contract_review.py            # 合同审查
└── docs/
    └── supply_chain.yaml             # 本体定义文档
```

## 快速开始

### 1. 本体验证

```bash
python3 ~/.openclaw/skills/ontology-clawra/scripts/ontology-clawra.py validate
```

### 2. 运行推理脚本

#### 供应商风险评估
```bash
python3 scripts/ontology-clawra/supplier_risk_evaluation.py
```

#### 采购价格分析
```bash
python3 scripts/ontology-clawra/purchase_price_analysis.py
```

#### 合同审查
```bash
python3 scripts/ontology-clawra/contract_review.py
```

## 推理场景说明

### 供应商风险评估
- **输入**: 供应商基础信息、绩效数据、财务数据
- **输出**: 风险等级评分、风险因子分析、预警建议
- **规则**:
  - 交付风险: OTD < 90% 触发
  - 质量风险: 不良率 > 2% 或有事故记录
  - 价格风险: 价格波动 > 10%
  - 财务风险: 财务状况差
  - 供应风险: 单一供应商占比 > 60%

### 采购价格分析
- **输入**: 采购物料信息、历史价格数据
- **输出**: 价格趋势分析、最佳采购时机建议

### 合同审查
- **输入**: 合同文本
- **输出**: 关键条款检查、风险点识别

## 本体版本

- **当前版本**: v2.0
- **更新日期**: 2026-03-19
- **领域**: 采购供应链 + 燃气设备垂直用例

## 依赖

- Python 3.8+
- 无外部依赖（使用标准库）
