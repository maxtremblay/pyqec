from pyqec.sparse import BinaryMatrix, BinaryVector
from pyqec.classical import LinearCode, BinarySymmetricChannel, repetition_code
from pyqec.experiments import ClassicalDecodingExperiment, Laboratory


class MajorityDecoder:
    def __init__(self, code):
        self.code = code
        length = len(code)
        self.limit = (length - 1) / 2
        self.zero_codeword = BinaryVector(length, list())
        self.one_codeword = BinaryVector(length, list(range(length)))

    def decode(self, message):
        if message.weight() > self.limit:
            return self.one_codeword
        else:
            return self.zero_codeword


def build_experiment(code_length, probability):
    code = repetition_code(code_length, f"n = {code_length}")
    decoder = MajorityDecoder(code)
    noise = BinarySymmetricChannel(probability)
    return ClassicalDecodingExperiment(code, decoder, noise)


laboratory = Laboratory(8)  # I have 8 CPUs on my machine.

for length in range(1, 10, 2):
    for probability in (0.05 * p for p in range(1, 21)):
        laboratory.add_experiment(build_experiment(length, probability))

results = laboratory.run_all_experiments_n_times(1000)
results.plot("repetition_codes.pdf")
