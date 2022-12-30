import pytest

from memory_atlas.mat_types import Range
from memory_atlas.models import BomVariable


def test_range_validation():
    with pytest.raises(AssertionError):
        Range(32, 16)


def test_variable_validation():
    var = BomVariable(name='foo', description='bar', var_type=Range(8, 16))
    var.validate()
