"""Tests for utility functions."""
import pytest
from pathlib import Path
from code_analyzer.utils.helpers import get_file_type

def test_get_file_type():
    """Test file type detection."""
    assert get_file_type(Path("test.py")) == "python"
    assert get_file_type(Path("test.md")) == "markdown"
    assert get_file_type(Path("test.unknown")) == "unknown" 