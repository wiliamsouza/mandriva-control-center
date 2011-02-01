import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Users',
    '/org/mandrivalinux/mcc2/Users')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')

user_info = {
    'old_username': 'john',
    'fullname': 'Johns Does',
    'username': 'johns',
    'shell': '/bin/bash',
    'uid': 666,
    'gid': 666,
    'home_directory': '/home/john',
    'password': 'secret2',
    #'shadow_expire': 'YYYY-MM-DD',
    #'shadow_min': 0,
    #'shadow_max', 99999,
    #'shadow_warning': 7,
    #'shadow_inactive': -1,
    #'shadow_last_change': 'YYYY-MM-DD'
    }
        



result = interface.ModifyUser(user_info)
print result   