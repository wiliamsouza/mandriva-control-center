import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Sshd',
    '/org/mandrivalinux/mcc2/Sshd')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Sshd')
for option in interface.ListOptions():
    print 'Option: %s\n Value: %s\n Number: %s\n' % option