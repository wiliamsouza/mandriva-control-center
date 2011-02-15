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
    
    def __option_exist(self,opt_name):
        """Check if an option already exist in the list and return
        it if yes
        """
        for opt in self.options:
            if opt.get_name() == opt_name:
                return opt
        return None
            
    def __process_multivalue_option(self,option,dup):
        """Process any multivalue option
        
        @param option: the option to process
        @param dup: if is a duplicate option
        @type dup: Boolean
        
        """
        merge_option = None
        if dup:
            opt_name = option.split("/")[-1].split("[")[0]
            for opt in self.options:
                if opt.get_name() == opt_name:
                    merge_option = opt
        else:
            opt_name = option.split("/")[-1]
            
        if not merge_option:
            multi_option = MccMultiValueOption(opt_name,[],option)
        else:
            multi_option = merge_option
            
        childs = self.__option_has_child(option)
        if childs:
            for child in childs:
                if opt_name == "Subsystem":
                    multi_option.add_value(child.split("/")[-1])
                multi_option.add_value(self.aug.get(child))
        else:
            multi_option.add_value(self.aug.get(option))
            
        if not merge_option:
            self.options.append(multi_option)

    def __parse_matchblock(self,matchblock):
        """Parse a matchblock and save its options"""
        #TODO: check if is permited dup option inside match block
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
        self.options=[]
        tree = self.aug.match('/files/etc/ssh/sshd_config/*')
        for option in tree:
            opt_num = 1
            if option.split("/")[-1][0] != '#' and option.split("/")[-1][:5] != 'Match': # exclude comments
                    #if option.split("/")[-1][-1] == ']':
                if self.__option_has_child(option):
                    if option.split("/")[-1][-1] == ']':
                        self.__process_multivalue_option(option,True)
                    else:
                        self.__process_multivalue_option(option,False)
                else:
                    if option.split("/")[-1][-1] == ']':
                        opt_name = option.split("/")[-1].split("[")[0]
                        opt_num =  option.split("/")[-1].split("[")[1].split("]")[0]
                    else:
                        opt_name = option.split("/")[-1] 

                    if opt_name in SSHDOptions.options_list:
                        self.options.append(MccOption(opt_name,self.aug.get(option),option,opt_num))
                    else:
                        print "Unknow option read from file"
                        
            elif option.split("/")[-1][:5] == 'Match':
                self.__parse_matchblock(option)

    def remove_option(self,option):
        #TODO: remember position to insert    
        if not option.path:
            option.path = "/files/etc/ssh/sshd_config/"+option.name+"[*]/"            
            
        if isinstance(option,MccMultiValueOption):
            if option.name == "Subsystem":
                self.aug.remove(option.path)
            else:
                #option.path = "/files/etc/ssh/sshd_config/"+option.name+"[%s]/"%str(opt_num)
                self.aug.remove("/files/etc/ssh/sshd_config/"+option.name+"[*]")
        else:
            self.aug.remove(option.path)

        try:
            self.aug.save()
        except IOError:
            print "Error saving config file"
            #print self.aug.get("/augeas/files/etc/ssh/sshd_config/error/message")
            return -1
        self.parse()
        
    def set_option(self,option):    
        """Set an option using a MCCOption"""
        #TODO: remember position to insert    
        opt_num = 1
        if not option.path:
            option.path = "/files/etc/ssh/sshd_config/"+option.name+"[last()]/"            
            
        if isinstance(option,MccMultiValueOption):
            if option.name == "Subsystem":
                self.aug.set(option.path, option.get_value(0))
                self.aug.set(option.path+str(option.get_value(0)), option.get_value(1))
            else:
                option.path = "/files/etc/ssh/sshd_config/"+option.name+"[%s]/"%str(opt_num)
                self.aug.remove("/files/etc/ssh/sshd_config/"+option.name+"[*]")
                #self.aug.
                values = option.get_values()
                value_len = 0
                for value,num in  map(None,values,range(1,len(values)+1)):
                    value_len += len(value)
                    if value_len >= 60:
                        opt_num += 1
                        value_len = 0
                        option.path = "/files/etc/ssh/sshd_config/"+option.name+"[%s]/"%str(opt_num)
                    print "setting %s to %s"%(option.path+str(num),value)
                    self.aug.set(option.path+str(num),value)
        else:
            self.aug.set(option.path,option.get_value())

        try:
            self.aug.save()
        except IOError:
            print "Error saving config file"
            #print self.aug.get("/augeas/files/etc/ssh/sshd_config/error/message")
            return -1
        self.parse()
        
    def set_match_option(self,option):
        """Set a match Block using a MCCSshdMatchOptions"""
        self.aug.set(option.condition.path, option.condition.value)
        for setting in option.settings:
            self.aug.set(setting.path, setting.value)