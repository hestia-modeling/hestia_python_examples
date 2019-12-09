from components import FunctionalProcessor, MemoryBoundProcessor, PerformantProcessor, PipelinedProcessor, Memory
from applications import SimpleApplication
from hestia.connection import Connection
from hestia.connection_parameters import ConnectionParameters
from hestia.container import Container

# We are going to create a black box container that defines our test bench
class FunctionalTestBench(Container):
    def __init__(self, name: str, domain: str):
        super(FunctionalTestBench, self).__init__(name)

        # Our Components
        self.components["application"] = SimpleApplication("driver", "mem")
        self.components["processor"] = FunctionalProcessor("processor", "mem")

        # Our Connection
        connection_params = ConnectionParameters()
        self.connections["doorbell"] = Connection(self.components["application"].ports["doorbell"], self.components["processor"].ports["doorbell"], connection_params)

