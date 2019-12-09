import csv
import ctypes
import os
import shutil
from copy import copy
from multiprocessing.pool import Pool
from typing import Dict, List

import matplotlib.pyplot as plt

from hestia.connection_parameters import ConnectionParameters
from hestia.experiment import Experiment
from hestia.model import Model


class MyExperimentParameters:
    def __init__(self):
        self.num_transactions = 100
        self.latencies = [1]
        self.capacities = [1]
        self.read_rates = [1]
        self.write_rates = [1]


class MyExperiment(Experiment):
    def __init__(self, name: str, path: str, params: MyExperimentParameters = MyExperimentParameters()):
        super(MyExperiment, self).__init__(name)
        self.path = path
        self.params = copy(params)
        self.domain = "clk"

        self.create_tests()

    def create_tests(self) -> None:
        params = ConnectionParameters()
        params.domain = ctypes.c_char_p(self.domain.encode("utf-8"))
        params.is_timed = True
        for read_rate in self.params.read_rates:
            for write_rate in self.params.write_rates:
                for latency in self.params.latencies:
                    for capacity in self.params.capacities:
                        model = Model(self.path)
                        model.add_clock_domain(self.domain, 1)
                        test_name = "r_{}.w_{}.l_{}.c_{}".format(read_rate, write_rate, latency, capacity)

                        test = NumberTestBench(test_name, self.domain)
                        test.set_num_transactions(self.params.num_transactions)
                        params.read_rate = read_rate
                        params.write_rate = write_rate
                        params.latency = latency
                        params.capacity = capacity
                        test.set_connection_params(params)
                        test.build(model)

                        model.attach_basic_stats_to_connections()

                        model.create_csv_sampler("sampler", "counters.csv", 1, "clk")
                        model.attach_counters_to_sampler("sampler", ".*\.stats\..*")

                        self.tests[test.name] = model

    @staticmethod
    def get_data(test: str) -> Dict[str, List[int]]:
        results = {"production": [], "consumption": []}
        with open(os.path.join(test, "counters.csv"), 'r') as f:
            data = csv.DictReader(f)
            for row in data:
                for column in row:
                    if column.endswith("stats.pushed"):
                        results["production"].append(row[column])
                    elif column.endswith("stats.popped"):
                        results["consumption"].append(row[column])

        # Remove idle portion of end of test
        results["production"] = results["production"][:-10]
        results["consumption"] = results["consumption"][:-10]
        return results

    @staticmethod
    def generate_report(name: str):
        data = MyExperiment.get_data(name)
        plt.plot(data["production"], label="Write", drawstyle="steps")
        plt.plot(data["consumption"], label="Read", drawstyle="steps")
        plt.xlabel("Clocks")
        plt.ylabel("Transactions")
        plt.legend()
        plt.savefig(os.path.join("results", name + ".png"))
        plt.clf()

    def generate_reports(self, number_of_jobs: int = 4):
        if os.path.exists("results"):
            shutil.rmtree("results")
        os.mkdir("results")
        with Pool(number_of_jobs) as p:
            p.map(MyExperiment.generate_report, self.tests.keys())



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
    params.num_transactions = 20
    params.read_rates = [1, 2, 3, 5, 10]
    params.write_rates = copy(params.read_rates)
    params.latencies = copy(params.read_rates)
    params.capacities = copy(params.read_rates)
    experiment = MyExperiment("my_experiment", args.model_path, params)
    experiment.run(10)
    experiment.generate_reports()
    os.chdir("..")

if __name__ == "__main__":
    run()
