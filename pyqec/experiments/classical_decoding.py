import json
from .statistics import Statistics

class ClassicalDecodingExperiment:
    def __init__(self, code, decoder, noise):
        self.code = code
        self.decoder = decoder
        self.noise = noise

    def run_once(self):
        """
            Run a single decoding simulation assuming a zero codeword.
        """
        error = self.noise.sample_error_of_length(len(self.code))
        codeword = self.decoder.decode(error)
        return codeword.is_zero()

    def run_while(self, condition):
        stats = Statistics()
        while condition(stats):
            if self.run_once():
                stats.add_success()
            else:
                stats.add_failure()
        return stats

    def run_n_times(self, number_of_iterations):
        return self.run_while(lambda s: s.sample_size() < number_of_iterations)

    def to_json(self):
        return json.dumps(
            {
                "length": len(self),
                "dimension": self.code.dimension(),
                "number_of_checks": self.code.number_of_checks(),
                "decoder": self.decoder.to_json(),
            }
        )
        
    def error_probability(self):
        return self.noise.error_probability()

    def tag(self):
        try:
            code_tag = self.code.tag()
        except:
            code_tag = None
        try:
            decoder_tag = self.decoder.tag()
        except:
            decoder_tag = None
        if code_tag and decoder_tag:
            return f"{code_tag} + {decoder_tag}"
        elif code_tag:
            return code_tag
        elif decoder_tag:
            return decoder_tag
        else:
            return ""
