from pyqec.sparse import BinaryMatrix, BinaryVector, to_dense
import pytest
import numpy as np


def test_row_iterations():
    matrix = BinaryMatrix(4, [[0, 1], [2, 3], [1, 2]])
    rows = matrix.rows()

    assert rows.__next__() == BinaryVector(4, [0, 1])
    assert rows.__next__() == BinaryVector(4, [2, 3])
    assert rows.__next__() == BinaryVector(4, [1, 2])

    with pytest.raises(StopIteration):
        rows.__next__()


def test_row_access():
    matrix = BinaryMatrix(4, [[0, 1], [2, 3], [1, 2]])
    assert matrix.row(2) == BinaryVector(4, [1, 2])
    with pytest.raises(IndexError):
        matrix.row(10)


def test_to_dense():
    matrix = BinaryMatrix(4, [[0, 1], [2, 3], [1, 2]])
    dense = to_dense(matrix)
    expected = np.array(
        [
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 1, 0],
        ]
    )
    np.testing.assert_array_equal(dense, expected)
