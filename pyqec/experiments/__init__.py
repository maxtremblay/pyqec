from pyqec.experiments.css_decoding import CssDecodingExperiment
from .statistics import Statistics
from .classical_decoding import ClassicalDecodingExperiment
from .laboratory import Laboratory
from .results import Results

from abc import ABC

class DecodingExperiment(ABC):
    def run_once(self):
        raise NotImplementedError
    
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

    def run_until_n_failures(self, number_of_failures):
        return self.run_while(lambda s: s.number_of_failures < number_of_failures)

    def run_until_n_successes(self, number_of_successes):
        return self.run_while(lambda s: s.number_of_successes < number_of_successes)

    def run_until_n_events(self, number_of_events):
        pass

    def error_probability(self):
        raise NotImplementedError
