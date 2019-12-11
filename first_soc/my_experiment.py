import json
import operator
import os
import shutil
from copy import copy

from hestia.experiment import Experiment
from hestia.memory_parameters import MemoryParameters
from hestia.model import Model

from first_soc.containers import PipelinedTestBench


class MyExperimentParameters:
    def __init__(self):
        self.num_operations_per_iteration = 100
        self.num_iterations = 100
        self.instruction_rates = [1,2]
        self.data_rates = [1,2,3,4,5]
        self.fetcher_rates = copy(self.data_rates)
        self.decoder_rates = copy(self.data_rates)
        self.executor_rates = copy(self.data_rates)
        self.write_back_rates = copy(self.data_rates)


def calculate_area(name: str) -> int:
    rates = name.split(".")
    result = 0
    for rate in rates:
        result += int(rate.split("_")[-1])
    return result


class MyExperiment(Experiment):
    def __init__(self, name: str, path: str, params: MyExperimentParameters = MyExperimentParameters()):
        super(MyExperiment, self).__init__(name)
        self.path = path
        self.params = copy(params)
        self.domain = "clk"

        self.create_tests()

    def create_tests(self) -> None:

        for instruction_rate in self.params.instruction_rates:
            for data_rate in self.params.data_rates:
                for fetcher_rate in self.params.fetcher_rates:
                    for decoder_rate in self.params.decoder_rates:
                        for executor_rate in self.params.executor_rates:
                            for write_back_rates in self.params.write_back_rates:
                                model = Model(self.path)
                                model.add_clock_domain(self.domain, 1)

                                memory_name = "mem"
                                memory_params = MemoryParameters()
                                memory_params.discrete = False
                                memory_params.size = 1024

                                model.create_memory(memory_name, memory_params)


                                test_name = "i_{}.d_{}.f_{}.d_{}.e_{}.w_{}".format(instruction_rate, data_rate, fetcher_rate, decoder_rate, executor_rate, write_back_rates)

                                test = PipelinedTestBench(test_name, self.domain, memory_name)
                                test.set_instruction_memory_params(rate=instruction_rate, capacity=10, latency=0)
                                test.set_data_memory_params(rate=data_rate, capacity=10, latency=0)
                                test.set_fetcher_params(rate=fetcher_rate, capacity=10, latency=0)
                                test.set_decoder_params(rate=decoder_rate, capacity=10, latency=0)
                                test.set_executor_params(rate=executor_rate, capacity=10, latency=0)
                                test.set_write_back_params(rate=write_back_rates, capacity=10, latency=0)

                                test.build(model)

                                self.tests[test.name] = model

    def generate_report(self):
        if os.path.exists("results"):
            shutil.rmtree("results")
        os.mkdir("results")
        os.chdir("results")
        test_times = {}
        for test in self.tests:
            test_times[test] = self.tests[test].get_time()

        with open("top_5.json", 'w') as f:
            json.dump(dict(sorted(test_times.items(), key=operator.itemgetter(1))[:5]), f)

        with open("top_10.json", 'w') as f:
            json.dump(dict(sorted(test_times.items(), key=operator.itemgetter(1))[:10]), f)

        with open("all.json", 'w') as f:
            json.dump(dict(sorted(test_times.items(), key=operator.itemgetter(1))), f)

        winner = {"name": "", "clocks": 0, "area" : 0}
        for test in test_times:
            is_winner = False
            if winner["clocks"] is 0:
                is_winner = True
            elif test_times[test] < winner["clocks"]:
                is_winner = True
            elif test_times[test] == winner["clocks"] and winner["area"] > calculate_area(test):
                is_winner = True

            if is_winner:
                winner["name"] = test
                winner["clocks"] = test_times[test]
                winner["area"] = calculate_area(test)

        with open("winner.json", 'w') as f:
            json.dump(winner, f)

        os.chdir("..")


def run():
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('model_path', type=str,
                        help='Path to the sandbox model (libsandbox.so)')

    parser.add_argument('-d', '--run-directory', type=str, dest='run_directory', action='store',
                        default="_experiment",help='Path to the run directory')

    args = parser.parse_args()

    if os.path.exists("_tests"):
        shutil.rmtree("_tests")
    os.mkdir("_tests")
    os.chdir("_tests")
    params = MyExperimentParameters()
    experiment = MyExperiment("my_experiment", args.model_path, params)
    experiment.run(4)
    experiment.generate_report()
    os.chdir("..")

if __name__ == "__main__":
    run()
