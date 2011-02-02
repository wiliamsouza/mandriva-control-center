#!/usr/bin/python

import sys
sys.path.append('/usr/share/mcc2/')

from mcc2.backends.services.service import Services
if __name__ == '__main__':
    Services.main()