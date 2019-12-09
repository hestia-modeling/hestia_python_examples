from hestia.component import Component
from hestia.parameter import Parameter, ParameterType
from hestia.port import Port, PortType

"""
 Our python representation of our NumberConsumer component
"""
class Consumer(Component):
    def __init__(self, name: str):
        super(Consumer, self).__init__(name, "number_consumer")
        # Our Port
        self.ports["in"] = Port("in", PortType.READ, self)

"""
 Our python representation of our NumberProducer component
"""
class Producer(Component):
    def __init__(self, name: str):
        super(Producer, self).__init__(name, "number_producer")
        # Our Port
        self.ports["out"] = Port("out", PortType.WRITE, self)
        # Our Parameters with reasonable default values
        self.parameters["num_transactions"] = Parameter("num_transactions", ParameterType.UINT, str(100))
        self.parameters["min_number"] = Parameter("min_number", ParameterType.UINT, str(0))
        self.parameters["max_number"] = Parameter("max_number", ParameterType.UINT, str(100))

    # Helper functions to set public parameters in meaningful ways.
    # This is also a perfect place to provide some initial validation
    def set_num_transactions(self, num_transactions: int) -> None:
        self.parameters["num_transactions"].value = str(num_transactions)

    def set_min_value(self, value: int) -> None:
        self.parameters["min_number"].value = str(value)

    def set_max_value(self, value: int) -> None:
        self.parameters["max_number"].value = str(value)