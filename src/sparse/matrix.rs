use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use sparse_bin_mat::SparseBinMat;

#[pyclass(name = BinaryMatrix)]
#[derive(Debug, Clone)]
pub struct PyBinaryMatrix {
    pub(crate) inner: SparseBinMat,
}

impl From<SparseBinMat> for PyBinaryMatrix {
    fn from(inner: SparseBinMat) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl PyBinaryMatrix {
    #[new]
    pub fn new(number_of_columns: usize, rows: Vec<Vec<usize>>) -> PyResult<Self> {
        let matrix = SparseBinMat::try_new(number_of_columns, rows)
            .map_err(|error| PyValueError::new_err(error.to_string()))?;
        Ok(Self::from(matrix))
    }

    #[staticmethod]
    pub fn identity(length: usize) -> Self {
        Self::from(SparseBinMat::identity(length))
    }

    #[staticmethod]
    pub fn zeros(number_of_rows: usize, number_of_columns: usize) -> Self {
        Self::from(SparseBinMat::zeros(number_of_rows, number_of_columns))
    }

    #[staticmethod]
    pub fn empty() -> Self {
        Self::from(SparseBinMat::empty())
    }

    reimplement_directly!(number_of_columns, usize);
    reimplement_directly!(number_of_rows, usize);
    reimplement_directly!(dimension, (usize, usize));
    reimplement_directly!(number_of_zeros, usize);
    reimplement_directly!(number_of_ones, usize);
    reimplement_directly!(is_empty, bool);
    reimplement_directly!(is_zero, bool);
    reimplement_directly!(rank, usize);

    wrap_and_reimplement!(transposed);
    wrap_and_reimplement!(echelon_form);
    wrap_and_reimplement!(nullspace);

    reimplement_with_indices!(is_zero_at, bool; row, column; usize, usize);
    reimplement_with_indices!(is_one_at, bool; row, column; usize, usize);

    reimplement_operator!(horizontal_concat_with);
    reimplement_operator!(vertical_concat_with);
    reimplement_failable_operator!(dot_with_matrix);
}
