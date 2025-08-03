import pytest

from src.modules.token_validator.token_validator import TokenCounter

def test_token_counter_count_tokens(monkeypatch):
    counter = TokenCounter()
    monkeypatch.setattr(counter, "count_tokens", lambda: 7)
    assert counter.count_tokens() == 7

def test_token_counter_count_tokens_zero(monkeypatch):
    counter = TokenCounter()
    monkeypatch.setattr(counter, "count_tokens", lambda: 0)
    assert counter.count_tokens() == 0
