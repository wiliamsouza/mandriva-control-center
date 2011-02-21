import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/usr/share/mandriva/config/mcc2.cfg')

print config.get('policy', 'level')
print type(config.get('policy', 'level'))