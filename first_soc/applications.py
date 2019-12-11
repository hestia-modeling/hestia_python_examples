from hestia.component import Component
from hestia.parameter import Parameter, ParameterType
from hestia.port import Port, PortType

"""
 Our python representation of our NumberConsumer component
"""
class SimpleApplication(Component):
    def __init__(self, name: str, memory_name: str):
        super(SimpleApplication, self).__init__(name, "simple_driver")
        # Our Port
        self.ports["doorbell"] = Port("doorbell", PortType.READ, self)

        self.parameters["memory_name"] = Parameter("memory_name", ParameterType.STRING, memory_name)

    def set_memory_name(self, memory_name: str) -> None:
        self.parameters["memory_name"].value = memory_name


"""
 Our python representation of our NumberConsumer component
"""
class LoopApplication(Component):
    def __init__(self, name: str, memory_name: str):
        super(LoopApplication, self).__init__(name, "loop_driver")
        # Our Port
        self.ports["doorbell"] = Port("doorbell", PortType.READ, self)

        self.parameters["memory_name"] = Parameter("memory_name", ParameterType.STRING, memory_name)
        self.parameters["num_iterations"] = Parameter("num_iterations", ParameterType.STRING, str(100))
        self.parameters["num_ops_per_iteration"] = Parameter("num_ops_per_iteration", ParameterType.STRING, str(100))
        self.parameters["mode"] = Parameter("mode", ParameterType.STRING, "alu")

    def set_memory_name(self, memory_name: str) -> None:
        self.parameters["memory_name"].value = memory_name

    def set_num_iterations(self, amount: int) -> None:
        self.parameters["num_iterations"].value = str(amount)

    def set_num_operations_per_iteration(self, amount: int) -> None:
        self.parameters["num_ops_per_iteration"].value = amount

    def set_mode(self, mode: str) -> None:
        self.parameters["mode"].value = mode