import SshdConfig
import os
import sys

base_path = '/tmp/augeas-sandbox' #set to the root where /etc resides
ssh = SshdConfig.SshdConfig(base_path,flags = 2)
for opt in ssh.get_options():
    if opt.name == 'X11Forwarding':
        opt.set_value("no")
        if ssh.set_option(opt) == -1:
            print "error saving file"
            sys.exit(0)
            
arq = base_path+"/etc/ssh/sshd_config"
arq_new = arq+".augnew"
if os.path.exists(arq_new):
    os.system("diff -u "+arq+" "+arq_new)
    os.system("rm "+arq_new)
else:
    print "Option not saved because we have the same values"