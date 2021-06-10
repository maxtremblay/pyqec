import json
from abc import ABC
from math import sqrt

import matplotlib.pyplot as plt
import multiprocess as mup


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
        assert self.sample_size != 0
        return sqrt(self.failure_rate() * self.success_rate() / self.sample_size())

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
        string = "Statistics\n"
        string += "----------\n"
        string += f"sample size: {self.sample_size()}\n"
        if self.sample_size() > 0:
            string += f"failure rate: {self.failure_rate()}\n"
            string += f"success rate: {self.success_rate()}\n"
            string += f"uncertainty: {self.uncertainty()}"
        return string


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


class ClassicalDecodingExperiment(DecodingExperiment):
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

    def to_json(self):
        return json.dumps(
            {
                "length": len(self.code),
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


class CssDecodingExperiment(DecodingExperiment):
    def __init__(self, code, x_decoder, z_decoder, noise):
        self.code = code
        self.x_decoder = x_decoder
        self.z_decoder = z_decoder
        self.noise = noise

    def run_once(self):
        """Runs a random decoding simulation and returns True if the process
        is successful. Else returns False.
        """
        error = self.noise.sample_error_of_length(len(self.code))
        (x_syndrome, z_syndrome) = self.code.syndrome_of(error)
        x_correction = self.x_decoder.decode(x_syndrome)
        z_correction = self.z_decoder.decode(z_syndrome)
        return self.code.has_stabilizer(x_correction.apply(z_correction).apply(error))

    def to_json(self):
        return json.dumps(
            {
                "length": len(self.code),
                "dimension": self.code.dimension(),
                "num_x_stabs": self.code.num_x_stabs(),
                "num_z_stabs": self.code.num_z_stabs(),
                "x_decoder": self.x_decoder.to_json(),
                "z_decoder": self.z_decoder.to_json(),
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
            decoder_tag = self.x_decoder.tag() + " / " + self.z_decoder.tag()
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


class Results:
    def __init__(self, tags=None, probabilities=None, statistics=None):
        if tags:
            self.tags = tags
        else:
            self.tags = list()
        if probabilities:
            self.probabilities = probabilities
        else:
            self.probabilities = list()
        if statistics:
            self.statistics = statistics
        else:
            self.statistics = list()

    def group_by_tag(self):
        tags_to_results = dict()
        for (tag, prob, stat) in zip(self.tags, self.probabilities, self.statistics):
            if tag not in tags_to_results:
                tags_to_results[tag] = Results()
            tags_to_results[tag].tags.append(tag)
            tags_to_results[tag].probabilities.append(prob)
            tags_to_results[tag].statistics.append(stat)
        return tags_to_results

    def filter_by_tag(self, condition):
        def condition_on_tuple(data):
            return condition(data[0])

        filtered = filter(
            condition_on_tuple, zip(self.tags, self.probabilities, self.statistics)
        )
        tags, probabilities, statistics = list(zip(*filtered))
        return Results(tags, probabilities, statistics)

    def failure_rates(self):
        return [stat.failure_rate() for stat in self.statistics]

    def uncertainties(self):
        return [stat.uncertainty() for stat in self.statistics]

    def plot(self, savepath=None):
        fig, ax = self.__setup_plot()
        results_by_tags = self.group_by_tag()
        for tag, results in results_by_tags.items():
            if tag == "":
                results.__plot_curve(ax)
            else:
                results.__plot_curve(ax, tag)
        self.__render_plot(ax, fig, self.__has_legend(results_by_tags), savepath)

    def __setup_plot(self):
        fig, ax = plt.subplots()
        ax.set_xlabel("Error probability")
        ax.set_ylabel("Failure rate")
        return fig, ax

    def __plot_curve(self, ax, label=None):
        if label:
            ax.errorbar(
                self.probabilities,
                self.failure_rates(),
                yerr=self.uncertainties(),
                marker="o",
                markersize=4,
                label=label,
            )
        else:
            ax.errorbar(
                self.probabilities,
                self.failure_rates(),
                yerr=self.uncertainties(),
                marker="o",
                markersize=4,
            )

    def __has_legend(self, results_by_tags):
        if len(results_by_tags) > 2:
            return True
        elif len(results_by_tags) == 1 and "" not in results_by_tags:
            return True
        else:
            return False

    def __render_plot(self, ax, fig, legend, savepath=None):
        if legend:
            ax.legend(frameon=False)
        if savepath:
            fig.savefig(savepath)


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
