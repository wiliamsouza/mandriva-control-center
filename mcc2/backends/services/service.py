import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

class Services(dbus.service.Object):
    def __init__(self):
        self.__bus = dbus.SystemBus()

        bus_name = dbus.service.BusName(
            "org.mandrivalinux.mcc2.Services",
            bus=self.__bus)

        dbus.service.Object.__init__(
            self,
            bus_name,
            "/org/mandrivalinux/mcc2/Services")

        self.__systemd_proxy = self.__bus.get_object(
            'org.freedesktop.systemd1',
            '/org/freedesktop/systemd1')

        self.__systemd_interface = dbus.Interface(
            self.__systemd_proxy,
            'org.freedesktop.systemd1.Manager')

        self._loop = gobject.MainLoop()


    @dbus.service.method("org.mandrivalinux.mcc2.Services",
                         in_signature='ss',
                         out_signature='o',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def Start(self, name, mode, sender, connection):
        """Start unit.
        
        @param name: Unit name (ie: network.service).
        @param mode: Must be one of "fail" or "replace".

        @raise dbus.DBusException:

        @rtype dbus.Interface: Job path.
        """
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.services.start')

        return self.__systemd_interface.StartUnit(name, mode)


    @dbus.service.method("org.mandrivalinux.mcc2.Services",
                         in_signature='ss',
                         out_signature='o',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def Stop(self, name, mode, sender, connection):
        """Stop unit.
        
        @param name: Unit name (ie: network.service).
        @param mode:  Must be one of "fail" or "replace".
        
        @raise dbus.DBusException:
        
        @rtype dbus.Interface: Job path.
        """
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.services.stop')

        return self.__systemd_interface.StopUnit(name, mode)


    @dbus.service.method("org.mandrivalinux.mcc2.Services",
                         in_signature='ss',
                         out_signature='o',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def Restart(self, name, mode, sender, connection):
        """Restart unit.
        
        @param name: Unit name (ie: network.service).
        @param mode: Must be one of "fail", "replace" or "isolate".
        
        @raise dbus.DBusException
        
        @rtype dbus.Interface: Job path.
        """
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.services.restart')

        return self.__systemd_interface.RestartUnit(name, mode)


    @dbus.service.method("org.mandrivalinux.mcc2.Services",
                         out_signature='a(ssssssouso)')
    def List(self):
        """List all units, inactive units too.
        
        @raise dbus.DBusException.
        
        @rtype dbus.Array:
        """
        return self.__systemd_interface.ListUnits()


    @dbus.service.method("org.mandrivalinux.mcc2.Services",
                         in_signature='s',
                         out_signature='a{sv}')
    def ServiceDetails(self, path):
        """Services Detail.
        
        @param path: Unit path.
        
        @raise dbus.DBusException.
        
        @rtype dbus.Array:
        """
        unit_proxy = self.__bus.get_object(
            'org.freedesktop.systemd1',
            path)

        properties_interface = dbus.Interface(
            unit_proxy,
            'org.freedesktop.DBus.Properties')

        return properties_interface.GetAll('org.freedesktop.systemd1.Unit')


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
            msg = 'org.mandrivalinux.mcc2.Services.Error.NotAuthorized'
            raise dbus.DBusException, msg


    def run(self):
        self._loop.run()


    @classmethod
    def main(cls):
        services = cls()
        try:
            services.run()
        except KeyboardInterrupt:
            pass