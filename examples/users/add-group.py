import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Users',
    '/org/mandrivalinux/mcc2/Users')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')
result = interface.AddGroup('john', 666)
print result
