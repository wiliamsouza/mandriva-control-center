import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'com.mandriva.mcc2.Services',
    '/com/mandriva/mcc2/Services')
interface = dbus.Interface(proxy, 'com.mandriva.mcc2.Services')
print interface.stop('crond.service', 'fail')