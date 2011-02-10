#!/usr/bin/python

import sys
sys.path.append('/usr/share/mandriva/')

from mcc2.backends.users.service import Users
if __name__ == '__main__':
    Users.main()