import ConfigParser
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
from mcc2.backends.policykit import check_authorization

__all__ = ['Services']

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

        self.is_systemd_running = False

        try:
            self.__systemd_proxy = self.__bus.get_object(
                'org.freedesktop.systemd1',
                '/org/freedesktop/systemd1')

            self.__systemd_interface = dbus.Interface(
                self.__systemd_proxy,
                'org.freedesktop.systemd1.Manager')

            self.is_systemd_running = True

        except dbus.exceptions.DBusException, error:
            # If systemd is not running don`t raise an exception,
            # all bus method may use self.is_systemd_running and raise
            # org.mandrivalinux.mcc2.Services.Error.SystemdNotRunning
            systemd_error = 'org.freedesktop.DBus.Error.Spawn.ChildExited'
            if error.get_dbus_name() == systemd_error:
                pass

        self.__loop = gobject.MainLoop()
        self.msg = {
            'not_running':'org.mandrivalinux.mcc2.Services.Error.SystemdNotRunning'
            }

        self.__action = 'org.mandrivalinux.mcc2.auth_admin_keep'

        config = ConfigParser.ConfigParser()
        config.read('/usr/share/mandriva/config/mcc2.cfg')
        policy_level = config.get('policy', 'level')

        if policy_level == 'application':
            self.__action = 'org.mandrivalinux.mcc2.services.auth_admin_keep'

        if policy_level == 'method':
            self.__action = None


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
        if not self.is_systemd_running:
            raise dbus.DBusException, self.msg['not_running']

        check_authorization(sender, connection, self.__action)

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
        if not self.is_systemd_running:
            raise dbus.DBusException, self.msg['not_running']

        check_authorization(sender, connection, self.__action)

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
        if not self.is_systemd_running:
            raise dbus.DBusException, self.msg['not_running']

        check_authorization(sender, connection, self.__action)

        return self.__systemd_interface.RestartUnit(name, mode)


    @dbus.service.method("org.mandrivalinux.mcc2.Services",
                         out_signature='a(ssssssouso)')
    def List(self):
        """List all units, inactive units too.
        
        @raise dbus.DBusException.
        
        @rtype dbus.Array:
        """
        if not self.is_systemd_running:
            raise dbus.DBusException, self.msg['not_running']

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
        if not self.is_systemd_running:
            raise dbus.DBusException, self.msg['not_running']

        unit_proxy = self.__bus.get_object(
            'org.freedesktop.systemd1',
            path)

        properties_interface = dbus.Interface(
            unit_proxy,
            'org.freedesktop.DBus.Properties')

        return properties_interface.GetAll('org.freedesktop.systemd1.Unit')


    @dbus.service.method('org.mandrivalinux.mcc2.Services',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def StopInterface(self, sender, connection):
        self.__loop.quit()


    def run(self):
        self.__loop.run()


    @classmethod
    def main(cls):
        services = cls()
        try:
            services.run()
        except KeyboardInterrupt:
            pass