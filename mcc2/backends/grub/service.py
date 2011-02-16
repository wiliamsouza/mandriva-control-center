import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from mcc2.parsers.grub.GrubConfig import GrubConfig

from mcc2.backends.policykit import check_authorization

__all__ = ['Grub']

class Grub(dbus.service.Object):
    def __init__(self):
        self.__bus = dbus.SystemBus()

        bus_name = dbus.service.BusName(
            "org.mandrivalinux.mcc2.Grub",
            bus=self.__bus)

        dbus.service.Object.__init__(
            self,
            bus_name,
            "/org/mandrivalinux/mcc2/Grub")

        self.__loop = gobject.MainLoop()
        self.__grub = grub = GrubConfig()
        self.__grub.parse()


    @dbus.service.method("org.mandrivalinux.mcc2.Grub",
                         out_signature='a{sv}')
    def ListTitles(self):
        return self.__grub.get_title_blocks()


    @dbus.service.method("org.mandrivalinux.mcc2.Grub",
                         in_signature='s',
                         out_signature='i')
    def SetDefaultBoot(self, name):
        """
        Set the default booted option to name.
    
        -1 set it to savedefault.
        Return 0 if successful.
        Return 1 if failed.
        """
        return self.__grub.set_default_boot(name)


    @dbus.service.method("org.mandrivalinux.mcc2.Grub",
                         out_signature='v')
    def GetDefaultBoot(self):
        """Return the name of the default booted option.
        
        Return -1 if it is savedefault.
        
        """
        return self.__grub.get_default_boot()


    @dbus.service.method("org.mandrivalinux.mcc2.Grub",
                         in_signature='i')
    def SetTimeout(self, timeout):
        """Set the timeout in seconds used in the Grub menu.
        active = bool whether timeout is used
        timeout = number of seconds
        """
        self.__grub.set_timeout(timeout)


    @dbus.service.method("org.mandrivalinux.mcc2.Grub",
                         out_signature='i')
    def GetTimeout(self):
        """Return the timeout in seconds used for Grub menu"""
        return self.__grub.get_timeout()


    @dbus.service.method("org.mandrivalinux.mcc2.Grub",
                         in_signature='i')
    def SetVgaCode(self, vga):
        """Set the resolution based on Grub vga code
        vga = integer, grub vga code
        """
        self.__grub.set_vga_code(vga)


    @dbus.service.method("org.mandrivalinux.mcc2.Grub",
                         out_signature='i')
    def GetVgaCode(self):
        """Return the Grub vga code used, as integer"""
        return self.__grub.get_vga_code()


    def run(self):
        self.__loop.run()


    @classmethod
    def main(cls):
        sshd = cls()
        try:
            sshd.run()
        except KeyboardInterrupt:
            pass