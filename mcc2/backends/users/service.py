import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

import libuser

MAX_USERNAME_LENGTH = libuser.UT_NAMESIZE - 1
MAX_GROUPNAME_LENGTH = libuser.UT_NAMESIZE - 1

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
                         in_signature='si',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def AddGroup(self, name, gid, sender, connection):
        """Add Group.
        
        @param name: Group name
        @param gid: Group ID
        
        @raise dbus.DBusException:
        
        @rtype: The GID from recently created Group.
        """
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.users.addgroup')
        init_group = self.__libuser.initGroup(name)
        init_group.set(libuser.GIDNUMBER, gid)
        try:
            self.__libuser.addGroup(init_group)
        except RuntimeError, error:
            msg = 'org.mandrivalinux.mcc2.Users.Error.AddGroupFailed'
            #FIXME: What's the others libuser errors?
            if str(error) == 'entry already present in file':
                msg = 'org.mandrivalinux.mcc2.Users.Error.GroupAlreadyExist'
            raise dbus.DBusException, msg
        group_entity = self.__libuser.lookupGroupByName(name)
        gid = group_entity.get(libuser.GIDNUMBER)[0]
        return dbus.Int32(gid)

    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='a{sv}',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def AddUser(self, user_info, sender, connection):
        """Add User.
        
        @param user_info: {
                            'full_name': 'John Doe',
                            'login': 'john',
                            'shell': '/bin/bash',
                            'uid': 666,
                            'gid': 666,
                            'create_home': True,
                            'home_directory': '/home/john',
                            'password': 'secret'
                        }
        
        @raise dbus.DBusException:
        
        @rtype: The UID from recently created User.
        """
        self.check_authorization(sender, connection,
            'org.mandrivalinux.mcc2.users.adduser')
        user_entity = self.__libuser.initUser(user_info['login'])
        user_entity.set(libuser.GECOS, [user_info['full_name']])
        user_entity.set(libuser.GIDNUMBER, [user_info['gid']])
        user_entity.set(libuser.UIDNUMBER, [user_info['uid']])
        user_entity.set(libuser.HOMEDIRECTORY, [user_info['home_directory']])
        user_entity.set(libuser.LOGINSHELL, [user_info['shell']])
        try:
            self.__libuser.addUser(
                user_entity,
                mkhomedir = user_info['create_home'])
        except RuntimeError, error:
            msg = 'org.mandrivalinux.mcc2.Users.Error.AddUserFailed'
            # FIXME: What's the others libuser errors?
            if str(error) == 'entry already present in file':
                msg = 'org.mandrivalinux.mcc2.Users.Error.UserAlreadyExist'
            raise dbus.DBusException, msg
        self.__libuser.setpassUser(user_entity, user_info['password'], 0)
        user_entity = self.__libuser.lookupUserByName(user_info['login'])
        uid = user_entity.get(libuser.UIDNUMBER)[0]
        return dbus.Int32(uid)

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
        return {'gid': dbus.String(gid), 'name': dbus.String(name)}

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
        return {'uid': dbus.String(uid), 'name': dbus.String(name)}

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

    #This method should be used only internaly
    #@dbus.service.method("org.mandrivalinux.mcc2.Users",
    #                     out_signature='as')
    #def GroupsFull(self):
    #    return self.__libuser.enumerateGroupsFull()

    #TODO: Rename to ListUsers
    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='as')
    def Users(self):
        return self.__libuser.enumerateUsers()

    #TODO: Rename to ListUsersByGroup
    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='as')
    def UsersByGroup(self, group):
        return self.__libuser.enumerateUsersByGroup(group)

    #This method should be used only internaly
    #@dbus.service.method("org.mandrivalinux.mcc2.Users",
    #                     out_signature='as')
    #def UsersFull(self):
    #    return self.__libuser.enumerateUsersFull()

    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='i')
    def FirstUnusedGid(self):
        return dbus.Int32(self.__libuser.getFirstUnusedGid())

    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='i')
    def FirstUnusedUid(self):
        return dbus.Int32(self.__libuser.getFirstUnusedGid())

    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='as')
    def UserShells(self):
        return self.__libuser.getUserShells()

    #@dbus.service.method("org.mandrivalinux.mcc2.Users",
    #                     in_signature='s',
    #                     out_signature='s')
    #def ModifyGroup(self):
    #    pass

    #@dbus.service.method("org.mandrivalinux.mcc2.Users",
    #                     in_signature='s',
    #                     out_signature='s')
    #def ModifyUser(self):
    #    pass

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