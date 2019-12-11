from hestia.component import Component
from hestia.connection_parameters import ConnectionParameters
from hestia.internal_connection import InternalConnection, InternalConnectionType
from hestia.parameter import Parameter, ParameterType
from hestia.port import Port, PortType

"""
 Our python representation of our FunctionalProcessor component
"""
class FunctionalProcessor(Component):
    def __init__(self, name: str, memory_name: str):
        super(FunctionalProcessor, self).__init__(name, "functional_processor")
        # Our Port
        self.ports["doorbell"] = Port("doorbell", PortType.READ, self)

        self.parameters["memory_name"] = Parameter("memory_name", ParameterType.STRING, memory_name)
        self.parameters["num_registers"] = Parameter("num_registers", ParameterType.UINT, str(10))

    def set_num_registers(self, num_registers: int) -> None:
        self.parameters["num_registers"].value = str(num_registers)


"""
 Our python representation of our MemoryBoundProcessor component
"""
class MemoryBoundProcessor(Component):
    def __init__(self, name: str, memory_name: str):
        super(MemoryBoundProcessor, self).__init__(name, "memory_bound_processor")
        # Our Port
        self.ports["doorbell"] = Port("doorbell", PortType.READ, self)
        self.ports["instruction_request"] = Port("instruction_request", PortType.WRITE, self)
        self.ports["instruction_response"] = Port("instruction_response", PortType.READ, self)
        self.ports["data_request"] = Port("data_request", PortType.WRITE, self)
        self.ports["data_response"] = Port("data_response", PortType.READ, self)

        # Internal Connections

        self.internal_connections["decoded_instruction"] = InternalConnection("decoded_instruction", self, InternalConnectionType.FIFO, ConnectionParameters())

        # Parameters

        self.parameters["memory_name"] = Parameter("memory_name", ParameterType.STRING, memory_name)
        self.parameters["num_registers"] = Parameter("num_registers", ParameterType.UINT, str(10))


    def set_num_registers(self, num_registers: int) -> None:
        self.parameters["num_registers"].value = str(num_registers)


"""
 Our python representation of our PerformantProcessor component
"""
class PerformantProcessor(Component):
    def __init__(self, name: str, domain: str, memory_name: str):
        super(PerformantProcessor, self).__init__(name, "performant_processor")
        # Our Port
        self.ports["doorbell"] = Port("doorbell", PortType.READ, self)
        self.ports["instruction_request"] = Port("instruction_request", PortType.WRITE, self)
        self.ports["instruction_response"] = Port("instruction_response", PortType.READ, self)
        self.ports["data_request"] = Port("data_request", PortType.WRITE, self)
        self.ports["data_response"] = Port("data_response", PortType.READ, self)

        # Internal Connections
        connection_parameters = ConnectionParameters()
        connection_parameters.is_timed = True
        connection_parameters.domain = domain.encode("utf-8")
        self.internal_connections["fetcher"] = InternalConnection("fetcher", self, InternalConnectionType.PIPELINE, connection_parameters)
        self.internal_connections["decoder"] = InternalConnection("decoder", self, InternalConnectionType.PIPELINE, connection_parameters)
        self.internal_connections["executor"] = InternalConnection("executor", self, InternalConnectionType.PIPELINE, connection_parameters)
        self.internal_connections["write_back"] = InternalConnection("write_back", self, InternalConnectionType.PIPELINE, connection_parameters)

        # Parameters

        self.parameters["memory_name"] = Parameter("memory_name", ParameterType.STRING, memory_name)
        self.parameters["num_registers"] = Parameter("num_registers", ParameterType.UINT, str(10))


    def set_num_registers(self, num_registers: int) -> None:
        self.parameters["num_registers"].value = str(num_registers)

"""
 Our python representation of our PipelinedProcessor component
"""
class PipelinedProcessor(Component):
    def __init__(self, name: str, domain: str, memory_name: str):
        super(PipelinedProcessor, self).__init__(name, "pipelined_processor")
        # Our Port
        self.ports["doorbell"] = Port("doorbell", PortType.READ, self)
        self.ports["instruction_request"] = Port("instruction_request", PortType.WRITE, self)
        self.ports["instruction_response"] = Port("instruction_response", PortType.READ, self)
        self.ports["data_request"] = Port("data_request", PortType.WRITE, self)
        self.ports["data_response"] = Port("data_response", PortType.READ, self)

        # Internal Connections
        connection_parameters = ConnectionParameters()
        connection_parameters.is_timed = True
        connection_parameters.domain = domain.encode("utf-8")
        self.internal_connections["fetcher"] = InternalConnection("fetcher", self, InternalConnectionType.PIPELINE, connection_parameters)
        self.internal_connections["decoder"] = InternalConnection("decoder", self, InternalConnectionType.PIPELINE, connection_parameters)
        self.internal_connections["executor"] = InternalConnection("executor", self, InternalConnectionType.PIPELINE, connection_parameters)
        self.internal_connections["write_back"] = InternalConnection("write_back", self, InternalConnectionType.PIPELINE, connection_parameters)

        # Parameters

        self.parameters["memory_name"] = Parameter("memory_name", ParameterType.STRING, memory_name)
        self.parameters["num_registers"] = Parameter("memory_name", ParameterType.UINT, str(10))


    def set_num_registers(self, num_registers: int) -> None:
        self.parameters["num_registers"].value = str(num_registers)

"""
 Our python representation of our Memory component
"""
class Memory(Component):
    def __init__(self, name: str, memory_name: str):
        super(Memory, self).__init__(name, "memory")
        # Our Port
        self.ports["requests"] = Port("requests", PortType.READ_ARRAY, self)
        self.ports["responses"] = Port("responses", PortType.WRITE_ARRAY, self)

        self.parameters["memory_name"] = Parameter("memory_name", ParameterType.STRING, memory_name)
