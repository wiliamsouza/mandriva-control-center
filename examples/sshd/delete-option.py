import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Sshd',
    '/org/mandrivalinux/mcc2/Sshd')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Sshd')
print interface.OptionValue('X11Forwarding', '1')
print interface.DeleteOption('X11Forwarding', '1')
print interface.OptionValue('X11Forwarding', '1')