use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use sparse_bin_mat::SparseBinVec;

#[pyclass(name = BinaryVector)]
pub struct PyBinaryVector {
    inner: SparseBinVec,
}

impl From<SparseBinVec> for PyBinaryVector {
    fn from(vector: SparseBinVec) -> Self {
        Self { inner: vector }
    }
}

#[pymethods]
impl PyBinaryVector {
    #[new]
    fn new(length: usize, non_trivial_positions: Vec<usize>) -> PyResult<Self> {
        SparseBinVec::try_new(length, non_trivial_positions)
            .map(|vector| Self::from(vector))
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }

    #[staticmethod]
    pub fn zeros(length: usize) -> Self {
        Self::from(SparseBinVec::zeros(length))
    }

    #[staticmethod]
    pub fn empty() -> Self {
        Self::from(SparseBinVec::empty())
    }

    reimplement_directly!(weight, usize);
    reimplement_directly!(is_empty, bool);
    reimplement_directly!(is_zero, bool);

    reimplement_with_indices!(is_zero_at, bool; position; usize);
    reimplement_with_indices!(is_one_at, bool; position; usize);

    reimplement_operator!(concat);

    reimplement_failable_operator!(dot_with, u8);
}
