from .pyqec import BinaryMatrix, BinaryVector
import numpy as np


def to_dense(sparse_bin_array):
    """ Converts a sparse matrix or vector to a dense numpy representation.

    Arguments
    ---------
    sparse_bin_array : Union[BinaryMatrix, BinaryVector]
        The array to convert.

    Example
    -------
        >>> from pyqec.sparse import BinaryMatrix, to_dense
        >>> to_dense(BinaryMatrix.identity(3))
        array([[1, 0, 0],
               [0, 1, 0],
               [0, 0, 1]], dtype=int32)
    """
    if isinstance(sparse_bin_array, BinaryMatrix):
        return _mat_to_dense(sparse_bin_array)
    elif isinstance(sparse_bin_array, BinaryVector):
        return _vec_to_dense(sparse_bin_array)
    else:
        raise NotImplemented


def _mat_to_dense(matrix):
    array = np.zeros((matrix.num_rows(), matrix.num_columns()), dtype=np.int32)
    for row, cols in enumerate(matrix.rows()):
        for col in cols:
            array[row, col] = 1
    return array


def _vec_to_dense(vector):
    array = np.zeros(vector.len(), dtype=np.int32)
    for pos in vector:
        array[pos] = 1
    return array


def dot(left, right):
    """ Computes the dot product between two sparse binary arrays.

    Arguments
    ---------
    left : Union[BinaryMatrix, BinaryVector]
        The left hand side of the product.
    right : Union[BinaryMatrix, BinaryVector]
        The right hand side of the product.

    Examples
    --------
        >>> from pyqec.sparse import BinaryMatrix, BinaryVector, dot
        >>> matrix1 = BinaryMatrix(3, [[0, 1], [1, 2]])
        >>> matrix2 = BinaryMatrix(2, [[0], [1], [0, 1]])
        >>> dot(matrix1, matrix2)
        [0, 1]
        [0]
        >>> vector = BinaryVector(3, [0, 2])
        >>> dot(matrix1, vector)
        [0, 1]
        >>> dot(vector, matrix2)
        [1]
    """
    if isinstance(right, BinaryMatrix):
        return left.dot_with_matrix(right)
    elif isinstance(right, BinaryVector):
        return left.dot_with_vector(right)
    else:
        raise NotImplemented

def zeros(shape):
    """ Creates a vector or matrix filled with zeros.

    Arguments
    ---------
    shape: Union[int, Tuple[int, int]]
        If shape is a non-negative integer, this returns a vector.
        If it is a pair of non-negative integers, this returns a matrix.
    """
    if isinstance(shape, int):
        BinaryVector.zeros(shape)
    elif isinstance(shape, tuple[int, int]):
        BinaryMatrix.identity(*shape)
    else:
        raise NotImplemented

