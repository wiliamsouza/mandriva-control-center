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


    def run(self):
        self.__loop.run()


    @classmethod
    def main(cls):
        sshd = cls()
        try:
            sshd.run()
        except KeyboardInterrupt:
            pass