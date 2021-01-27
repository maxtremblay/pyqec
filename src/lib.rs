use pyo3::prelude::*;

mod linear_code;
use linear_code::PyLinearCode;

/// A toolbox for classical (and soon quantum) error correction.
#[pymodule]
fn pyqec(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyLinearCode>()?;

    Ok(())
}
