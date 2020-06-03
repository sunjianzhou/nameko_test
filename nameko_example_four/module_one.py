from nameko.rpc import rpc, RpcProxy


class ClassOne:
    name = "service_1"
    connection_rpc = RpcProxy("service_2")

    def __init__(self):
        self.personal_name = "LiLei"
        self.age = 18

    @rpc
    def get_personal_info(self):
        return self.personal_name, self.age

    @rpc
    def communication(self):
        target_name, target_age = self.connection_rpc.get_personal_info()
        print("hello {}, I know your are {} years old!".format(target_name, target_age))
        return "{} call {} finished!".format(self.personal_name, target_name)

