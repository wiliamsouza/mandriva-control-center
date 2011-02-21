import ConfigParser
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
            'org.mandrivalinux.mcc2.Grub',
            bus=self.__bus)

        dbus.service.Object.__init__(
            self,
            bus_name,
            '/org/mandrivalinux/mcc2/Grub')

        self.__loop = gobject.MainLoop()
        self.__grub = grub = GrubConfig()
        self.__grub.parse()
        self.__action = 'org.mandrivalinux.mcc2.auth_admin_keep'

        config = ConfigParser.ConfigParser()
        config.read('/usr/share/mandriva/config/mcc2.cfg')
        policy_level = config.get('policy', 'level')

        if policy_level == 'application':
            self.__action = 'org.mandrivalinux.mcc2.grub.auth_admin_keep'

        if policy_level == 'method':
            self.__action = None


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         out_signature='a{sv}')
    def ListTitles(self):
        return self.__grub.get_title_blocks()


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         in_signature='s',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def ChangeDefaultBoot(self, name, sender, connection):
        """
        Change the default booted option to name.
    
        -1 set it to savedefault.
        Return 0 if successful.
        Return 1 if failed.
        """
        check_authorization(sender, connection, self.__action)

        return self.__grub.set_default_boot(name)


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         out_signature='v')
    def DefaultBoot(self):
        """Return the name of the default booted option.
        
        Return -1 if it is savedefault.
        
        """
        return self.__grub.get_default_boot()


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         in_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def ChangeTimeout(self, timeout, sender, connection):
        """Change the timeout in seconds used in the Grub menu.
        active = bool whether timeout is used
        timeout = number of seconds
        """
        check_authorization(sender, connection, self.__action)

        self.__grub.set_timeout(timeout)


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         out_signature='i')
    def Timeout(self):
        """Return the timeout in seconds used for Grub menu"""
        return self.__grub.get_timeout()


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         in_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def ChangeVgaCode(self, vga, sender, connection):
        """Change the resolution based on Grub vga code
        vga = integer, grub vga code
        """
        check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.grub.rootpassword')

        self.__grub.set_vga_code(vga)


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         out_signature='i')
    def VgaCode(self):
        """Return the Grub vga code used, as integer"""
        return self.__grub.get_vga_code()


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         in_signature='b',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def ChangePasswordProtection(self, active, sender, connection):
        """Change whether the Grub menu is password protected
        
        @param active: boolean
        
        @return dbus.Bollean
        """
        check_authorization(sender, connection, self.__action)

        self.__grub.set_password_protection(active)


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         out_signature='b')
    def PasswordProtection(self):
        """Boolean, returns whether the Grub menu is password protected"""
        return self.__grub.get_password_protection()


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         in_signature='b',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def ChangeProtectRescueMode(self, active, sender, connection):
        """Change whether the alternate boot option is password protected
        active = boolean
        """
        check_authorization(sender, connection, self.__action)

        self.__grub.Change_protect_rescuemode(active)


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         out_signature='b')
    def ProtectRescueMode(self):
        """Boolean, returns whether the alternate boot option
        is password protected
        """
        return self.__grub.get_protect_rescuemode()


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         in_signature='b',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def ChangeProtectOldMode(self, active, sender, connection):
        """Change whether old boot options are password protected
        active = boolean
        """
        check_authorization(sender, connection, self.__action)

        self.__grub.Change_protect_oldmode(active)


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         out_signature='b')
    def ProtectOldMode(self):
        """Boolean, returns whether old boot options are password protected"""
        return self.__grub.get_protect_oldmode()


    @dbus.service.method('org.mandrivalinux.mcc2.Grub',
                         out_signature='sb',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def UpdatePassword(self, password, active, sender, connection):
        """Change password for grub menu, and whether
        password protection is active
        
        active = boolean
        password = string, must be at least four characters
        """
        check_authorization(sender, connection, self.__action)

        self.__grub.update_password(password, active)


    def run(self):
        self.__loop.run()


    @classmethod
    def main(cls):
        sshd = cls()
        try:
            sshd.run()
        except KeyboardInterrupt:
            pass