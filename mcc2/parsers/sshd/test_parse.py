'''
Created on Feb 8, 2011

@author: guilherme
'''
import SshdConfig

base_path = '/tmp/augeas-sandbox' #set to the root where /etc resides

ssh = SshdConfig.SshdConfig(base_path, 2)
for opt in ssh.get_options():
    print opt.name + " : " + str(opt)
