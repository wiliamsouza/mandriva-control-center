import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Services',
    '/org/mandrivalinux/mcc2/Services')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Services')
for service in interface.List():
    for s in service:
        print s
    print '-'*80