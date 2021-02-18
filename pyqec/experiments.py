from math import sqrt
import json

class Statistics:
    def __init__(self):
        self.number_of_successes = 0
        self.number_of_failures = 0

    def add_failure(self):
        self.number_of_failures += 1

    def add_success(self):
        self.number_of_successes += 1

    def sample_size(self):
        return self.number_of_failures + self.number_of_successes

    def failure_rate(self):
        return self.number_of_failures / self.sample_size()

    def success_rate(self):
        return self.number_of_successes / self.sample_size()

    def uncertainty(self):
        assert(self.sample_size != 0)
        return sqrt(
            self.failure_rate() 
            * self.success_rate() 
            / self.sample_size()
        )

    def to_json(self):
        return json.dumps(
            {
                "number_of_failures": self.number_of_failures,
                "number_of_successes": self.number_of_successes,
            }
        )

    def from_json(self, source):
        return Statistics(
            source["number_of_failures"],
            source["number_of_successes"],
        )

    def __repr__(self):
        string =  "Statistics\n"
        string += "----------\n"
        string += f"sample size: {self.sample_size()}\n"
        string += f"failure rate: {self.failure_rate()}\n"
        string += f"success rate: {self.success_rate()}\n"
        string += f"uncertainty: {self.uncertainty()}"
        return string


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
        
        


