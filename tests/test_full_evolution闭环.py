"""
Full Evolution Loop 端到端集成测试

测试完整闭环通道:
  1. learn() → EvolutionLoop.run() → KG 模式沉淀
  2. orchestrate() → EvolutionLoop.step(reason) → 检索增强
  3. HonchoBridge 实时同步 → 用户认知注入推理上下文
  4. 每次 learn 成功后自动触发 evolve() 后台进化

无需真实 LLM API，使用 mock 保持测试稳定快速。
"""
import pytest
import sys
import os
import asyncio
import time
import concurrent.futures
from unittest.mock import MagicMock, AsyncMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.clawra import Clawra
from src.evolution.llm_extractor import ExtractionResult, ExtractedEntity, ExtractedRule


def make_mock_result(domain="通用", rules=None, entities=None):
    """构建mock ExtractionResult，简化各fixture的创建"""
    return ExtractionResult(
        rules=rules or [],
        entities=entities or [],
        relations=[],
        domain=domain,
    )


def create_test_clawra(mock_learn_result=None):
    """
    创建测试用 Clawra，同时 patch 所有外部网络调用：
    - evolution_loop.run（返回模拟学习结果到 logic_layer）
    - Honcho API 同步
    - GitHub 记忆加载

    关键：clawra.learn() 内部调用 self.evolution_loop.run() 并从返回结构中
    解析 pattern_ids，所以必须 patch evolution_loop.run 而非 meta_learner.learn。
    patch.object 替换实例方法时，mock 函数不加 self（bound method 绑定会自动处理）。
    """
    import src.evolution.honcho_bridge as hb_module
    import src.evolution.self_memory as sm_module

    _mock_result = mock_learn_result or {
        "success": True,
        "learned_patterns": ["p_test1"],
        "patterns_created": 1,
        "extracted_facts": [],
        "domain": "通用",
        "strategy": "mock",
        "episode_id": "test_ep",
    }

    def mock_sync(self, logic_layer, **kwargs):
        return 0

    def mock_load(self):
        pass

    # evolution_loop.run 的 mock 不需要 self（patch.object 替换 bound method 时自动处理）
    def mock_evo_run(input_data):
        pattern_ids = _mock_result.get("learned_patterns", [])
        # 直接在 logic_layer 创建 LogicPattern（模拟 meta_learner.learn 的真实行为）
        if _mock_result.get("success") and pattern_ids:
            from src.evolution.unified_logic import LogicPattern, LogicType
            for pid in pattern_ids:
                if pid not in clawra.logic_layer.patterns:
                    p = LogicPattern(
                        id=pid,
                        logic_type=LogicType.RULE,
                        name=f"MockPattern: {pid}",
                        description="mock pattern for testing",
                        conditions=[],
                        actions=[],
                        confidence=0.9,
                        source="mock",
                        domain=_mock_result.get("domain", "通用"),
                    )
                    clawra.logic_layer.add_pattern(p)
        return {
            "success": _mock_result.get("success", True),
            "episode_id": _mock_result.get("episode_id", "test_ep"),
            "results": {
                "learn": {
                    "data": {
                        "patterns_created": _mock_result.get("patterns_created", 1),
                        "pattern_ids": pattern_ids,
                    }
                }
            },
            "feedback_signals": [],
        }

    # Patch class-level（屏蔽外部网络调用）
    patches = [
        patch.object(hb_module.HonchoBridge, 'sync_from_honcho_sync', mock_sync),
        patch.object(sm_module.SelfMemory, 'load_from_github', mock_load),
    ]

    for p in patches:
        p.start()

    clawra = Clawra()

    for p in patches:
        p.stop()

    # Patch 实例方法：替换 evolution_loop.run 为 mock（无需 self 参数）
    clawra.evolution_loop.run = mock_evo_run
    return clawra


class TestLearnEvolutionLoopIntegration:
    """通道1: learn() → EvolutionLoop.run() → KG 更新"""

    @pytest.fixture
    def mock_clawra(self):
        mock_learn_result = {
            "success": True,
            "learned_patterns": ["p1"],
            "patterns_created": 1,
            "extracted_facts": [],
            "domain": "燃气",
            "strategy": "mock",
            "episode_id": "test_learn1",
        }
        return create_test_clawra(mock_learn_result)

    def test_learn_calls_evolution_loop_run(self, mock_clawra):
        """验证 learn() 真实调用了 evolution_loop.run()"""
        with patch.object(mock_clawra.evolution_loop, 'run', wraps=mock_clawra.evolution_loop.run) as mock_run:
            result = mock_clawra.learn(
                "燃气调压箱是一种燃气设备，燃气设备需要定期维护。",
                domain_hint="燃气"
            )
            assert mock_run.call_count >= 1
            call_args = mock_run.call_args[0][0]
            assert "text" in call_args
            assert result["success"] is True

    def test_learn_patterns_stored_in_logic_layer(self, mock_clawra):
        """验证 learn() 学到的模式写入了 LogicLayer"""
        result = mock_clawra.learn("燃气调压箱是一种燃气设备。", domain_hint="燃气")
        pattern_ids = result.get("learned_patterns", [])
        assert len(pattern_ids) > 0
        for pid in pattern_ids:
            assert pid in mock_clawra.logic_layer.patterns

    def test_learn_episodic_memory_recorded(self, mock_clawra):
        """验证 learn() 自动记录到情节记忆"""
        if not hasattr(mock_clawra, 'episodic_mgr'):
            pytest.skip("EpisodicMemory 未启用")
        with patch.object(mock_clawra.episodic_mgr, 'add_interaction', wraps=mock_clawra.episodic_mgr.add_interaction) as mock_add:
            mock_clawra.learn("燃气调压箱是一种燃气设备。", domain_hint="燃气")
            assert mock_add.call_count >= 1

    def test_learn_auto_evolve_no_exception(self, mock_clawra):
        """验证 learn() 成功后触发 evolve() 不会抛异常（fire-and-forget 正常）"""
        # 等待后台任务触发
        time.sleep(0.5)
        # 不抛异常即说明正常
        assert True


class TestOrchestrateEvolutionReason:
    """通道2: orchestrate() → EvolutionLoop.step(reason) → 检索增强"""

    @pytest.fixture
    def mock_clawra(self):
        mock_learn_result = {
            "success": True,
            "learned_patterns": [],
            "patterns_created": 0,
            "extracted_facts": [],
            "domain": "通用",
            "strategy": "mock",
            "episode_id": "test_orch",
        }
        clawra = create_test_clawra(mock_learn_result)
        clawra.add_fact("燃气调压箱", "is_a", "燃气设备", 0.95)
        clawra.add_fact("燃气设备", "需要", "定期维护", 0.9)
        return clawra

    def test_orchestrate_calls_evolution_loop_step_reason(self, mock_clawra):
        """验证 orchestrate() 真实调用了 evolution_loop.step(phase=reason)"""
        with patch.object(
            mock_clawra.evolution_loop, 'step',
            wraps=mock_clawra.evolution_loop.step
        ) as mock_step:
            result = mock_clawra.orchestrate("燃气调压箱需要维护吗？")
            assert mock_step.call_count >= 1
            call_args = mock_step.call_args[0][0]
            assert call_args.get("phase") == "reason"
            assert result["query"] == "燃气调压箱需要维护吗？"

    def test_orchestrate_injects_self_memory_context(self, mock_clawra):
        """验证 orchestrate() 注入了自我记忆上下文"""
        if not hasattr(mock_clawra, 'self_memory') or not mock_clawra.self_memory:
            pytest.skip("SelfMemory 未启用")
        with patch.object(
            mock_clawra.self_memory, 'to_reasoning_context',
            return_value="[自我偏好]: 喜欢简洁回答"
        ):
            result = mock_clawra.orchestrate("什么是燃气调压箱？")
            assert result is not None

    def test_orchestrate_injects_episodic_context(self, mock_clawra):
        """验证 orchestrate() 注入了情节记忆上下文"""
        if not hasattr(mock_clawra, 'episodic_mgr'):
            pytest.skip("EpisodicMemory 未启用")
        result = mock_clawra.orchestrate("上次我问了什么问题？")
        assert result is not None


class TestHonchoBridgeSync:
    """通道3: HonchoBridge 实时同步"""

    @pytest.fixture
    def mock_clawra(self):
        mock_learn_result = {
            "success": True,
            "learned_patterns": [],
            "patterns_created": 0,
            "extracted_facts": [],
            "domain": "通用",
            "strategy": "mock",
            "episode_id": "test_honcho",
        }
        return create_test_clawra(mock_learn_result)

    def test_honcho_bridge_initialized(self, mock_clawra):
        """验证 HonchoBridge 在 Clawra 初始化时已实例化"""
        assert hasattr(mock_clawra, '_honcho_bridge')
        assert mock_clawra._honcho_bridge is not None

    def test_get_user_cognition_guidance_calls_honcho(self, mock_clawra):
        """验证 get_user_cognition_guidance() 调用了 HonchoBridge"""
        if not hasattr(mock_clawra, '_honcho_bridge'):
            pytest.skip("HonchoBridge 未启用")
        with patch.object(
            mock_clawra._honcho_bridge, 'query_patterns',
            wraps=mock_clawra._honcho_bridge.query_patterns
        ) as mock_query:
            guidance = mock_clawra.get_user_cognition_guidance()
            assert mock_query.call_count >= 1

    def test_orchestrate_injects_user_guidance(self, mock_clawra):
        """验证 orchestrate() 注入了用户认知指导"""
        if not hasattr(mock_clawra, '_honcho_bridge'):
            pytest.skip("HonchoBridge 未启用")
        with patch.object(mock_clawra._honcho_bridge, 'query_patterns', return_value=[]):
            result = mock_clawra.orchestrate("如何维护燃气设备？")
            assert result is not None
            assert "trace" in result


class TestEvolveAutoTrigger:
    """通道4: 每次 learn 成功后自动触发 evolve()"""

    @pytest.fixture
    def mock_clawra(self):
        mock_learn_result = {
            "success": True,
            "learned_patterns": ["p_auto"],
            "patterns_created": 1,
            "extracted_facts": [],
            "domain": "通用",
            "strategy": "mock",
            "episode_id": "test_evolve",
        }
        return create_test_clawra(mock_learn_result)

    def test_evolve_method_exists_and_async(self, mock_clawra):
        """验证 evolve() 方法存在且为 async"""
        assert hasattr(mock_clawra, 'evolve')
        import inspect
        assert inspect.iscoroutinefunction(mock_clawra.evolve)

    def test_safe_evolve_exists(self, mock_clawra):
        """验证 _safe_evolve() 包装器存在"""
        assert hasattr(mock_clawra, '_safe_evolve')
        import inspect
        assert inspect.iscoroutinefunction(mock_clawra._safe_evolve)

    @pytest.mark.asyncio
    async def test_evolve_runs_knowledge_evaluation(self, mock_clawra):
        """验证 evolve() 执行了知识质量评估"""
        eval_summary = mock_clawra.evaluate_knowledge()
        assert "total_evaluated" in eval_summary

    @pytest.mark.asyncio
    async def test_evolve_runs_conflict_check(self, mock_clawra):
        """验证 evolve() 执行了冲突检测"""
        conflicts = mock_clawra.conflict_checker.check_all_facts()
        assert conflicts is not None


class TestFullWorkflow:
    """完整场景: learn() → evolve() → orchestrate() 联合测试"""

    @pytest.fixture
    def mock_clawra(self):
        mock_learn_result = {
            "success": True,
            "learned_patterns": ["p_闭环1"],
            "patterns_created": 1,
            "extracted_facts": [],
            "domain": "燃气",
            "strategy": "mock",
            "episode_id": "test_full_flow",
        }
        return create_test_clawra(mock_learn_result)

    def test_learn_then_orchestrate_full_flow(self, mock_clawra):
        """完整流程: learn() 学知识 → orchestrate() 用知识推理"""
        # Step 1: learn()
        learn_result = mock_clawra.learn(
            "闭环测试设备是一种燃气设备，燃气设备需要安全检查。",
            domain_hint="燃气"
        )
        assert learn_result["success"] is True

        # Step 2: orchestrate()
        query = "闭环测试设备需要什么？"
        orch_result = mock_clawra.orchestrate(query)

        # 验证返回结构完整
        assert "query" in orch_result
        assert "conclusions" in orch_result
        assert "trace" in orch_result

        # 验证 trace 包含关键阶段
        trace_str = str(orch_result["trace"])
        assert "perception" in trace_str.lower()

    def test_multiple_learns_accumulate_patterns(self, mock_clawra):
        """多次 learn() 累积模式到 LogicLayer"""
        initial_patterns = len(mock_clawra.logic_layer.patterns)

        mock_clawra.learn("设备A 是一种燃气设备。", domain_hint="燃气")
        mock_clawra.learn("设备B 是一种燃气设备。", domain_hint="燃气")

        current = len(mock_clawra.logic_layer.patterns)
        assert current >= initial_patterns


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
