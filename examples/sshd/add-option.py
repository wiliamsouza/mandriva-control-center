import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Sshd',
    '/org/mandrivalinux/mcc2/Sshd')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Sshd')

try:
    print interface.OptionValue('X11Forwarding', '1')
except dbus.exceptions.DBusException, msg:
    print msg

print interface.AddOption('X11Forwarding', 'yes', '1')

print interface.OptionValue('X11Forwarding', '1')
