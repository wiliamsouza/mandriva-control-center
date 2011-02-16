#!/usr/bin/python

import sys
sys.path.append('/usr/share/mandriva/')

from mcc2.backends.grub.service import Grub
if __name__ == '__main__':
    Grub.main()