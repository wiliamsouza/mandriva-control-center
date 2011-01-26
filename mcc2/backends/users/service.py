import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

import libuser

class Users(dbus.service.Object):
    def __init__(self):
        self.__bus = dbus.SystemBus()
        bus_name = dbus.service.BusName(
            "org.mandrivalinux.mcc2.Users",
            bus=self.__bus)
        dbus.service.Object.__init__(
            self,
            bus_name,
            "/org/mandrivalinux/mcc2/Users")

        self._loop = gobject.MainLoop()

        self.__libuser = libuser.admin()


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='a{sv}',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def AddGroup(self, group, sender, connection):
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.users.addgroup')
        init_group = self.__libuser.initGroup(group)
        try:
            self.__libuser.addGroup(init_group)
        except RuntimeError, error:
            msg = 'org.mandrivalinux.mcc2.Users.Error.AddGroupFailed'
            #FIXME: What's the others libuser errors?
            if str(error) == 'entry already present in file':
                msg = 'org.mandrivalinux.mcc2.Users.Error.GroupAlreadyExist'
            raise dbus.DBusException, msg
        group_entity = self.__libuser.lookupGroupByName(group)
        gid = group_entity.get(libuser.GIDNUMBER)[0]
        name = group_entity.get(libuser.GROUPNAME)[0]
        return {'gid': gid, 'name': name}

    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='a{sv}',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def AddUser(self, user, sender, connection):
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.users.adduser')
        init_user = self.__libuser.initUser(user)
        try:
            self.__libuser.addUser(init_user)
        except RuntimeError, error:
            msg = 'org.mandrivalinux.mcc2.Users.Error.AddUserFailed'
            # FIXME: What's the others libuser errors?
            if str(error) == 'entry already present in file':
                msg = 'org.mandrivalinux.mcc2.Users.Error.UserAlreadyExist'
            raise dbus.DBusException, msg
        user_entity = self.__libuser.lookupUserByName(user)
        uid = user_entity.get(libuser.UIDNUMBER)[0]
        name = user_entity.get(libuser.USERNAME)[0]
        return {'uid': uid, 'name': name}

    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='a{sv}',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def DeleteGroup(self, group, sender, connection):
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.users.deletegroup')
        group_entity = self.__libuser.lookupGroupByName(group)
        gid = group_entity.get(libuser.GIDNUMBER)[0]
        name = group_entity.get(libuser.GROUPNAME)[0]
        init_group = self.__libuser.initGroup(group)
        try:
            self.__libuser.deleteGroup(init_group)
        except RuntimeError, error:
            msg = 'org.mandrivalinux.mcc2.Users.Error.DeleteGroupFailed'
            raise dbus.DBusException, msg
        return {'gid': gid, 'name': name}

    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='a{sv}',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def DeleteUser(self, user, sender, connection):
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.users.deleteuser')
        user_entity = self.__libuser.lookupUserByName(user)
        uid = user_entity.get(libuser.UIDNUMBER)[0]
        name = user_entity.get(libuser.USERNAME)[0]
        init_user = self.__libuser.initUser(user)
        try:
            self.__libuser.deleteUser(init_user)
        except RuntimeError, error:
            msg = 'org.mandrivalinux.mcc2.Users.Error.DeleteUserFailed'
            raise dbus.DBusException, msg
        return {'uid': uid, 'name': name}

    #TODO: Rename to ListGroups
    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='as')
    def Groups(self):
        return self.__libuser.enumerateGroups()

    #TODO: Rename to ListGroupsByUser
    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='as')
    def GroupsByUser(self, user):
        return self.__libuser.enumerateGroupsByUser(user)

    #FIXME: Remove this method should be used only internaly
    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='as')
    def GroupsFull(self):
        return self.__libuser.enumerateGroupsByUser()

    #TODO: Rename to ListUsers
    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='as')
    def Users(self):
        return self.__libuser.enumerateUsers()

    #TODO: Rename to ListUsersByGroup
    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='as')
    def UsersByGroup(self, user):
        return self.__libuser.enumerateUsersByGroup(user)

    #FIXME: Remove this method should be used only internaly
    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='as')
    def UsersFull(self):
        return self.__libuser.enumerateUsersFull()

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
            msg= 'org.mandrivalinux.mcc2.Users.Error.NotAuthorized'
            raise dbus.DBusException, msg

    def run(self):
        self._loop.run()

    @classmethod
    def main(cls):
        users = cls()
        try:
            users.run()
        except KeyboardInterrupt:
            pass