import time

import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Users',
    '/org/mandrivalinux/mcc2/Users')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')
result = interface.UserDetails('bedi')
print result['uid']
print result['gid']
print result['userName']
print result['fullName']
print result['homeDirectory']
print result['loginShell']

print result['shadowExpire']

if result['shadowExpire']:
    days = int(result['shadowExpire'])
    tmp = days * int(24 * 60 * 60)
    age = time.localtime(tmp)
    print time.strftime('%Y %m %d', age)
else:
    print result['shadowExpire']

print result['shadowMin']
print result['shadowMax']
print result['shadowWarning']
print result['shadowInactive']
print result['shadowLastChange']
