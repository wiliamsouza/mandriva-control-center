import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Services',
    '/org/mandrivalinux/mcc2/Services')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Services')
print interface.Stop('crond.service', 'fail')