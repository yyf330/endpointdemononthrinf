import os

def GetValue_FromFile_Bystr(str):
    sh_str="cat init.txt|grep "+str+"| gawk -F = '{print $2}'"
    ret=os.popen(sh_str).read().split('\n')[0]
    return ret

print (GetValue_FromFile_Bystr('firststart'))
print ('end')



