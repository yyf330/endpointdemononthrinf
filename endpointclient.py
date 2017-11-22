import thriftpy



micro_thrift_control = thriftpy.load("endpoint_service.thrift", module_name="endpoint_service_thrift")

from thriftpy.rpc import make_client

client = make_client(micro_thrift_control.endpointControl, '192.168.20.199', 7000)


print('start')
client.start_p('helloworld')

