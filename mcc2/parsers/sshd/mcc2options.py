'''
Created on Jan 28, 2011

@author: guilherme
'''

class MccSshdMatchOption:
    
    def __init__(self,condition,settings=[]):
        self.name = 'Match'
        self.condition = condition
        self.settings = settings
        
    def set_condition(self,condition):
        self.condition = condition
        
    def get_condition(self,condition):
        return self.condition
    
    def set_setting(self,index,setting):
        self.settings[index] = setting

    def get_setting(self,index):
        return self.settings[index]
        
    def add_setting(self,setting):
        self.settings.append(setting)
    
    def get_option(self):
        set = []
        for setting in self.settings:
            set.append((setting.name,str(setting)))
        return ((self.condition.name,str(self.condition)),set)
    
    def __str__(self):
        ret = ''
        ret = ret + 'Condition %s: \n'%self.condition
        ret = ret + 'Settings: '
        for setting in self.settings:
            ret = ret + str(setting)+'\n'
        return ret
    
class MccOption:
    
    def __init__(self,name,value="",path=None,num = "1"):
        self.name = name
        self.value = value
        self.path = path
        self.num = num
    def set_value(self,value):
        self.value = value
    
    def set_num(self,num):
        self.num = num
    
    def get_num(self):
        return self.num
    
    def get_value(self):
        return self.value
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        return self.value
    
class MccMultiValueOption:
    
    def __init__(self,name,values=[],path=None):
        self.name = name
        self.values = values
        self.path = path
    
    def set_values(self,values):
        self.values = values
        
    def get_values(self):
        return self.values
    
    def set_value(self,index,value):
        self.values[index] = value

    def add_value(self,value):
        self.values.append(value)
        
    def get_value(self,index):
        return self.values[index]
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        ret = ''
        for value in self.values:
            ret = ret + value + ' '
        return ret[:-1]