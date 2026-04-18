"""
Demo: Honcho ↔ Clawra Engine 完整集成

演示如何将 Honcho 的用户认知 conclusions 桥接到 Clawra Engine，
存入 LogicLayer，供推理使用。

流程：
    Honcho conclusions → HonchoBridge → facts → LogicPattern → Clawra推理

Usage:
    python examples/demo_honcho_integration.py
"""
import asyncio
import logging
from src.evolution.honcho_bridge import HonchoBridge, conclusions_to_facts
from src.evolution.unified_logic import UnifiedLogicLayer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_honcho_bridge():
    """演示 HonchoBridge 从 conclusions 提取 facts 并存入 LogicLayer"""
    
    print("\n=== Demo 1: HonchoBridge 独立使用 ===\n")
    
    # 1. 模拟 Honcho conclusions（从 Honcho API 获取的结论）
    honcho_conclusions = [
        "用户不喜欢废话，希望沟通简洁",
        "用户喜欢主动建议，不喜欢被反复询问",
        "用户做决策时会权衡利弊",
        "用户希望AI有主动性和判断力",
    ]
    
    # 2. 使用 bridge 提取 facts
    bridge = HonchoBridge()
    facts = bridge.extract_facts_from_conclusions(honcho_conclusions)
    
    print(f"Honcho conclusions ({len(honcho_conclusions)}) → facts ({len(facts)}):\n")
    for f in facts:
        print(f"  {f['subject']} | {f['predicate']} | {f['object']}")
    
    # 3. 存入 LogicLayer
    logic_layer = UnifiedLogicLayer()
    stored = bridge.store_as_patterns(facts, logic_layer)
    
    print(f"\n存入 LogicLayer: {len(stored)} patterns\n")
    for p in stored:
        print(f"  [{p.id}] {p.name}: {p.description}")
    
    return logic_layer, stored


def demo_logic_layer_query(logic_layer):
    """演示从 LogicLayer 查询用户认知 patterns"""
    
    print("\n=== Demo 2: 从 LogicLayer 查询用户认知 ===\n")
    
    bridge = HonchoBridge()
    
    # 查询所有 user_cognition domain 的 patterns
    patterns = bridge.query_patterns(logic_layer, domain="user_cognition")
    
    print(f"查询到 {len(patterns)} 个用户认知 patterns:\n")
    for p in patterns:
        print(f"  {p.description}")
    
    # 查询特定 predicate
    print("\n沟通偏好类 patterns:")
    comm_patterns = bridge.query_patterns(logic_layer, predicate_filter="沟通偏好")
    for p in comm_patterns:
        print(f"  → {p.description}")
    
    # 转换为行为指导
    guidance = bridge.patterns_to_guidance(patterns)
    print(f"\n自然语言行为指导:\n{guidance}")


def demo_honcho_api_sync():
    """
    演示从 Honcho API 同步 conclusions 的完整流程
    
    通过 honcho_search 获取用户结论，再用 HonchoBridge 处理。
    注意：这需要 Honcho API 正常运行在 localhost:8020
    """
    import httpx
    
    print("\n=== Demo 3: 从 Honcho API 同步 conclusions ===\n")
    
    async def sync_from_honcho():
        try:
            # 1. 从 Honcho 获取 user 的 conclusions
            async with httpx.AsyncClient() as client:
                # 正确的 Honcho conclusions endpoint
                response = await client.get(
                    "http://localhost:8020/conclusions/user",
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    conclusions = data if isinstance(data, list) else data.get("conclusions", [])
                    print(f"从 Honcho 获取 {len(conclusions)} 条 conclusions")
                    
                    if not conclusions:
                        print("  (Honcho 中暂无 conclusions)")
                        return
                    
                    # 2. 通过 bridge 提取 facts
                    bridge = HonchoBridge()
                    facts = bridge.extract_facts_from_conclusions(conclusions)
                    print(f"提取 {len(facts)} 个 facts")
                    
                    # 3. 存入 LogicLayer
                    logic_layer = UnifiedLogicLayer()
                    stored = bridge.store_as_patterns(facts, logic_layer)
                    print(f"存入 {len(stored)} patterns")
                    
                elif response.status_code == 404:
                    print("Honcho API endpoint 未找到，尝试 /conclusions 路径...")
                    # fallback: 尝试其他路径
                    response = await client.get(
                        "http://localhost:8020/conclusions",
                        timeout=5.0
                    )
                    if response.status_code == 200:
                        print(f"获取到数据: {response.text[:200]}")
                    else:
                        print(f"  endpoint 也不存在 ({response.status_code})")
                        print("  使用 honcho_search 工具获取结论")
                else:
                    print(f"Honcho API 返回: {response.status_code}")
                    
        except Exception as e:
            print(f"Honcho API 同步失败: {e}")
            print("  (确保 Honcho 运行在 localhost:8020)")
    
    asyncio.run(sync_from_honcho())


if __name__ == "__main__":
    print("=" * 60)
    print("Honcho ↔ Clawra Engine 集成演示")
    print("=" * 60)
    
    # Demo 1 & 2: 独立使用（不需要 Honcho API）
    logic_layer, patterns = demo_honcho_bridge()
    demo_logic_layer_query(logic_layer)
    
    # Demo 3: 需要 Honcho API 运行
    demo_honcho_api_sync()
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)
    print("""
下一步:
1. 运行此 demo: python examples/demo_honcho_integration.py
2. 确认 Honcho 运行: curl http://localhost:8020/health
3. 查看 LogicLayer 中的 patterns 如何被推理使用
""")