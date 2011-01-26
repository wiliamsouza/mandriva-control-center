import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Services',
    '/org/mandrivalinux/mcc2/Services')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Services')
for service in interface.List():
    details = interface.ServiceDetails(service[6])
    for key, value in details.items():
        print '%s: %s' % (key, value)
    print '-'*80
