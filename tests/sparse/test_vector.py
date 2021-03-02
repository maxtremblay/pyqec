import pytest
from pyqec.sparse import BinaryVector

def test_access():
    vector = BinaryVector(5, [1, 3])
    assert vector[0] == 0
    assert vector[1] == 1
    assert vector[2] == 0
    assert vector[3] == 1
    assert vector[4] == 0

    with pytest.raises(IndexError):
        vector[5]

