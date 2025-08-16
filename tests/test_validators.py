"""Tests for individual validator functionality."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pydantic import BaseModel
from typing import List

from aisert.validators.schema_validator import SchemaValidator
from aisert.validators.contains_validator import ContainsValidator
from aisert.validators.semantic_validator import SemanticValidator
from aisert.validators.token_validator.token_validator import TokenValidator
from aisert.validators.token_validator.common_token_validators import OpenAITokenValidator
from aisert.exception import (
    SchemaValidationError,
    ContainsValidationError,
    SemanticValidationError,
    TokenValidationError
)


class TestUser(BaseModel):
    name: str
    age: int


class TestSchemaValidator:
    """Test SchemaValidator functionality."""

    def test_valid_pydantic_model(self):
        """Test validation with valid Pydantic model."""
        validator = SchemaValidator()
        content = '{"name": "John", "age": 30}'
        result = validator.validate(content, TestUser)
        assert result.status is True

    def test_invalid_pydantic_model(self):
        """Test validation with invalid data."""
        validator = SchemaValidator()
        content = '{"name": "John"}'  # missing age
        with pytest.raises(SchemaValidationError):
            validator.validate(content, TestUser)

    def test_list_validation(self):
        """Test validation with list of models."""
        validator = SchemaValidator()
        content = '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]'
        result = validator.validate(content, List[TestUser])
        assert result.status is True

    def test_invalid_json(self):
        """Test validation with invalid JSON."""
        validator = SchemaValidator()
        with pytest.raises(SchemaValidationError, match="Content is not a valid JSON"):
            validator.validate("invalid json", TestUser)

    def test_non_pydantic_schema(self):
        """Test validation with non-Pydantic schema."""
        validator = SchemaValidator()
        with pytest.raises(SchemaValidationError, match="not a valid Pydantic model"):
            validator.validate('{"test": "data"}', dict)

    def test_dict_input(self):
        """Test validation with dict input."""
        validator = SchemaValidator()
        content = {"name": "John", "age": 30}
        result = validator.validate(content, TestUser)
        assert result.status is True


class TestContainsValidator:
    """Test ContainsValidator functionality."""

    def test_contains_success(self):
        """Test successful contains validation."""
        validator = ContainsValidator()
        result = validator.validate("Hello world", ["Hello", "world"])
        assert result.status is True
        assert "Found all items" in result.reason

    def test_contains_partial_match(self):
        """Test partial contains validation."""
        validator = ContainsValidator()
        result = validator.validate("Hello world", ["Hello", "missing"])
        assert result.status is False
        assert "Missing items" in result.reason

    def test_not_contains_success(self):
        """Test successful not_contains validation."""
        validator = ContainsValidator(invert=True)
        result = validator.validate("Hello world", ["spam", "bad"])
        assert result.status is True
        assert "No flagged items found" in result.reason

    def test_not_contains_failure(self):
        """Test failed not_contains validation."""
        validator = ContainsValidator(invert=True)
        result = validator.validate("Hello world", ["Hello", "spam"])
        assert result.status is False
        assert "Found flagged items" in result.reason

    def test_invalid_items_type(self):
        """Test validation with invalid items type."""
        validator = ContainsValidator()
        with pytest.raises(ContainsValidationError, match="items must be a list"):
            validator.validate("test", "not_a_list")

    def test_empty_items_list(self):
        """Test validation with empty items list."""
        validator = ContainsValidator()
        result = validator.validate("Hello world", [])
        assert result.status is True


class TestSemanticValidator:
    """Test SemanticValidator functionality."""

    @patch('aisert.validators.semantic_validator.SentenceTransformer')
    @patch('aisert.validators.semantic_validator.util')
    def test_semantic_similarity_success(self, mock_util, mock_transformer):
        """Test successful semantic similarity validation."""
        mock_model = Mock()
        mock_model.encode.return_value = "mock_embedding"
        mock_transformer.return_value = mock_model
        mock_util.pytorch_cos_sim.return_value.item.return_value = 0.9
        
        validator = SemanticValidator("test-model")
        result = validator.validate("Hello world", "Hi world", 0.8)
        assert result.status is True
        assert "0.9" in result.reason

    @patch('aisert.validators.semantic_validator.SentenceTransformer')
    @patch('aisert.validators.semantic_validator.util')
    def test_semantic_similarity_failure(self, mock_util, mock_transformer):
        """Test failed semantic similarity validation."""
        mock_model = Mock()
        mock_model.encode.return_value = "mock_embedding"
        mock_transformer.return_value = mock_model
        mock_util.pytorch_cos_sim.return_value.item.return_value = 0.5
        
        validator = SemanticValidator("test-model")
        result = validator.validate("Hello", "Goodbye", 0.8)
        assert result.status is False
        assert "0.5" in result.reason

    def test_invalid_threshold(self):
        """Test validation with invalid threshold."""
        with patch('aisert.validators.semantic_validator.SentenceTransformer'):
            validator = SemanticValidator("test-model")
            with pytest.raises(SemanticValidationError, match="Threshold must be between 0 and 1"):
                validator.validate("test", "test", 1.5)

    def test_non_string_input(self):
        """Test validation with non-string input."""
        with patch('aisert.validators.semantic_validator.SentenceTransformer'):
            validator = SemanticValidator("test-model")
            with pytest.raises(SemanticValidationError, match="Both inputs must be strings"):
                validator.validate(123, "test", 0.8)

    def test_singleton_pattern(self):
        """Test singleton pattern for SemanticValidator."""
        with patch('aisert.validators.semantic_validator.SentenceTransformer'):
            validator1 = SemanticValidator.get_instance("test-model")
            validator2 = SemanticValidator.get_instance("test-model")
            assert validator1 is validator2


class TestTokenValidator:
    """Test TokenValidator functionality."""

    @patch('aisert.validators.token_validator.token_validator_factory.TokenValidatorFactory.get_instance')
    def test_token_validation_success(self, mock_factory):
        """Test successful token validation."""
        mock_validator = Mock()
        mock_validator.count.return_value = 5
        mock_factory.return_value = mock_validator
        
        validator = TokenValidator("openai")
        result = validator.validate("short text", token_limit=10, token_model="gpt-3.5-turbo")
        assert result.status is True
        assert "within limit" in result.reason

    @patch('aisert.validators.token_validator.token_validator_factory.TokenValidatorFactory.get_instance')
    def test_token_validation_failure(self, mock_factory):
        """Test failed token validation."""
        mock_validator = Mock()
        mock_validator.count.return_value = 15
        mock_factory.return_value = mock_validator
        
        validator = TokenValidator("openai")
        with pytest.raises(TokenValidationError, match="Token limit exceeded"):
            validator.validate("long text", token_limit=10, token_model="gpt-3.5-turbo")

    @patch('aisert.validators.token_validator.token_validator_factory.TokenValidatorFactory.get_instance')
    def test_dict_to_json_conversion(self, mock_factory):
        """Test dict to JSON conversion."""
        mock_validator = Mock()
        mock_validator.count.return_value = 5
        mock_factory.return_value = mock_validator
        
        validator = TokenValidator("openai")
        result = validator.validate({"key": "value"}, token_limit=10, token_model="gpt-3.5-turbo")
        
        # Verify JSON conversion was called
        mock_validator.count.assert_called_with('{"key": "value"}')
        assert result.status is True

    @patch('aisert.validators.token_validator.token_validator_factory.TokenValidatorFactory.get_instance')
    def test_list_to_json_conversion(self, mock_factory):
        """Test list to JSON conversion."""
        mock_validator = Mock()
        mock_validator.count.return_value = 5
        mock_factory.return_value = mock_validator
        
        validator = TokenValidator("openai")
        result = validator.validate([1, 2, 3], token_limit=10, token_model="gpt-3.5-turbo")
        
        # Verify JSON conversion was called
        mock_validator.count.assert_called_with('[1, 2, 3]')
        assert result.status is True


class TestOpenAITokenValidator:
    """Test OpenAITokenValidator functionality."""

    @patch('aisert.validators.token_validator.common_token_validators.tiktoken')
    def test_count_with_model(self, mock_tiktoken):
        """Test token counting with model."""
        mock_encoding = Mock()
        mock_encoding.encode.return_value = [1, 2, 3, 4, 5]
        mock_tiktoken.encoding_for_model.return_value = mock_encoding
        
        validator = OpenAITokenValidator.get_instance(token_model="gpt-3.5-turbo")
        count = validator.count("test text")
        assert count == 5

    @patch('aisert.validators.token_validator.common_token_validators.tiktoken')
    def test_count_with_encoding(self, mock_tiktoken):
        """Test token counting with encoding."""
        mock_encoding = Mock()
        mock_encoding.encode.return_value = [1, 2, 3]
        mock_tiktoken.get_encoding.return_value = mock_encoding
        mock_tiktoken.list_encodings.return_value = ["cl100k_base"]
        
        validator = OpenAITokenValidator.get_instance(token_encoding="cl100k_base")
        count = validator.count("test")
        assert count == 3

    def test_missing_parameters(self):
        """Test validation with missing parameters."""
        with pytest.raises(TokenValidationError, match="Either token_encoding or token_model must be provided"):
            OpenAITokenValidator.get_instance()

    def test_singleton_pattern(self):
        """Test singleton pattern for OpenAITokenValidator."""
        with patch('aisert.validators.token_validator.common_token_validators.tiktoken'):
            validator1 = OpenAITokenValidator.get_instance(token_model="gpt-3.5-turbo")
            validator2 = OpenAITokenValidator.get_instance(token_model="gpt-3.5-turbo")
            assert validator1 is validator2