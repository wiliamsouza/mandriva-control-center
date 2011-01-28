import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Users',
    '/org/mandrivalinux/mcc2/Users')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')

# first add a group
gid = interface.AddGroup('john', 666)

user_info = {
    'full_name': 'John Doe',
    'login': 'john',
    'shell': '/bin/bash',
    'uid': 666,
    'gid': gid,
    'create_home': True,
    'home_directory': '/home/john',
    'password': 'secret'
    }

result = interface.AddUser(user_info)
print result   