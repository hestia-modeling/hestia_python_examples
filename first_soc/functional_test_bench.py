import argparse

from containers import FunctionalTestBench

from hestia.model import Model

def main():
    # User's can provide the path to their test bench library
    parser = argparse.ArgumentParser(description="Run a python test bench")
    parser.add_argument("model_path", metavar='B', type=str, help="Path to the model shared library")
    args = parser.parse_args()

    # Initialize the
    model = Model(args.model_path)

    # Add Clock Domain
    domain = "clk"
    model.add_clock_domain(domain, 1)

    # Create our test bench container
    number_test_bench = FunctionalTestBench("test_bench", domain)

    # Build our test bench in our model
    number_test_bench.build(model)

    # Validate the model
    if not model.validate():
        print("Model is not in a valid state")
        exit(1)

    # Setup the model
    model.setup()

    # Clock the model until no longer busy
    while model.clock(1):
        pass

    # Tear Down
    model.tear_down()

if __name__ == "__main__":
    main()
