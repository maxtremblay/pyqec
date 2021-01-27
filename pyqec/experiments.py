def sample_noise(code, noise_model):
    return noise_model.sample_error_of_length(code.block_size())

