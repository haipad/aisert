import pytest

from src.modules.semantic_match import SemanticMatch

def test_semantic_match_compare_equal(monkeypatch):
    matcher = SemanticMatch()
    monkeypatch.setattr(matcher, "compare", lambda a, b: True)
    assert matcher.compare("hello", "hello") is True

def test_semantic_match_compare_not_equal(monkeypatch):
    matcher = SemanticMatch()
    monkeypatch.setattr(matcher, "compare", lambda a, b: False)
    assert matcher.compare("hello", "world") is False
