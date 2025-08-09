import pytest
from unittest.mock import MagicMock, patch

from aisert.aisert import Aisert

@pytest.fixture
def sample_content():
    return {"key": "value", "list": [1, 2, 3]}

@pytest.fixture
def sample_schema():
    return {"type": "object", "properties": {"key": {"type": "string"}}}

@pytest.fixture
def sample_config():
    return {"setting": True, "threshold": 10}

def test_configure_sets_config_and_initializes_helpers(sample_content, sample_config):
    aisert = Aisert(sample_content)
    with patch("src.aisert.main.TokenCounter") as MockTokenCounter, \
         patch("src.aisert.main.SemanticMatch") as MockSemanticMatch:
        aisert.configure(sample_config)
        assert aisert.config == sample_config
        MockTokenCounter.assert_called_once()
        MockSemanticMatch.assert_called_once()
        assert hasattr(aisert, "token_counter")
        assert hasattr(aisert, "semantic_matcher")

def test_assert_schema_calls_validator(sample_content, sample_schema):
    aisert = Aisert(sample_content)
    with patch("src.aisert.main.SchemaValidator.is_schema_match", return_value=True) as mock_validator:
        result = aisert.assert_schema(sample_schema)
        mock_validator.assert_called_once_with(sample_content, sample_schema)
        assert result is True

def test_assert_contains_true_and_false(sample_content, sample_config):
    aisert = Aisert(sample_content)
    aisert.config = sample_config
    assert aisert.assert_contains("setting") is True
    assert aisert.assert_contains("nonexistent") is False

def test_assert_tokens_less_than_and_greater_than(sample_content):
    aisert = Aisert(sample_content)
    aisert.token_counter = MagicMock()
    aisert.token_counter.count_tokens.return_value = 5
    assert aisert.assert_tokens_less_than(10) is True
    assert aisert.assert_tokens_less_than(5) is False
    assert aisert.assert_tokens_greater_than(2) is True
    assert aisert.assert_tokens_greater_than(5) is False

def test_assert_semantic_equals(sample_content):
    aisert1 = Aisert(sample_content)
    aisert2 = Aisert(sample_content)
    aisert1.semantic_matcher = MagicMock()
    aisert2.name = "other"
    aisert1.name = "self"
    aisert1.semantic_matcher.compare.return_value = True
    result = aisert1.assert_semantic_equals(aisert2)
    aisert1.semantic_matcher.compare.assert_called_once_with(
        aisert1.content, aisert2.content
    )
    assert result is True

def test_parse_config_returns_config(sample_content, sample_config):
    aisert = Aisert(sample_content)
    result = aisert._parse_config(sample_config)
    assert result == sample_config
