from nameko.rpc import rpc, RpcProxy


class ClassTwo:
    name = "service_2"

    connection_rpc = RpcProxy("service_1")

    def __init__(self):
        self.personal_name = "HanMeiMei"
        self.age = 16

    @rpc
    def get_personal_info(self):
        return self.personal_name, self.age

    @rpc
    def communication(self):
        target_name, target_age = self.connection_rpc.get_personal_info()
        print("hello {}, I know your are {} years old!".format(target_name, target_age))
        return "{} call {} finished!".format(self.personal_name, target_name)


