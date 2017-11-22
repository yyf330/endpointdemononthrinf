import thriftpy
from thriftpy.rpc import make_server
import consulate
import json
from thriftpy.rpc import make_client
import time
import socket
import os
import threading
import sys
import socket
from  consul_reg_check import *
from service_create import Create_service_file
consul = consulate.Consul()
#gui thrift rpc
gui_client = thriftpy.load("/usr/local/workerman-thrift/workerman-thrift/ToWeb.thrift", module_name="gui_client_thrift")
#endpoint deamon  thrift rpc
endpoint_service = thriftpy.load("/home/wangdl/nodedeamon/endpoint_service.thrift", module_name="endpoint_service_thrift")

if len(sys.argv)<2:
    print("Usage:[work]")
    sys.exit()
else:
    work=sys.argv[1]

import multiprocessing
from multiprocessing import queues
e_que = queues.Queue(5, ctx=multiprocessing)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

ip=get_host_ip()
port=0

# def get_busi_services():
#     try:
#         services = consul.agent.services()
#         busi_l=['C','T','L']
#         # print((services))
#         # re_serv_m={'address':'','port':''}
#         # ret
#         for key in services:
#             for key1 in key:
#                 s_type=key[key1]['Tags'][1]
#                 time_t=key[key1]['Tags'][2]
#                 if s_type in busi_l and((time.time()-time_t)>15) :
#                     # time_c=time.time()-time_t
#                     print('status error')
#
#
#     except Exception as e:
#         print('---get_busi_services error !--', e)

    # finally:

def get_gui_agent_services():
    services = consul.agent.services()
    # print((services))
    re_serv_m={'address':'','port':''}
    for key in services:
        for key1 in key:
            # print(key1)
            if key1 == "gui":
                re_serv_m['address']=key[key1]['Address']
                re_serv_m['port']=key[key1]['Port']
                # re_service.update({key1:re_serv_m})
                # print(re_serv_m)
            # re_serv_m={}
    # print(re_serv_m)
    return re_serv_m

def send_msg_gui(e_que):
    client=''
    while True:
        try:
            if e_que.qsize() == 0:
                pass
            else:
                status=e_que.get()
                print('----d----',status)
                if status=='stop':
                    print('exit')
                    sys.exit()
            gui_service = get_gui_agent_services()
            if gui_service['address'] == '' or gui_service['port'] == '':
                # if True:#gui_service['address'] == '' or gui_service['port'] == '':
                gui_service['address'] = '127.0.0.1'
                gui_service['port'] = '9090'
            client = make_client(gui_client.ToWeb, gui_service['address'], int(gui_service['port']))
            break
        except Exception as e:
            print('---send_msg_gui error !--', e)
            time.sleep(2)
            continue

    while True:
        # print('send_msg_gui--------1')
        try:
            if e_que.qsize() == 0:
                pass
            else:
                status=e_que.get()
                print('----d----',status)
                if status=='stop':
                    print('exit')
                    sys.exit()

            send_msg = { 'serviceType': 'E', 'servicename': ''}
            services = consul.agent.services()
            busi_l = ['C', 'T', 'L']
            busi_type = ['C', 'T', 'L','G','E']
            # print((services))
            # re_serv_m={'address':'','port':''}
            # ret
            # print('send_msg_gui-------0000')
            for key in services:
                for key1 in key:
                    s_type = key[key1]['Tags'][1]
                    if len(key[key1]['Tags'])<4 or s_type not in busi_type:
                        consul.agent.service.deregister(key[key1]['Service'])
                        continue

                    time_1 = key[key1]['Tags'][2]
                    time_p=(int(time.time()) - int(time_1))
                    print(s_type,time_p)
                    if s_type in busi_l and (time_p > 15 or time_p<0):

                        print('status error')

                        in_json = json.dumps(send_msg)


                        gui_service = get_gui_agent_services()
                        if gui_service['address'] == '' or gui_service['port'] == '':
                            # if True:#gui_service['address'] == '' or gui_service['port'] == '':
                            gui_service['address'] = '127.0.0.1'
                            gui_service['port'] = '9090'
                        client = make_client(gui_client.ToWeb, gui_service['address'], int(gui_service['port']))

                        ret = client.pushData(str(in_json))
                        s_name =key1
                        consul.agent.service.deregister(key[key1]['Service'])
                        print('restart--',s_name)
                        # os.system('service ' + s_name + ' restart ')
                        print(ret)
                        time.sleep(2)

        except Exception as e:
            try:
                print('---get_busi_services error !--', e)
                gui_service = get_gui_agent_services()
                if gui_service['address'] == '' or gui_service['port'] == '':
                    # if True:#gui_service['address'] == '' or gui_service['port'] == '':
                    gui_service['address'] = '127.0.0.1'
                    gui_service['port'] = '9090'
                client = make_client(gui_client.ToWeb, gui_service['address'], int(gui_service['port']))
                continue
            except Exception as e:
                print('---send_msg_gui error !--', e)
                time.sleep(2)
                continue
        finally:
            # print('send_msg_gui--------2')
            time.sleep(2)



class Dispatcher(object):
    def create_capture_p(self,workid,s_name,cid):
        if s_name==None or s_name==''or workid>15:
            return 1
        start_sh='/home/dss/capture/capture start '+str(workid)+' '+s_name+' '+str(cid)+' &'
        stop_sh='/home/dss/capture/capture stop '+str(workid)+' '+s_name+' '+str(cid)+' &'
        status_sh=''
        Create_service_file(s_name,start_sh,stop_sh,status_sh)
        return 0

    def create_trnsp_p(self,workid,s_name,cid):
        if s_name==None or s_name==''or workid>15:
            return 1
        start_sh='/bin/python3.4  /home/dss/transport/zhiwang_transport.py start '+str(workid)+' '+s_name+' '+str(cid)+' &'
        stop_sh='/bin/python3.4  /home/dss/transport/zhiwang_transport.py stop '+str(workid)+' '+s_name+' '+str(cid)+' &'
        status_sh=''
        Create_service_file(s_name,start_sh,stop_sh,status_sh)
        return 0

    def create_load_p(self,workid,s_name,cid):
        if s_name==None or s_name==''or workid>15:
            return 1
        start_sh='/home/dss/load/load start '+str(workid)+' '+s_name+' '+str(cid)+' &'
        stop_sh='/home/dss/load/load stop '+str(workid)+' '+s_name+' '+str(cid)+' &'
        status_sh=''
        Create_service_file(s_name,start_sh,stop_sh,status_sh)
        return 0

    def start_p(self,s_name):
        if s_name==None or s_name=='':
            return 1
        print('service start!')
        start_sh=str('service '+s_name+' start ')
        print('------',start_sh)
        os.system(start_sh)
        return 0

    def stop_p(self,s_name):
        if s_name==None or s_name=='':
            return 1
        os.system('service '+ s_name+' stop ' )
        return 0

    def del_p(self,s_name):
        if s_name==None or s_name=='':
            return 1
        os.system('rm /etc/init.d/'+ s_name+' -rf' )
        return 0

    def get_ip(self):

        return get_host_ip()

def fun_receive(args):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, 7005))
    # print('---',ip)
    # print ('...waiting for message..')
    while True:
        data, address = s.recvfrom(1024)
        print (data)
        str1=data.decode('utf-8')
        status=str1.split('#')[1]
        #print(status)
        s.sendto('server reveive'.encode('utf8'), address)
        # s.sendto('this is the UDP server'.encode('utf8'), address)
        if status=='stop':
            e_que.put('stop')
            break

    s.close()

def fun_rpc_server(args):
    print('fun_rpc_server  start!')
    print(ip, port)
    server = make_server(endpoint_service.endpointControl, Dispatcher(), ip, port)
    server.serve()

def fun_send(args):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # //#005#2#
    msg = '0' + '#' + args
    print(msg)
    s.sendto(msg.encode('utf8'), (ip, 7005))
    data = s.recv(1024)
    print(data)
    s.close()
    return data

threads = []
t1 = threading.Thread(target=send_msg_gui,args=(e_que,))
threads.append(t1)

def GetValue_FromFile_Bystr(str):
    sh_str="cat init.txt|grep "+str+"| gawk -F = '{print $2}'"
    ret=os.popen(sh_str).read().split('\n')[0]
    return ret


def EndPoint_Init():
    if int(GetValue_FromFile_Bystr('firststart'))==1:
        pass
    else:
        pass


s_name='endpoint_service'
if __name__== "__main__":
    try:
        if work == 'start':
            port =7000
            now_t = time.time()
            # s_tags = ['1.0.2.0', 'T', str(int(now_t)), 'reserve']
            s_tags = ['1.0.2.0', 'E',str(int(now_t)) , 'reserve']
            agent_register(s_name, port, ip, s_tags)

            p_list=[fun_rpc_server,fun_receive]
            for pro in p_list:
                p = multiprocessing.Process(target = pro, args = (e_que,))
                p.daemon = True
                p.start()

            try:
                for t in threads:
                    t.setDaemon(True)
                    t.start()
                t.join()
                # print(ip,port)
                # server = make_server(endpoint_service.endpointControl, Dispatcher(), ip, port)
                # server.serve()
            finally:
                print('end')
                consul.agent.service.deregister(s_name)
        elif work=='stop':
            fun_send('stop')
    except (KeyboardInterrupt, SystemExit):
        print("exit!")
    finally:
        # print('end')
        consul.agent.service.deregister(s_name)