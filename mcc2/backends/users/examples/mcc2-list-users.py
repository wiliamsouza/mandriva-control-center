import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'com.mandriva.mcc2.Users',
    '/com/mandriva/mcc2/Users')
interface = dbus.Interface(proxy, 'com.mandriva.mcc2.Users')
for user in interface.Users():
    print user