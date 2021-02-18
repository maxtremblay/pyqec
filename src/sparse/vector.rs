use pyo3::class::basic::CompareOp;
use pyo3::exceptions::{PyIndexError, PyNotImplementedError, PyValueError};
use pyo3::prelude::*;
use pyo3::{PyNumberProtocol, PyObjectProtocol};
use sparse_bin_mat::SparseBinVec;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

#[pyclass(name = BinaryVector)]
#[derive(Debug, PartialEq, Eq, Clone)]
pub struct PyBinaryVector {
    pub(crate) inner: SparseBinVec,
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

    pub fn weight(&self) -> usize {
        self.inner.weight()
    }

    pub fn is_empty(&self) -> bool {
        self.inner.is_empty()
    }

    pub fn is_zero(&self) -> bool {
        self.inner.is_zero()
    }

    pub fn is_zero_at(&self, index: usize) -> PyResult<bool> {
        self.inner.is_zero_at(index).ok_or_else(|| {
            PyIndexError::new_err(format!(
                "invalid index {} for vector of length {}",
                index,
                self.inner.len()
            ))
        })
    }

    pub fn is_one_at(&self, index: usize) -> PyResult<bool> {
        self.inner.is_one_at(index).ok_or_else(|| {
            PyIndexError::new_err(format!(
                "invalid index {} for vector of length {}",
                index,
                self.inner.len()
            ))
        })
    }

    pub fn concat(&self, other: PyRef<Self>) -> Self {
        self.inner.concat(&other.inner).into()
    }

    pub fn dot_with(&self, other: PyRef<Self>) -> PyResult<u8> {
        self.inner
            .dot_with(&other.inner)
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }
}

#[pyproto]
impl PyObjectProtocol for PyBinaryVector {
    fn __repr__(&self) -> String {
        self.inner.to_string()
    }

    fn __richcmp__(&self, other: PyRef<Self>, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Eq => Ok(&self.inner == &other.inner),
            CompareOp::Ne => Ok(&self.inner != &other.inner),
            _ => Err(PyNotImplementedError::new_err("not implemented")),
        }
    }

    fn __hash__(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.inner.hash(&mut hasher);
        hasher.finish()
    }
}

#[pyproto]
impl PyNumberProtocol for PyBinaryVector {
    fn __add__(lhs: PyRef<Self>, rhs: PyRef<Self>) -> PyResult<Self> {
        lhs.inner
            .bitwise_xor_with(&rhs.inner)
            .map(|vector| vector.into())
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }
}
