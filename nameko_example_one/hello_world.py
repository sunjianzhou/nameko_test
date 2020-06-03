from nameko.rpc import rpc


class GreetingService:
    name = "nameko_service_1"

    @rpc
    def hello(self, name):
        return "Hello, {}!".format(name)