import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'com.mandriva.mcc2.Services',
    '/com/mandriva/mcc2/Services')
interface = dbus.Interface(proxy, 'com.mandriva.mcc2.Services')
for service in interface.list():
    for s in service:
        print s
    print '-'*80