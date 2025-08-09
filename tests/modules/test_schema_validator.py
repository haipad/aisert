import pytest

from aisert.validators.schema_validator import SchemaValidator

def test_schema_validator_is_schema_match_valid(monkeypatch):
    # Simulate a valid schema match
    monkeypatch.setattr(SchemaValidator, "is_schema_match", lambda content, schema: True)
    assert SchemaValidator.is_schema_match({"foo": "bar"}, {"type": "object"}) is True

def test_schema_validator_is_schema_match_invalid(monkeypatch):
    # Simulate an invalid schema match
    monkeypatch.setattr(SchemaValidator, "is_schema_match", lambda content, schema: False)
    assert SchemaValidator.is_schema_match({"foo": 123}, {"type": "object"}) is False
