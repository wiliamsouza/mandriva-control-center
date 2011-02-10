import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from mcc2.parsers.sshd.SshdConfig import SshdConfig

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
        return self.__sshd.get_option_value(option)


    @dbus.service.method("org.mandrivalinux.mcc2.Sshd",
                         out_signature='a(ss)')
    def ListOptions(self):
        return self.__sshd.get_options_as_str()


    def check_authorization(self, sender, connection, action):
        """Check policykit authorization.
        
        @param sender:
        @param connection:
        @param action:
        
        @raise dbus.DBusException: SystemServices.Error.NotAuthorized.
        """
        dbus_proxy = connection.get_object(
            'org.freedesktop.DBus',
            '/org/freedesktop/DBus/Bus')

        dbus_interface = dbus.Interface(
            dbus_proxy,
            'org.freedesktop.DBus')

        pid = dbus_interface.GetConnectionUnixProcessID(sender)

        policekit_proxy = self.__bus.get_object(
            'org.freedesktop.PolicyKit1',
            '/org/freedesktop/PolicyKit1/Authority')

        policekit_interface = dbus.Interface(
            policekit_proxy,
            'org.freedesktop.PolicyKit1.Authority')

        subject = (
            'unix-process',
            {'pid': dbus.UInt32(pid, variant_level=1),
             'start-time': dbus.UInt64(0, variant_level=1)}
        )

        detail = {'':''}
        flags = dbus.UInt32(1)
        cancellation = ''

        (is_auth, _, details) = policekit_interface.CheckAuthorization(
            subject, action, detail, flags, cancellation, timeout=600)

        if not is_auth:
            msg = 'org.mandrivalinux.mcc2.Sshd.Error.NotAuthorized'
            raise dbus.exceptions.DBusException, msg


    def run(self):
        self.__loop.run()


    @classmethod
    def main(cls):
        sshd = cls()
        try:
            sshd.run()
        except KeyboardInterrupt:
            pass