import pytest
from pyqec.sparse import BinaryVector, to_dense
import numpy as np


def test_access():
    vector = BinaryVector(5, [1, 3])
    assert vector.element(0) == 0
    assert vector.element(1) == 1
    assert vector.element(2) == 0
    assert vector.element(3) == 1
    assert vector.element(4) == 0

    with pytest.raises(IndexError):
        vector.element(5)


def test_to_dense():
    vector = BinaryVector(5, [1, 3])
    dense = to_dense(vector)
    expected = np.array([0, 1, 0, 1, 0])
    np.testing.assert_array_equal(dense, expected)
