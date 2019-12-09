from components import Producer, Consumer

from hestia.connection import Connection
from hestia.connection_parameters import ConnectionParameters
from hestia.container import Container

# We are going to create a black box container that defines our test bench
class NumberTestBench(Container):
    def __init__(self, name: str, domain: str):
        super(NumberTestBench, self).__init__(name)

        # Our Components
        self.components["producer"] = Producer("producer")
        self.components["consumer"] = Consumer("consumer")

        # Our Connection
        connection_params = ConnectionParameters()
        connection_params.is_timed = True
        connection_params.domain = domain.encode("utf-8")
        self.connections["producer_consumer"] = Connection(self.components["producer"].ports["out"], self.components["consumer"].ports["in"], connection_params)

    def set_num_transactions(self, num_transactions: int) -> None:
        self.components["producer"].set_num_transactions(num_transactions)

    def set_connection_params(self, params: ConnectionParameters):
        self.connections["producer_consumer"].set_params(params)

