#!/usr/bin/python

import sys
sys.path.append('/usr/share/mandriva/')

from mcc2.backends.services.service import Services
if __name__ == '__main__':
    Services.main()