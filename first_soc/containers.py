from components import FunctionalProcessor, MemoryBoundProcessor, PerformantProcessor, PipelinedProcessor, Memory
from applications import SimpleApplication
from hestia.connection import Connection
from hestia.connection_parameters import ConnectionParameters
from hestia.container import Container

# We are going to create a black box container that defines our test bench
from first_soc.applications import LoopApplication


class FunctionalTestBench(Container):
    def __init__(self, name: str, domain: str, memory_name: str):
        super(FunctionalTestBench, self).__init__(name)

        # Our Components
        self.components["application"] = SimpleApplication("driver", memory_name)
        self.components["processor"] = FunctionalProcessor("processor", memory_name)

        # Our Connection
        connection_params = ConnectionParameters()
        self.connections["doorbell"] = Connection(self.components["application"].ports["doorbell"], self.components["processor"].ports["doorbell"], connection_params)

class MemoryBoundTestBench(Container):
    def __init__(self, name: str, domain: str, memory_name: str):
        super(MemoryBoundTestBench, self).__init__(name)

        # Our Components
        self.components["application"] = SimpleApplication("driver", memory_name)
        self.components["processor"] = MemoryBoundProcessor("processor", memory_name)
        self.components["memory"] = Memory("ram", memory_name)

        # Our Connection
        connection_params = ConnectionParameters()
        connection_params.domain = domain.encode("utf-8")
        connection_params.is_timed = True
        self.connections["doorbell"] = Connection(self.components["application"].ports["doorbell"], self.components["processor"].ports["doorbell"], connection_params)
        self.connections["instruction_request"] = Connection(self.components["processor"].ports["instruction_request"], self.components["memory"].ports["requests"], connection_params)
        self.connections["instruction_response"] = Connection(self.components["processor"].ports["instruction_response"], self.components["memory"].ports["responses"], connection_params)
        self.connections["data_request"] = Connection(self.components["memory"].ports["requests"], self.components["processor"].ports["data_request"], connection_params)
        self.connections["data_response"] = Connection(self.components["memory"].ports["responses"], self.components["processor"].ports["data_response"], connection_params)

    def set_instruction_memory_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.connections["instruction_request"].params.latency = latency
        self.connections["instruction_response"].params.latency = latency
        self.connections["instruction_request"].params.capacity = capacity
        self.connections["instruction_response"].params.capacity = capacity
        self.connections["instruction_request"].params.read_rate = rate
        self.connections["instruction_response"].params.read_rate = rate
        self.connections["instruction_request"].params.write_rate = rate
        self.connections["instruction_response"].params.write_rate = rate

    def set_data_memory_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.connections["data_request"].params.latency = latency
        self.connections["data_response"].params.latency = latency
        self.connections["data_request"].params.capacity = capacity
        self.connections["data_response"].params.capacity = capacity
        self.connections["data_request"].params.read_rate = rate
        self.connections["data_response"].params.read_rate = rate
        self.connections["data_request"].params.write_rate = rate
        self.connections["data_response"].params.write_rate = rate


class PerformantTestBench(Container):
    def __init__(self, name: str, domain: str, memory_name: str):
        super(PerformantTestBench, self).__init__(name)

        # Our Components
        self.components["application"] = SimpleApplication("driver", memory_name)
        self.components["processor"] = PerformantProcessor("processor", domain, memory_name)
        self.components["memory"] = Memory("ram", memory_name)

        # Our Connection
        connection_params = ConnectionParameters()
        connection_params.domain = domain.encode("utf-8")
        connection_params.is_timed = True
        self.connections["doorbell"] = Connection(self.components["application"].ports["doorbell"], self.components["processor"].ports["doorbell"], connection_params)
        self.connections["instruction_request"] = Connection(self.components["processor"].ports["instruction_request"], self.components["memory"].ports["requests"], connection_params)
        self.connections["instruction_response"] = Connection(self.components["processor"].ports["instruction_response"], self.components["memory"].ports["responses"], connection_params)
        self.connections["data_request"] = Connection(self.components["memory"].ports["requests"], self.components["processor"].ports["data_request"], connection_params)
        self.connections["data_response"] = Connection(self.components["memory"].ports["responses"], self.components["processor"].ports["data_response"], connection_params)

    def set_instruction_memory_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.connections["instruction_request"].params.latency = latency
        self.connections["instruction_response"].params.latency = latency
        self.connections["instruction_request"].params.capacity = capacity
        self.connections["instruction_response"].params.capacity = capacity
        self.connections["instruction_request"].params.read_rate = rate
        self.connections["instruction_response"].params.read_rate = rate
        self.connections["instruction_request"].params.write_rate = rate
        self.connections["instruction_response"].params.write_rate = rate

    def set_data_memory_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.connections["data_request"].params.latency = latency
        self.connections["data_response"].params.latency = latency
        self.connections["data_request"].params.capacity = capacity
        self.connections["data_response"].params.capacity = capacity
        self.connections["data_request"].params.read_rate = rate
        self.connections["data_response"].params.read_rate = rate
        self.connections["data_request"].params.write_rate = rate
        self.connections["data_response"].params.write_rate = rate

    def set_fetcher_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.components["processor"].internal_connections["fetcher"].params.latency = latency
        self.components["processor"].internal_connections["fetcher"].params.capacity = capacity
        self.components["processor"].internal_connections["fetcher"].params.read_rate = rate
        self.components["processor"].internal_connections["fetcher"].params.write_rate = rate

    def set_decoder_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.components["processor"].internal_connections["decoder"].params.latency = latency
        self.components["processor"].internal_connections["decoder"].params.capacity = capacity
        self.components["processor"].internal_connections["decoder"].params.read_rate = rate
        self.components["processor"].internal_connections["decoder"].params.write_rate = rate

    def set_executor_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.components["processor"].internal_connections["executor"].params.latency = latency
        self.components["processor"].internal_connections["executor"].params.capacity = capacity
        self.components["processor"].internal_connections["executor"].params.read_rate = rate
        self.components["processor"].internal_connections["executor"].params.write_rate = rate

    def set_write_back_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.components["processor"].internal_connections["write_back"].params.latency = latency
        self.components["processor"].internal_connections["write_back"].params.capacity = capacity
        self.components["processor"].internal_connections["write_back"].params.read_rate = rate
        self.components["processor"].internal_connections["write_back"].params.write_rate = rate


class PipelinedTestBench(Container):
    def __init__(self, name: str, domain: str, memory_name: str):
        super(PipelinedTestBench, self).__init__(name)

        # Our Components
        self.components["application"] = LoopApplication("driver", memory_name)
        self.components["processor"] = PipelinedProcessor("processor", domain, memory_name)
        self.components["memory"] = Memory("ram", memory_name)

        # Our Connection
        connection_params = ConnectionParameters()
        connection_params.domain = domain.encode("utf-8")
        connection_params.is_timed = True
        self.connections["doorbell"] = Connection(self.components["application"].ports["doorbell"], self.components["processor"].ports["doorbell"], connection_params)
        self.connections["instruction_request"] = Connection(self.components["processor"].ports["instruction_request"], self.components["memory"].ports["requests"], connection_params)
        self.connections["instruction_response"] = Connection(self.components["memory"].ports["responses"], self.components["processor"].ports["instruction_response"], connection_params)
        self.connections["data_request"] = Connection(self.components["processor"].ports["data_request"], self.components["memory"].ports["requests"], connection_params)
        self.connections["data_response"] = Connection(self.components["memory"].ports["responses"], self.components["processor"].ports["data_response"], connection_params)

    def set_instruction_memory_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.connections["instruction_request"].params.latency = latency
        self.connections["instruction_response"].params.latency = latency
        self.connections["instruction_request"].params.capacity = capacity
        self.connections["instruction_response"].params.capacity = capacity
        self.connections["instruction_request"].params.read_rate = rate
        self.connections["instruction_response"].params.read_rate = rate
        self.connections["instruction_request"].params.write_rate = rate
        self.connections["instruction_response"].params.write_rate = rate

    def set_data_memory_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.connections["data_request"].params.latency = latency
        self.connections["data_response"].params.latency = latency
        self.connections["data_request"].params.capacity = capacity
        self.connections["data_response"].params.capacity = capacity
        self.connections["data_request"].params.read_rate = rate
        self.connections["data_response"].params.read_rate = rate
        self.connections["data_request"].params.write_rate = rate
        self.connections["data_response"].params.write_rate = rate

    def set_fetcher_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.components["processor"].internal_connections["fetcher"].params.latency = latency
        self.components["processor"].internal_connections["fetcher"].params.capacity = capacity
        self.components["processor"].internal_connections["fetcher"].params.read_rate = rate
        self.components["processor"].internal_connections["fetcher"].params.write_rate = rate

    def set_decoder_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.components["processor"].internal_connections["decoder"].params.latency = latency
        self.components["processor"].internal_connections["decoder"].params.capacity = capacity
        self.components["processor"].internal_connections["decoder"].params.read_rate = rate
        self.components["processor"].internal_connections["decoder"].params.write_rate = rate

    def set_executor_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.components["processor"].internal_connections["executor"].params.latency = latency
        self.components["processor"].internal_connections["executor"].params.capacity = capacity
        self.components["processor"].internal_connections["executor"].params.read_rate = rate
        self.components["processor"].internal_connections["executor"].params.write_rate = rate

    def set_write_back_params(self, latency: int = 1, capacity: int = 1, rate: int = 1):
        self.components["processor"].internal_connections["write_back"].params.latency = latency
        self.components["processor"].internal_connections["write_back"].params.capacity = capacity
        self.components["processor"].internal_connections["write_back"].params.read_rate = rate
        self.components["processor"].internal_connections["write_back"].params.write_rate = rate
