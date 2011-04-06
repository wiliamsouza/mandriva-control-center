import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Users',
    '/org/mandrivalinux/mcc2/Users')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')


import time
import math

date = '2011-04-06'

year = None
month = None
day = None

(year, month, day) = date.split('-')

try:
    tmp = time.mktime([int(year), int(month), int(day), 0, 0, 0, 0, 0, -1])
except OverflowError:
    print 'The year is out of range.  Please select a different year'

seconds = 24 * 60 * 60
days_expire = tmp / seconds
fraction, integer = math.modf(days_expire)

if fraction == 0.0:
    days_expire = integer
else:
    days_expire = integer + 1


print int(days_expire)

user_info = {
    'username': 'john',
    'new_username': 'johns',
    'fullname': 'Johns Does',
    'shell': '/bin/bash',
    'uid': 666,
    'gid': 666,
    'home_directory': '/home/john',
    'password': 'secret2',
    #'shadow_expire': days_expire,
    #'shadow_min': 0,
    #'shadow_max', 99999,
    #'shadow_warning': 7,
    #'shadow_inactive': -1,
    #'shadow_last_change': 'YYYY-MM-DD'
    }

#result = interface.ModifyUser(user_info)
#print result   