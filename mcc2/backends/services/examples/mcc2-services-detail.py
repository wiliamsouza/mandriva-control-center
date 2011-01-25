import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'com.mandriva.mcc2.Services',
    '/com/mandriva/mcc2/Services')
interface = dbus.Interface(proxy, 'com.mandriva.mcc2.Services')
for service in interface.list():
    details = interface.service_details(service[6])
    for key, value in details.items():
        print '%s: %s' % (key, value)
    print '-'*80
