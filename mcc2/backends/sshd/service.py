import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from mcc2.parsers.sshd.SshdConfig import SshdConfig
from mcc2.backends.policykit import check_authorization

__all__ = ['Sshd']

class Sshd(dbus.service.Object):
    def __init__(self):
        self.__bus = dbus.SystemBus()

        bus_name = dbus.service.BusName(
            "org.mandrivalinux.mcc2.Sshd",
            bus=self.__bus)

        dbus.service.Object.__init__(
            self,
            bus_name,
            "/org/mandrivalinux/mcc2/Sshd")

        self.__loop = gobject.MainLoop()
        self.__sshd = SshdConfig('/tmp/augeas-sandbox', 2)


    @dbus.service.method("org.mandrivalinux.mcc2.Sshd",
                         in_signature='s',
                         out_signature='s')
    def OptionValue(self, option):
        value = self.__sshd.get_option_value(option)
        if not value:
            msg = 'org.mandrivalinux.mcc2.Sshd.Error.OptionNotFound'
            raise dbus.exceptions.DBusException, msg
        return value


    @dbus.service.method("org.mandrivalinux.mcc2.Sshd",
                         out_signature='a(ss)')
    def ListOptions(self):
        return self.__sshd.get_options_as_str()


    @dbus.service.method("org.mandrivalinux.mcc2.Sshd",
                         in_signature='s',
                         out_signature='s')
    def RemoveOption(self, option):
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.sshd.removeoption')

        opt = self.__sshd.get_option(option)
        if not opt:
            msg = 'org.mandrivalinux.mcc2.Sshd.Error.OptionNotFound'
            raise dbus.exceptions.DBusException, msg
        result = self.__sshd.remove_option(opt)
        if result == -1:
            msg = 'org.mandrivalinux.mcc2.Sshd.Error.OptionRemoveError'
            raise dbus.exceptions.DBusException, msg
        return option


    def run(self):
        self.__loop.run()


    @classmethod
    def main(cls):
        sshd = cls()
        try:
            sshd.run()
        except KeyboardInterrupt:
            pass