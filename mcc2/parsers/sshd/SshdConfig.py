'''
Created on Feb 3, 2011

@author: guilherme
'''
from SshdAugeas import SshdAugConfigParser
from mcc2options import *

class SshdConfig:
    '''Class to control sshd configuration
    '''
    
    def __init__(self,sshd_config_path=None,flags=0):
        '''Constructor
        
        @param sshd_config_path: base path where look for /etc/ssh/sshd_config
        @param flags: Flags to pass to augeas
        ''' 
        self.sshd_config_path = sshd_config_path
        self.augparser = SshdAugConfigParser(self.sshd_config_path,flags=flags)
        self.augparser.parse()
    
    def remove_option(self,option):
        return self.augparser.remove_option(option)
           
    def get_option_value(self,option):
        '''Get the value of a SSHD option
        
        @param option: String with the option name
        @type option: String
        '''
        value = None
        if option == 'Match':
            return value
        for o in self.augparser.options:
            if o.name == option:
                value = str(o)
        return value
    
    def get_options_as_str(self):
        '''Get all options in the config file as a string
        '''
        options=[]
        for option in self.augparser.options:
            if option.name == 'Match':
                pass
            else:
                options.append((option.name,str(option)))   
        return options
    
    def get_match_blocks_as_str(self):
        '''Get all match blocks as a string
        '''
        blocks = []
        for option in self.augparser.options:
            if option.name == 'Match':
                blocks.append(option.get_option())
        return blocks
    
    def get_options(self):
        '''Get all options as MCCOptions
        '''
        options = []
        for option in self.augparser.options:
            if option.name == 'Match':
                pass
            else:
                options.append(option)   
        return options
    
    def get_match_blocks(self):
        '''Get all match blocks as MCCSshdMatchOptions
        '''
        blocks = []
        for option in self.augparser.options:
            if option.name == 'Match':
                blocks.append(option)
        return blocks
    
    def set_option(self,option):
        '''Set the value of an option using a MCCOption
        
        @param option: option to be set in the config file
        @type option: MCCOption, MCCMultiValueOption
        '''
        if isinstance(option, MccMultiValueOption) or isinstance(option, MccOption):
            self.augparser.set_option(option)
        elif isinstance(option,MccSshdMatchOption):
            self.augparser.set_match_option(option)