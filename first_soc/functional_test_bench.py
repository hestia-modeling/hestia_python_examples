import argparse

from containers import FunctionalTestBench
from hestia.memory_parameters import MemoryParameters

from hestia.model import Model
from hestia.sink_parameters import SinkParameters, SinkType

from first_soc.containers import MemoryBoundTestBench, PerformantTestBench, PipelinedTestBench


def main():
    # User's can provide the path to their test bench library
    parser = argparse.ArgumentParser(description="Run a python test bench")
    parser.add_argument("model_path", metavar='B', type=str, help="Path to the model shared library")
    args = parser.parse_args()

    # Initialize the
    functional_model = Model(args.model_path)
    memory_bound_model = Model(args.model_path)
    performant_model = Model(args.model_path)
    pipelined_model = Model(args.model_path)

    # Add Clock Domain
    domain = "clk"
    functional_model.add_clock_domain(domain, 1)
    memory_bound_model.add_clock_domain(domain, 1)
    performant_model.add_clock_domain(domain, 1)
    pipelined_model.add_clock_domain(domain, 1)

    memory_name = "mem"
    memory_params = MemoryParameters()
    memory_params.discrete = False
    memory_params.size = 1024
    functional_model.create_memory(memory_name, memory_params)
    memory_bound_model.create_memory(memory_name, memory_params)
    performant_model.create_memory(memory_name, memory_params)
    pipelined_model.create_memory(memory_name, memory_params)

    # Create our test bench container
    functional_test_bench = FunctionalTestBench("functional_test_bench", domain, memory_name)
    memory_bound_test_bench = MemoryBoundTestBench("memory_bound_test_bench", domain, memory_name)
    performant_test_bench = PerformantTestBench("performant_test_bench", domain, memory_name)
    pipelined_test_bench = PipelinedTestBench("pipelined_test_bench", domain, memory_name)

    # Build our test bench in our model

    functional_test_bench.build(functional_model)
    memory_bound_test_bench.build(memory_bound_model)
    performant_test_bench.build(performant_model)
    pipelined_test_bench.build(pipelined_model)

    if not functional_test_bench.validate():
        print("Functional")
        exit(1)

    if not functional_test_bench.validate() or not memory_bound_test_bench.validate() or \
       not performant_test_bench.validate() or not pipelined_test_bench.validate():
        print("Model is not in a valid state")
        exit(1)

    # Setup the model
    functional_model.setup()
    memory_bound_model.setup()
    performant_model.setup()
    pipelined_model.setup()

    # Clock the model until no longer busy
    while functional_model.clock(1):
        pass

    while memory_bound_model.clock(1):
        pass

    while performant_model.clock(1):
        pass

    while pipelined_model.clock(1):
        pass

    # Tear Down
    functional_model.tear_down()
    memory_bound_model.tear_down()
    performant_model.tear_down()
    pipelined_model.tear_down()

    functional_counters = functional_model.get_all_counter_values()
    memory_bound_counters = functional_model.get_all_counter_values()
    performant_counters = functional_model.get_all_counter_values()
    pipelined_counters = functional_model.get_all_counter_values()

    if functional_counters != memory_bound_counters or functional_counters != performant_counters or functional_counters != pipelined_counters:
        print("Functional Counter mismatch\n")
        exit(1)

if __name__ == "__main__":
    main()
