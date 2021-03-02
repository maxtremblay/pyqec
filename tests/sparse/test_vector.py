import pytest
from pyqec.sparse import BinaryVector

def test_access():
    vector = BinaryVector(5, [1, 3])
    assert vector.element(0) == 0
    assert vector.element(1) == 1
    assert vector.element(2) == 0
    assert vector.element(3) == 1
    assert vector.element(4) == 0

    with pytest.raises(IndexError):
        vector.element(5)

