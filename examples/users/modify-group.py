import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Users',
    '/org/mandrivalinux/mcc2/Users')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')

group_info = {
    'groupname': 'john',
    'new_groupname': 'johns',
    'members': ['users', 'wheel', 'john']
    }

result = interface.ModifyGroup(group_info)
print result