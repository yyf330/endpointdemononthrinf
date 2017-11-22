import os


def Create_service_file(filename,start_st,stop_st,status_st):
    print ("we will create a new file\n")
    createfile = open('/etc/init.d/'+filename,'w')
    #createfile = open('/home/wangdl/'+filename,'w')
    createfile.writelines('# @author:daolin\n')
    createfile.writelines('# chkconfig:35 85 15\n')
    createfile.writelines('# description:this is a service.\n')
    createfile.writelines('\n')
    #start
    createfile.writelines('start() {\n    echo "Starting ..."\n')
    createfile.writelines('    '+start_st+'\n    echo "Started"\n}\n')
    #stop
    createfile.writelines('stop() {\n    echo "Stopping ..."\n')
    createfile.writelines('    '+stop_st+'\n    echo "Stopped"\n}\n')


    createfile.writelines('case "$1" in\n  start)\nstart\n;;\n  stop)\nstop\n;;\n  restart|force-reload)\nstop\nstart\n;;\n  *)\necho $"Usage: $0 {start|stop|restart|force-reload}"\nexit 2\nesac\n')
    #createfile.writelines('')
    #createfile.writelines('')
    #createfile.writelines('')
    #createfile.writelines('')
    createfile.close()
    os.system('chkconfig --add '+filename)
    os.system('chmod +x /etc/init.d/'+filename)

if __name__== "__main__":
    Create_service_file('service6','ff','ff1','')
