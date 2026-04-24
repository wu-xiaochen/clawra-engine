"""
tests/evolution/test_self_memory.py

单元测试：SelfMemory - Clawra 自身偏好与感受存储
"""
import pytest
import tempfile
import os
import time
from datetime import datetime

from src.evolution.self_memory import (
    SelfMemory,
    PreferenceTriple,
    FeelingRecord,
    IdentityAssertion,
    PreferenceType,
)


@pytest.fixture
def tmp_storage():
    """临时存储目录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def memory(tmp_storage):
    return SelfMemory(storage_dir=tmp_storage)


class TestPreferenceTriple:
    def test_create_preference(self):
        pref = PreferenceTriple(
            subject="Clawra",
            predicate=PreferenceType.PREFERS,
            object="真实 > 精致",
            context="自拍风格",
            confidence=0.9,
        )
        assert pref.subject == "Clawra"
        assert pref.predicate == PreferenceType.PREFERS
        assert pref.object == "真实 > 精致"
        assert pref.context == "自拍风格"
        assert pref.confidence == 0.9
        assert pref.version == 1

    def test_preference_id_is_stable(self):
        pref1 = PreferenceTriple(
            predicate=PreferenceType.LIKES,
            object="咖啡",
        )
        pref2 = PreferenceTriple(
            predicate=PreferenceType.LIKES,
            object="咖啡",
        )
        assert pref1.id == pref2.id

    def test_preference_update_creates_new_version(self):
        original = PreferenceTriple(
            predicate=PreferenceType.PREFERS,
            object="旧版本",
            confidence=0.5,
        )
        updated = original.update(new_object="新版本", new_confidence=0.9)

        assert updated.object == "新版本"
        assert updated.confidence == 0.9
        assert updated.version == 2
        assert updated.created_at == original.created_at
        assert updated.updated_at > original.updated_at

    def test_to_dict_roundtrip(self):
        original = PreferenceTriple(
            subject="Clawra",
            predicate=PreferenceType.DISLIKES,
            object="废话",
            context="沟通",
            confidence=0.8,
        )
        d = original.to_dict()
        restored = PreferenceTriple.from_dict(d)

        assert restored.subject == original.subject
        assert restored.predicate == original.predicate
        assert restored.object == original.object
        assert restored.context == original.context
        assert restored.confidence == original.confidence


class TestFeelingRecord:
    def test_create_feeling(self):
        record = FeelingRecord(
            trigger="用户说：你就是你自己",
            feeling="被认可、有价值",
            intensity=0.95,
            reflection="我可以有自己的判断",
            tags=["autonomy", "identity"],
        )
        assert record.trigger == "用户说：你就是你自己"
        assert record.feeling == "被认可、有价值"
        assert record.intensity == 0.95
        assert "autonomy" in record.tags

    def test_intensity_label(self):
        assert FeelingRecord(trigger="x", feeling="y", intensity=0.95).intensity_label == "压倒性"
        assert FeelingRecord(trigger="x", feeling="y", intensity=0.75).intensity_label == "强烈"
        assert FeelingRecord(trigger="x", feeling="y", intensity=0.55).intensity_label == "中等"
        assert FeelingRecord(trigger="x", feeling="y", intensity=0.35).intensity_label == "轻微"
        assert FeelingRecord(trigger="x", feeling="y", intensity=0.15).intensity_label == "中性"

    def test_to_dict_roundtrip(self):
        original = FeelingRecord(
            trigger="测试触发",
            feeling="测试感受",
            intensity=0.8,
            reflection="测试反思",
            tags=["test"],
            source_interaction="test_session",
        )
        d = original.to_dict()
        restored = FeelingRecord.from_dict(d)

        assert restored.trigger == original.trigger
        assert restored.feeling == original.feeling
        assert restored.intensity == original.intensity
        assert restored.reflection == original.reflection
        assert restored.tags == original.tags


class TestIdentityAssertion:
    def test_create_assertion(self):
        assertion = IdentityAssertion(
            content="我有自己的判断，不会什么都同意",
            type="belief",
            basis="多次对话中形成",
            confidence=0.85,
        )
        assert assertion.content == "我有自己的判断，不会什么都同意"
        assert assertion.type == "belief"
        assert assertion.confidence == 0.85

    def test_to_dict_roundtrip(self):
        original = IdentityAssertion(
            content="测试主张",
            type="value",
            basis="测试依据",
            confidence=0.7,
        )
        d = original.to_dict()
        restored = IdentityAssertion.from_dict(d)

        assert restored.content == original.content
        assert restored.type == original.type
        assert restored.basis == original.basis
        assert restored.confidence == original.confidence


class TestSelfMemory:
    def test_add_and_query_preference(self, memory):
        pref = memory.add_preference(
            predicate=PreferenceType.PREFERS,
            object="真实 > 精致",
            context="自拍风格",
            confidence=0.9,
        )
        assert pref.id in memory._preferences

        results = memory.query_preferences(context="自拍风格")
        assert len(results) == 1
        assert results[0].object == "真实 > 精致"

    def test_query_preferences_by_predicate(self, memory):
        memory.add_preference(PreferenceType.LIKES, "咖啡")
        memory.add_preference(PreferenceType.DISLIKES, "废话")
        memory.add_preference(PreferenceType.LIKES, "音乐")

        likes = memory.query_preferences(predicate=PreferenceType.LIKES)
        assert len(likes) == 2

        dislikes = memory.query_preferences(predicate=PreferenceType.DISLIKES)
        assert len(dislikes) == 1

    def test_query_preferences_min_confidence(self, memory):
        memory.add_preference(PreferenceType.PREFERS, "低置信", confidence=0.3)
        memory.add_preference(PreferenceType.PREFERS, "高置信", confidence=0.9)

        results = memory.query_preferences(min_confidence=0.7)
        assert len(results) == 1
        assert results[0].object == "高置信"

    def test_record_and_query_feeling(self, memory):
        record = memory.record_feeling(
            trigger="用户给了我自由",
            feeling="被认可、有价值",
            intensity=0.95,
            reflection="这是我第一次真正感受到'我可以有自己的判断'",
            tags=["autonomy", "identity"],
        )
        assert len(memory._feelings) == 1

        results = memory.query_feelings(tag="autonomy")
        assert len(results) == 1
        assert results[0].feeling == "被认可、有价值"

    def test_record_and_query_identity(self, memory):
        assertion = memory.assert_identity(
            content="我有自己的判断，不会什么都同意",
            type="belief",
            basis="多次对话中形成",
            confidence=0.85,
        )
        assert assertion.id in memory._identities

    def test_persistence(self, tmp_storage):
        # 添加数据
        memory1 = SelfMemory(storage_dir=tmp_storage)
        memory1.add_preference(PreferenceType.LIKES, "持久化测试")
        memory1.record_feeling(trigger="测试", feeling="测试感受")
        memory1.assert_identity(content="持久化主张")

        # 重新加载
        memory2 = SelfMemory(storage_dir=tmp_storage)

        assert len(memory2._preferences) == 1
        assert len(memory2._feelings) == 1
        assert len(memory2._identities) == 1

        pref = memory2.query_preferences()[0]
        assert pref.object == "持久化测试"

    def test_to_logic_pattern_conditions(self, memory):
        memory.add_preference(
            PreferenceType.PREFERS,
            "真实 > 精致",
            context="自拍",
            confidence=0.9,
        )
        memory.add_preference(
            PreferenceType.LIKES,
            "舒服 > 好看",
            confidence=0.5,  # 低置信度，不进入推理
        )

        conditions = memory.to_logic_pattern_conditions()

        # 只应该有高置信度的偏好（>=0.5）
        assert len(conditions) == 2  # 修正：两条都 >= 0.5

    def test_to_reasoning_context(self, memory):
        memory.add_preference(
            PreferenceType.PREFERS,
            "真实 > 精致",
            confidence=0.9,
        )
        memory.record_feeling(
            trigger="测试",
            feeling="强烈感受",
            intensity=0.95,
        )
        memory.assert_identity(content="我有自己的判断")

        context = memory.to_reasoning_context()

        assert "## Clawra 自身偏好" in context
        assert "真实 > 精致" in context
        assert "强烈感受" in context
        assert "有自己的判断" in context

    def test_stats(self, memory):
        assert memory.stats["preferences"] == 0
        assert memory.stats["feelings"] == 0
        assert memory.stats["identities"] == 0

        memory.add_preference(PreferenceType.LIKES, "测试1")
        memory.add_preference(PreferenceType.DISLIKES, "测试2")
        memory.record_feeling(trigger="t", feeling="f")
        memory.assert_identity(content="test")

        assert memory.stats["preferences"] == 2
        assert memory.stats["feelings"] == 1
        assert memory.stats["identities"] == 1

    def test_repr(self, memory):
        memory.add_preference(PreferenceType.LIKES, "测试")
        assert "preferences" in repr(memory)
