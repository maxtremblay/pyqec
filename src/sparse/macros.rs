macro_rules! reimplement_directly {
    ($function:ident, $return:ty) => {
        pub fn $function(&self) -> $return {
            self.inner.$function()
        }
    };
}

macro_rules! wrap_and_reimplement {
    ($function:ident) => {
        pub fn $function(&self) -> Self {
            Self::from(self.inner.$function())
        }
    };
}

macro_rules! reimplement_operator {
    ($function:ident) => {
        pub fn $function(&self, other: &Self) -> Self {
            Self::from(self.inner.$function(&other.inner))
        }
    };
}

macro_rules! reimplement_failable_operator {
    ($function:ident) => {
        pub fn $function(&self, other: &Self) -> PyResult<Self> {
            self.inner
                .$function(&other.inner)
                .map(|result| Self::from(result))
                .map_err(|error| PyValueError::new_err(error.to_string()))
        }
    };

    ($function:ident, $return:ty) => {
        pub fn $function(&self, other: &Self) -> PyResult<$return> {
            self.inner
                .$function(&other.inner)
                .map_err(|error| PyValueError::new_err(error.to_string()))
        }
    };
}

macro_rules! reimplement_with_indices {
    ($function:ident, $return:ty; $($index:ident),* ; $($type:ty),*) => {
        pub fn $function(&self, $($index: $type),*) -> PyResult<$return> {
            self.inner.$function($($index),*).ok_or_else(|| {
                PyValueError::new_err(format!("invalid indices {:?}", ($($index),*)))
            })
        }
    };
}
