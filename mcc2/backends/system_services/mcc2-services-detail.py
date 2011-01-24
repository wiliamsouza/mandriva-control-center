import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'com.mandriva.mcc2.SystemServices',
    '/com/mandriva/mcc2/SystemServices')
interface = dbus.Interface(proxy, 'com.mandriva.mcc2.SystemServices')
for service in interface.list():
    details = interface.service_details(service[6])
    print details['Id']
    #for key, value in details.items():
    #    print key, value
    print '-'*80
