import consulate

consul = consulate.Consul()

# Get all of the service checks for the local agent
def agent_check():
    checks = consul.agent.checks()
    print(checks)
    return checks

def agent_members():
    checks = consul.agent.members()
    print(checks)
    return checks
# Get all of the services registered with the local agent
def agent_services():
    services = consul.agent.services()
    print((services))
    re_service={}
    re_serv_m={'address':'','port':''}
    re_num=0
    for key in services:
        re_num=len(key)
        for key1 in key:
            print(key1)
            re_serv_m['address']=key[key1]['Address']
            re_serv_m['port']=key[key1]['Port']
            re_service.update({key1:re_serv_m})
            print(re_serv_m)
            re_serv_m={}

    return re_num,re_service

# Add a service to the local agent
def agent_register(name,s_port,s_address,s_tags):
    consul.agent.service.register(name,
                                   address=s_address,
                                   port=s_port,
                                   tags=s_tags,
                                   check='ls /home/wangdl/ > /home/wangdl/daolintest.txt',
                                   interval= "10s"
                                  # ttl='10s'
                                   )


def agent_deregister(name_id):
    consul.agent.service.deregister(name_id)

if __name__== "__main__":
    s_tags=['version','11111111','reserve','123']
    agent_register('cap',611,'192.168.20.199',s_tags)
    #print (agent_check())
    num,service=agent_services()
   # for i in range(0,num,2):
    #    print(service[i])
     #   agent_deregister(service[i])
   # print (agent_services())
 
