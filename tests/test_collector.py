"""
Tests for the collector module
"""
import pytest
from collector_core.collector import Collector


def test_collector_initialization():
    """Test that a collector can be initialized with a name"""
    collector = Collector(name="test_collector")
    assert collector.name == "test_collector"


def test_collector_collect():
    """Test that collect returns expected structure"""
    collector = Collector(name="test_collector")
    data = collector.collect()
    
    assert isinstance(data, dict)
    assert "collector" in data
    assert "data" in data
    assert data["collector"] == "test_collector"
    assert data["data"] == []
