"""Agent 记忆治理模块 (Memory Governance)

本模块提供 Agent 长期记忆的语义健康度监控与治理功能。

核心特性:
- 本体健康度监控仪表盘
- 类层次结构漂移检测
- 记忆一致性验证
- 目标稳定性校验

使用示例:
    from ontology_platform.memory import MemoryGovernance
    
    gov = MemoryGovernance(agent_memory_ontology)
    health = gov.check_health()
    print(f"Health score: {health.overall_score}")
    print(f"Drift detected: {health.drift_alerts}")
"""
from .governance import MemoryGovernance, HealthReport, DriftAlert
from .monitor import MemoryMonitor, TimeSeriesMetric

__all__ = [
    "MemoryGovernance", 
    "HealthReport", 
    "DriftAlert",
    "MemoryMonitor",
    "TimeSeriesMetric",
]
