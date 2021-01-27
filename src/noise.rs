use crate::randomness::{get_rng_with_seed, RandomNumberGenerator};
use ldpc::noise_model::{BinarySymmetricChannel, NoiseModel};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

/// An implementation of a binary symmetric channel.
///
/// A binary symmetric channel flips the value
/// of each bits according to a given error probability.
#[pyclass(name = BinarySymmetricChannel)]
pub struct PyBinarySymmetricChannel {
    channel: BinarySymmetricChannel,
    rng: RandomNumberGenerator,
}

#[pymethods]
impl PyBinarySymmetricChannel {
    #[staticmethod]
    #[text_signature = "(probability)"]
    fn with_probability(probability: f64) -> PyResult<PyBinarySymmetricChannel> {
        let channel = BinarySymmetricChannel::try_with_probability(probability)
            .map_err(|error| PyValueError::new_err(error.to_string()))?;
        let rng = get_rng_with_seed(None);
        Ok(PyBinarySymmetricChannel { channel, rng })
    }

    #[staticmethod]
    #[text_signature = "(probability)"]
    fn with_probability_and_random_seed(
        probability: f64,
        seed: u64,
    ) -> PyResult<PyBinarySymmetricChannel> {
        let channel = BinarySymmetricChannel::try_with_probability(probability)
            .map_err(|error| PyValueError::new_err(error.to_string()))?;
        let rng = get_rng_with_seed(Some(seed));
        Ok(PyBinarySymmetricChannel { channel, rng })
    }

    #[text_signature = "(self, length)"]
    fn sample_error_of_length(&mut self, length: usize) -> Vec<usize> {
        self.channel
            .sample_error_of_length(length, &mut self.rng)
            .to_positions_vec()
    }
}
