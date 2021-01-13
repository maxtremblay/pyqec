use ldpc::{LinearCode, SparseBinMat, SparseBinSlice};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::PyObjectProtocol;
use rand::SeedableRng;
use rand_xoshiro::Xoshiro512StarStar;

/// An implementation of linear codes optimized for LDPC codes.
///
/// A code can be defined from either a parity check matrix `H`
/// or a generator matrix `G`.
/// These matrices have the property that `H G^T = 0`.
///
/// # Example
///
/// This is example shows 2 way to define the Hamming code.
///
/// ```
/// # From a list of checks.
/// code_from_checks = LinearCode.from_checks(
///     7,
///     [[0, 1, 2, 4], [0, 1, 3, 5], [0, 2, 3, 6]]
/// )
///
/// # From a list of codeword generators.
/// code_from_generators = LinearCode.from_generators(
///     7,
///     [[0, 4, 5, 6], [1, 4, 5], [2, 4, 6], [3, 5, 6]]
/// )
///
/// assert code_from_checks.has_same_codespace_as(code_from_generators)
/// ```
///
/// # Comparison
///
/// Use the `==` if you want to know if 2 codes
/// have exactly the same parity check matrix and
/// generator matrix.
/// However, since there is freedom in the choice of
/// parity check matrix and generator matrix for the same code,
/// use `has_same_codespace_as` method
/// if you want to know if 2 codes define the same codespace even
/// if they may have different parity check matrix or generator matrix.
#[pyclass(name = LinearCode)]
struct PyLinearCode {
    inner: LinearCode,
}

impl From<LinearCode> for PyLinearCode {
    fn from(inner: LinearCode) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl PyLinearCode {
    /// Constructs a LinearCode from a parity check matrix.
    ///
    /// # Parameters
    /// block_size: int
    ///     The number of bits in the code.
    /// checks: list of list of int
    ///     A list of checks where each check is represented by the
    ///     list of positions where this check has value 1.
    ///
    /// # Returns
    /// LinearCode
    ///     The linear code with the given checks.
    ///
    /// # Raises
    ///
    #[staticmethod]
    #[text_signature = "(block_size, checks)"]
    fn from_checks(block_size: usize, checks: Vec<Vec<usize>>) -> PyLinearCode {
        let matrix = SparseBinMat::new(block_size, checks);
        PyLinearCode {
            inner: LinearCode::from_parity_check_matrix(matrix),
        }
    }

    #[staticmethod]
    #[text_signature = "(block_size, generators)"]
    fn from_generators(block_size: usize, generators: Vec<Vec<usize>>) -> PyLinearCode {
        let matrix = SparseBinMat::new(block_size, generators);
        PyLinearCode {
            inner: LinearCode::from_generator_matrix(matrix),
        }
    }

    #[staticmethod]
    #[args(block_size = 4, number_of_checks = 3, bit_degree = 3, check_degree = 4)]
    #[text_signature = "(block_size, number_of_checks, bit_degree, check_degree, random_seed)"]
    fn random_regular_code(
        block_size: usize,
        number_of_checks: usize,
        bit_degree: usize,
        check_degree: usize,
        random_seed: Option<u64>,
    ) -> PyResult<Self> {
        let mut rng = if let Some(seed) = random_seed {
            Xoshiro512StarStar::seed_from_u64(seed)
        } else {
            Xoshiro512StarStar::from_entropy()
        };
        LinearCode::random_regular_code()
            .block_size(block_size)
            .number_of_checks(number_of_checks)
            .bit_degree(bit_degree)
            .check_degree(check_degree)
            .sample_with(&mut rng)
            .map(|code| code.into())
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }

    #[text_signature = "($self)"]
    fn block_size(&self) -> usize {
        self.inner.block_size()
    }

    #[text_signature = "($self)"]
    fn dimension(&self) -> usize {
        self.inner.dimension()
    }

    #[text_signature = "($self)"]
    fn minimal_distance(&self) -> i64 {
        self.inner
            .minimal_distance()
            .map(|d| d as i64)
            .unwrap_or(-1)
    }

    #[text_signature = "($self)"]
    fn number_of_checks(&self) -> usize {
        self.inner.number_of_checks()
    }

    #[text_signature = "($self)"]
    fn number_of_generators(&self) -> usize {
        self.inner.number_of_generators()
    }

    #[text_signature = "($self)"]
    fn parity_check_matrix(&self) -> Vec<Vec<usize>> {
        self.inner
            .parity_check_matrix()
            .rows()
            .map(|row| row.as_slice().to_owned())
            .collect()
    }

    #[text_signature = "($self)"]
    fn generator_matrix(&self) -> Vec<Vec<usize>> {
        self.inner
            .generator_matrix()
            .rows()
            .map(|row| row.as_slice().to_owned())
            .collect()
    }

    #[text_signature = "($self, message)"]
    fn syndrome_of(&self, mut message: Vec<usize>) -> PyResult<Vec<usize>> {
        let vector = SparseBinSlice::new(self.inner.block_size(), &mut message);
        self.inner
            .syndrome_of(&vector)
            .map(|syndrome| syndrome.to_positions_vec())
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }

    #[text_signature = "($self, message)"]
    fn has_codeword(&self, mut message: Vec<usize>) -> PyResult<bool> {
        SparseBinSlice::try_new(self.inner.block_size(), &mut message)
            .map(|vector| self.inner.has_codeword(&vector).unwrap())
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }

    #[text_signature = "($self, other)"]
    fn has_same_codespace_as(&self, other: &Self) -> bool {
        self.inner.has_the_same_codespace_as(&other.inner)
    }
}
#[pyproto]
impl PyObjectProtocol for PyLinearCode {
    fn __repr__(&self) -> String {
        format!(
            "Parity check matrix:\n{}\nGenerator matrix:\n{}",
            self.inner.parity_check_matrix(),
            self.inner.generator_matrix(),
        )
    }
}

#[pymodule]
fn pyqec(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyLinearCode>()?;

    Ok(())
}
