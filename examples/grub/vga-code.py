import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Grub',
    '/org/mandrivalinux/mcc2/Grub')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Grub')
print 'Vga code: %i' % interface.VgaCode()