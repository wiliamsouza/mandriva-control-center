import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from mcc2.parsers.sshd.SshdConfig import SshdConfig
from mcc2.parsers.sshd.mcc2options import MccOption, MccMultiValueOption

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
        self.__sshd = SshdConfig('/tmp/augeas-sandbox', 0)


    @dbus.service.method("org.mandrivalinux.mcc2.Sshd",
                         in_signature='ss',
                         out_signature='s')
    def OptionValue(self, option, number):
        value = self.__sshd.get_option_value(option, number)
        if not value:
            msg = 'org.mandrivalinux.mcc2.Sshd.Error.OptionNotFound'
            raise dbus.exceptions.DBusException, msg
        return value


    @dbus.service.method("org.mandrivalinux.mcc2.Sshd",
                         out_signature='a(sss)')
    def ListOptions(self):
        return self.__sshd.get_options_as_str()


    @dbus.service.method("org.mandrivalinux.mcc2.Sshd",
                         in_signature='ss',
                         out_signature='s',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def DeleteOption(self, option, number, sender, connection):
        check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.sshd.deleteoption')

        opt = self.__sshd.get_option(option, number)
        if not opt:
            msg = 'org.mandrivalinux.mcc2.Sshd.Error.OptionNotFound'
            raise dbus.exceptions.DBusException, msg
        result = self.__sshd.remove_option(opt)
        if result == -1:
            msg = 'org.mandrivalinux.mcc2.Sshd.Error.DeleteOptionError'
            raise dbus.exceptions.DBusException, msg
        return option


    @dbus.service.method("org.mandrivalinux.mcc2.Sshd",
                         in_signature='svs',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def AddOption(self, option, value, number, sender, connection):
        check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.sshd.addoption')
        opt = None
        if isinstance(value, dbus.Array):
            print 'Creating MccMultiValueOption'
            opt = MccMultiValueOption(name=option, value=value)
        elif isinstance(value, dbus.String):
            print 'Creating MccOption'
            opt = MccOption(name=option, value=value, num=number)
        else:
            msg = 'org.mandrivalinux.mcc2.Sshd.Error.UnsupportedType'
            raise dbus.exceptions.DBusException, msg
        print self.__sshd.set_option(opt)
        return 1


    def run(self):
        self.__loop.run()


    @classmethod
    def main(cls):
        sshd = cls()
        try:
            sshd.run()
        except KeyboardInterrupt:
            pass