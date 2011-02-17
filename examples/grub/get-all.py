import dbus
bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Grub',
    '/org/mandrivalinux/mcc2/Grub')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Grub')

print 'Default boot: %s' % interface.DefaultBoot()
print 'Password protection: %i' % interface.PasswordProtection()
print 'Protect old mode: %i' % interface.ProtectOldMode()
print 'Protect recue mode: %i' % interface.ProtectRescueMode()
print 'Timeout: %i' % interface.Timeout()
print 'Vga code: %i' % interface.VgaCode()