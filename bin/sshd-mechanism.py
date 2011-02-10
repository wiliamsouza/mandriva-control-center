#!/usr/bin/python

import sys
sys.path.append('/usr/share/mandriva/')

from mcc2.backends.sshd.service import Sshd
if __name__ == '__main__':
    Sshd.main()