use pyo3::prelude::*;

mod linear_code;
use linear_code::{random_regular_code, hamming_code, repetition_code, PyLinearCode};

mod noise;
use noise::PyBinarySymmetricChannel;

mod flip_decoder;
use flip_decoder::PyFlipDecoder;

mod randomness;

mod sparse;
use sparse::{PyBinaryMatrix, PyBinaryVector};

/// A toolbox for classical (and soon quantum) error correction.
#[pymodule]
fn pyqec(_py: Python, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyLinearCode>()?;
    module.add_class::<PyBinarySymmetricChannel>()?;
    module.add_class::<PyFlipDecoder>()?;
    module.add_class::<PyBinaryMatrix>()?;
    module.add_class::<PyBinaryVector>()?;

    /// Samples a random regular codes.
    ///
    /// Parameters
    /// ----------
    /// num_bits: int
    ///     The number of bits in the code.
    /// num_checks: int, default = 3
    ///     The number of checks in the code.
    /// bit_degree: int
    ///     The number of checks connected to each bit.
    /// check_degree: int
    ///     The number of bits connected to each check.
    /// random_seed: Optional[int]
    ///     A seed to feed the random number generator.
    ///     By default, the rng is initialize from entropy.
    /// tag: Optional[string]
    ///     An identifier for the code.
    ///
    /// Returns
    /// -------
    /// LinearCode
    ///     A random linear code with the given parameters.
    ///
    /// Raises
    /// ------
    /// ValueError
    ///     If `block_size * bit_degree != number_of_checks * check_degree`.
    #[pyfn(module, "random_regular_code")]
    #[text_signature = "(num_bits=4, num_checks=3, bit_degree=3, check_degree=4, random_seed=None, tag=None)"]
    fn py_random_regular_code(
        num_bits: usize,
        num_checks: usize,
        bit_degree: usize,
        check_degree: usize,
        random_seed: Option<u64>,
        tag: Option<String>,
    ) -> PyResult<PyLinearCode> {
        random_regular_code(
            num_bits,
            num_checks,
            bit_degree,
            check_degree,
            random_seed,
            tag,
        )
    }


    /// Returns an instance of the Hamming code.
    ///
    /// Arguments
    /// ---------
    /// tag : Optional[String]
    ///     A label for the code used to save data
    ///     and make automatic legend in plots.
    #[pyfn(module, "hamming_code")]
    #[text_signature = "(tag=None)"]
    pub fn py_hamming_code(tag: Option<String>) -> PyLinearCode {
        hamming_code(tag)
    }

    /// Returns an instance of the repetition code.
    ///
    /// Arguments
    /// ---------
    /// length : Int
    ///     The number of bits.
    /// tag : Optional[String]
    ///     A label for the code used to save data
    ///     and make automatic legend in plots.
    #[pyfn(module, "repetition_code")]
    #[text_signature = "(length, tag=None)"]
    pub fn py_repetition_code(length: usize, tag: Option<String>) -> PyLinearCode {
        repetition_code(length, tag)
    }

    Ok(())
}
