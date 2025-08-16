"""Tests for model classes."""
import pytest

from aisert.models.report import AisertReport
from aisert.models.result import Result, AisertStatus


class TestResult:
    """Test Result model functionality."""

    def test_result_creation(self):
        """Test Result creation with status and reason."""
        result = Result(True, "Success message")
        assert result.status is True
        assert result.reason == "Success message"

    def test_result_to_dict(self):
        """Test Result to_dict conversion."""
        result = Result(False, "Error message")
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict['status'] is False
        assert result_dict['reason'] == "Error message"

    def test_result_str_representation(self):
        """Test Result string representation."""
        result = Result(True, "Test reason")
        str_repr = str(result)
        assert "True" in str_repr
        assert "Test reason" in str_repr


class TestAisertStatus:
    """Test AisertStatus functionality."""

    def test_aisert_status_creation(self):
        """Test AisertStatus initialization."""
        status = AisertStatus()
        assert isinstance(status.results, dict)
        assert len(status.results) == 0

    def test_update_status(self):
        """Test updating status with validator results."""
        status = AisertStatus()
        result = Result(True, "Success")
        
        status.update("TestValidator", result)
        assert "TestValidator" in status.results
        assert status.results["TestValidator"] == result

    def test_collect_results(self):
        """Test collecting all results."""
        status = AisertStatus()
        result1 = Result(True, "Success 1")
        result2 = Result(False, "Error 2")
        
        status.update("Validator1", result1)
        status.update("Validator2", result2)
        
        collected = status.collect()
        assert len(collected) == 2
        assert collected["Validator1"] == result1
        assert collected["Validator2"] == result2

    def test_multiple_updates_same_validator(self):
        """Test multiple updates to same validator overwrites."""
        status = AisertStatus()
        result1 = Result(True, "First")
        result2 = Result(False, "Second")
        
        status.update("TestValidator", result1)
        status.update("TestValidator", result2)
        
        collected = status.collect()
        assert len(collected) == 1
        assert collected["TestValidator"] == result2


class TestAisertReport:
    """Test AisertReport functionality."""

    def test_report_creation(self):
        """Test AisertReport creation."""
        rules = {
            "Validator1": {"status": True, "reason": "Success"},
            "Validator2": {"status": False, "reason": "Error"}
        }
        report = AisertReport(status=False, rules=rules)
        
        assert report.status is False
        assert report.rules == rules

    def test_report_str_representation(self):
        """Test AisertReport string representation."""
        rules = {"TestValidator": {"status": True, "reason": "OK"}}
        report = AisertReport(status=True, rules=rules)
        
        str_repr = str(report)
        assert "Status: True" in str_repr
        assert "Rules:" in str_repr

    def test_report_with_empty_rules(self):
        """Test AisertReport with empty rules."""
        report = AisertReport(status=True, rules={})
        assert report.status is True
        assert report.rules == {}

    def test_report_attributes_access(self):
        """Test direct attribute access on AisertReport."""
        rules = {"Validator": {"status": True, "reason": "Good"}}
        report = AisertReport(status=True, rules=rules)
        
        # Test direct attribute access
        assert hasattr(report, 'status')
        assert hasattr(report, 'rules')
        assert report.status is True
        assert report.rules == rules

    def test_report_with_complex_rules(self):
        """Test AisertReport with complex nested rules."""
        rules = {
            "SchemaValidator": {
                "status": True,
                "reason": "Schema validation passed",
                "details": {"fields_validated": ["name", "age"]}
            },
            "ContainsValidator": {
                "status": False,
                "reason": "Missing items: ['required_field']",
                "missing_items": ["required_field"]
            }
        }
        
        report = AisertReport(status=False, rules=rules)
        assert report.status is False
        assert len(report.rules) == 2
        assert report.rules["SchemaValidator"]["status"] is True
        assert report.rules["ContainsValidator"]["status"] is False