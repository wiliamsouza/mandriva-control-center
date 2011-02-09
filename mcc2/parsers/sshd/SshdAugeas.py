'''
Created on Jan 27, 2011

@author: guilherme@mandriva.com.br
'''
import augeas
from mcc2options import *
from ssh_options import SSHDOptions

class SshdAugConfigParser(object):
    
    """Base class for configuration parsing"""
    
    def __init__(self,filepath='/',flags=0):
        """Sshd augeas parsing
        
        @param filepath Path to the sshd_config file
        @param flags: Flags to be passed to augeas
        
        """
        self.filepath=filepath
        self.aug = augeas.Augeas(root=self.filepath,flags=flags)
        self.options = []
         
    def __option_has_child(self,option):
        """Return a list of childs of this option if any"""
        return self.aug.match(option+'/*')
    
    def __process_multivalue_option(self,option,dup):
        """Process any multivalue option
        
        @param option: the option to process
        @param dup: if is a duplicate option
        @type dup: Boolean
        
        """
        if dup:
            opt_name = option.split("/")[-1].split("[")[0]
        else:
            opt_name = option.split("/")[-1]
        multi_option = MccMultiValueOption(opt_name,[],option)
        childs = self.__option_has_child(option)
        if childs:
            for child in childs:
                if opt_name == "Subsystem":
                    multi_option.add_value(child.split("/")[-1])
                multi_option.add_value(self.aug.get(child))
        else:
            multi_option.add_value(self.aug.get(option))
            
        self.options.append(multi_option)
    
    def __parse_matchblock(self,matchblock):
        """Parse a matchblock and save its options"""
        #TODO: dup option inside match block
        cond = self.aug.match(matchblock+'/Condition/*')
        if not cond:
            return
        cond_name = cond[0].split("/")[-1]
        cond_value = self.aug.get(cond[0])
        match_option = MccSshdMatchOption(MccOption(cond_name,cond_value,cond[0]))
        for child in self.aug.match(matchblock+'/Settings/*'):
            opt = MccOption(child.split("/")[-1],self.aug.get(child),child)
            match_option.add_setting(opt)
        self.options.append(match_option)
    
    def parse(self):
        """Parse sshd_config file"""
        #tree = self.aug.match('/files/sshd_config/*')
        tree = self.aug.match('/files/etc/ssh/sshd_config/*')
        for option in tree:
            if option.split("/")[-1][0] != '#' and option.split("/")[-1][:5] != 'Match': # exclude comments
                if option.split("/")[-1][-1] == ']':
                    self.__process_multivalue_option(option,True)
                elif self.__option_has_child(option):
                        self.__process_multivalue_option(option,False)
                elif option.split("/")[-1] in SSHDOptions.options_list:
                    self.options.append(MccOption(option.split("/")[-1],self.aug.get(option),
                                                  option))
            elif option.split("/")[-1][:5] == 'Match':
                self.__parse_matchblock(option)

    def set_option(self,option):    
        """Set an option using a MCCOption"""    
        if not option.path:
            if option.split("/")[-1][-1] == "]":
                option.path = "/files/etc/ssh/sshd_config/"+option.name+"[last()+1]"
            else:
                option.path = "/files/etc/ssh/sshd_config/"+option.name
                
        if isinstance(option,MccMultiValueOption):
            if option.name == "Subsystem":
                self.aug.set(option.path, option.get_value(0))
                self.aug.set(option.path+str(option.get_value(0)), option.get_value(1))
            else:
                values = option.get_values()
                for value,num in  map(None,values,range(1,len(values)+1)):
                    self.aug.set(option.path+str(num),value)
        else:
            self.aug.set(option.path,option.get_value())

        try:
            self.aug.save()
        except IOError:
            print "Error saving config file"
            return -1
    
    def set_match_option(self,option):
        """Set a match Block using a MCCSshdMatchOptions"""
        self.aug.set(option.condition.path, option.condition.value)
        for setting in option.settings:
            self.aug.set(setting.path, setting.value)