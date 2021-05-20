from .pyqec import BinaryMatrix, BinaryVector
import numpy as np


def to_dense(bin_array):
    if isinstance(bin_array, BinaryMatrix):
        return _mat_to_dense(bin_array)
    elif isinstance(bin_array, BinaryVector):
        return _vec_to_dense(bin_array)
    else:
        raise ValueError("input must be a sparse binary matrix or vector")


def _mat_to_dense(matrix):
    array = np.zeros((matrix.number_of_rows(), matrix.number_of_columns()), dtype=np.int32)
    for row, cols in enumerate(matrix.rows()):
        for col in cols:
            array[row, col] = 1
    return array


def _vec_to_dense(vector):
    array = np.zeros(vector.len(), dtype=np.int32)
    for pos in vector:
        array[pos] = 1
    return array
