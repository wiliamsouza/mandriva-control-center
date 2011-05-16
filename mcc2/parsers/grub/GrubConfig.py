'''
Created on Feb 14, 2011

@author: guilherme
'''
import utils
from menu import *

class GrubConfig(GrubLegacy):
    """Class to get menu.lst information"""
    
    def __init__(self, menufile="/boot/grub/menu.lst"):
        #self.menu = menufile
        self.title_blocks = {}
        GrubLegacy.__init__(self)
        
    
    def parse(self):
        grub_lines = utils.read_lines_from_file(self.menu)
        block_num = 0
        last_title = ""
        block_value = []
        
        for line in grub_lines:
            if line[:5] == "title":
                block_num += 1
                block_value = []
                last_title = str(block_num)
                block_value.append((line[:5],line[6:]))
                self.title_blocks[str(block_num)] = block_value
                continue
    
            if line[:6] == "kernel":
                self.title_blocks[last_title].append((line[:6],line[7:]))
                continue
            
            if line[:6] == "initrd":
                self.title_blocks[last_title].append((line[:6],line[7:]))
                continue
                       
            if line[:6] == "append":
                self.title_blocks[last_title].append((line[:6],line[7:]))
                continue
    
    def get_title_blocks(self):
        return self.title_blocks   