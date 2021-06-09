from pyqec.experiments.css_decoding import CssDecodingExperiment
import multiprocess as mup
from .results import Results


class Laboratory:
    def __init__(self, number_of_processes=None):
        self.experiments = list()
        self.number_of_processes = number_of_processes
        self.stopping_condition = None

    def add_experiment(self, experiment):
        self.experiments.append(experiment)

    def run_all_experiments_while(self, condition):
        return self.__run_all(lambda experiment: experiment.run_while(condition))

    def run_all_experiments_n_times(self, number_of_iterations):
        def runner(experiment):
            return experiment.run_n_times(number_of_iterations)

        return self.__run_all(runner)

    def run_all_experiments_until_n_events(self, n):
        """
        Run each experiment until n successes and n failures are obtained
        """

        def condition(statistics):
            return (
                statistics.number_of_successes < n and statistics.number_of_failures < n
            )

        self.run_all_experiments_while(condition)

    def error_probabilities(self):
        return [experiment.error_probability() for experiment in self.experiments]

    def tags(self):
        return [experiment.tag() for experiment in self.experiments]

    def __number_of_processes(self):
        if self.number_of_processes:
            return self.number_of_processes
        else:
            return 1

    def __run_all(self, runner):
        with mup.Pool(self.__number_of_processes()) as pool:
            statistics = pool.map(runner, self.experiments)
            return Results(self.tags(), self.error_probabilities(), statistics)
