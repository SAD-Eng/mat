import pytest

from memory_atlas.mat_types import Range


def test_range_validation():
    with pytest.raises(AssertionError):
        Range(32, 16)
