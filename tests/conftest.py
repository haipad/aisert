"""Pytest configuration and fixtures."""
import pytest
import sys
import os

# Add the parent directory to the path so we can import aisert
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_config():
    """Fixture providing a sample AisertConfig."""
    from aisert import AisertConfig
    return AisertConfig(
        token_model="gpt-3.5-turbo",
        model_provider="openai",
        sentence_transformer_model="all-MiniLM-L6-v2"
    )


@pytest.fixture
def sample_json_data():
    """Fixture providing sample JSON data."""
    return '{"name": "John Doe", "email": "john@example.com", "age": 30}'


@pytest.fixture
def sample_json_list():
    """Fixture providing sample JSON list data."""
    return [
        {"name": "John", "email": "john@example.com", "age": 30},
        {"name": "Jane", "email": "jane@example.com", "age": 25}
    ]


@pytest.fixture
def sample_text():
    """Fixture providing sample text content."""
    return "This is a sample text for testing purposes."


@pytest.fixture
def mock_token_validator():
    """Fixture providing a mock token validator."""
    from unittest.mock import Mock
    mock_validator = Mock()
    mock_validator.count.return_value = 10
    return mock_validator


@pytest.fixture
def mock_semantic_validator():
    """Fixture providing a mock semantic validator."""
    from unittest.mock import Mock
    from aisert.models.result import Result
    
    mock_validator = Mock()
    mock_validator.validate.return_value = Result(True, "Semantic match found")
    return mock_validator