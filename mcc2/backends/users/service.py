import ConfigParser
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
import math
import libuser
from datetime import date, timedelta
from mcc2.backends.policykit import check_authorization

#TODO: make a method to this
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
        self.__action = 'org.mandrivalinux.mcc2.auth_admin_keep'

        config = ConfigParser.ConfigParser()
        config.read('/usr/share/mandriva/config/mcc2.cfg')
        policy_level = config.get('policy', 'level')

        if policy_level == 'application':
            self.__action = 'org.mandrivalinux.mcc2.users.auth_admin_keep'

        if policy_level == 'method':
            self.__action = None


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='si',
                         out_signature='t',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def AddGroup(self, groupname, gid, sender, connection):
        """Add Group.
        
        @param groupname: Group name
        @param gid: Group ID
        
        @raise dbus.DBusException:
        
        @rtype dbus.Int64: The GID from recently created Group.
        """
        check_authorization(sender, connection, self.__action)
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.addgroup')

        init_group = self.__libuser.initGroup(groupname)
        init_group.set(libuser.GIDNUMBER, gid)

        try:
            self.__libuser.addGroup(init_group)
        except RuntimeError, error:
            msg = 'org.mandrivalinux.mcc2.Users.Error.AddGroupFailed'

            #FIXME: What's the others libuser errors?
            if str(error) == 'entry already present in file':
                msg = 'org.mandrivalinux.mcc2.Users.Error.GroupAlreadyExist'

            raise dbus.DBusException, msg

        group_entity = self.__libuser.lookupGroupByName(groupname)
        gid = group_entity.get(libuser.GIDNUMBER)[0]

        return dbus.Int64(gid)


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='a{sv}',
                         out_signature='t',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def AddUser(self, user_info, sender, connection):
        """Add User.

        @param group_info: A dbus.Dictionary with user information with
        the following content:

            * fullname:
            * username:
            * shell:
            * uid:
            * gid:
            * home_directory:
            * password:

        Example:
        user_info = {
                'fullname': 'John Doe',
                'username': 'john',
                'shell': '/bin/bash',
                'uid': 666,
                'gid': 666,
                'home_directory': '/home/john',
                'password': 'secret'
                }

        @raise dbus.DBusException:

        @return dbus.Int64: The UID from recently created User.
        """
        check_authorization(sender, connection, self.__action)
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.adduser')

        user_entity = self.__libuser.initUser(user_info['username'])
        user_entity.set(libuser.GECOS, [user_info['fullname']])
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

        user_entity = self.__libuser.lookupUserByName(user_info['username'])
        uid = user_entity.get(libuser.UIDNUMBER)[0]

        return dbus.Int64(uid)


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='a{sv}',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def DeleteGroup(self, groupname, sender, connection):
        """Delete a Group.
        
        @param groupname: Group name.
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Dictionary: Recent removed group id and groupname.
        """
        check_authorization(sender, connection, self.__action)
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.deletegroup')

        group_entity = self.__libuser.lookupGroupByName(groupname)
        gid = group_entity.get(libuser.GIDNUMBER)[0]
        name = group_entity.get(libuser.GROUPNAME)[0]

        init_group = self.__libuser.initGroup(groupname)

        try:
            self.__libuser.deleteGroup(init_group)
        except RuntimeError, error:
            msg = 'org.mandrivalinux.mcc2.Users.Error.DeleteGroupFailed'
            raise dbus.DBusException, msg

        return dbus.Dictionary(
            {
            'gid': dbus.Int64(gid),
            'groupname': dbus.String(name)
            }, signature=dbus.Signature('sv'))


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='a{sv}',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def DeleteUser(self, username, sender, connection):
        """Delete an User.
        
        @param username: User name.
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Dictionary: Recent removed user id and groupname.
        """
        check_authorization(sender, connection, self.__action)
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.deleteuser')

        user_entity = self.__libuser.lookupUserByName(username)
        uid = user_entity.get(libuser.UIDNUMBER)[0]
        name = user_entity.get(libuser.USERNAME)[0]
        #user_entity = self.__libuser.initUser(username)

        try:
            self.__libuser.deleteUser(user_entity)
        except RuntimeError, error:
            msg = 'org.mandrivalinux.mcc2.Users.Error.DeleteUserFailed'
            raise dbus.DBusException, msg

        return dbus.Dictionary(
            {
            'uid': dbus.Int64(uid),
            'username': dbus.String(username)
            }, signature=dbus.Signature('sv'))


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='as')
    def ListGroups(self):
        """List All Groups.
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Array: All groups
        """
        return self.__libuser.enumerateGroups()


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='as')
    def ListGroupsByUser(self, username):
        """List Group by User.
        
        @param username: User name.
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Array: Groups this user is in.
        """
        return self.__libuser.enumerateGroupsByUser(username)


    #This method should be used only internaly
    #@dbus.service.method("org.mandrivalinux.mcc2.Users",
    #                     out_signature='as')
    #def GroupsFull(self):
    #    return self.__libuser.enumerateGroupsFull()


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='as')
    def ListUsers(self):
        """List All Users.
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Array: All users
        """
        return self.__libuser.enumerateUsers()


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='as')
    def ListUsersByGroup(self, groupname):
        """List Users by Group.
        
        @param groupname: Group name.
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Array: Users in this group.
        """
        return self.__libuser.enumerateUsersByGroup(groupname)


    #This method should be used only internaly
    #@dbus.service.method("org.mandrivalinux.mcc2.Users",
    #                     out_signature='as')
    #def UsersFull(self):
    #    return self.__libuser.enumerateUsersFull()


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='t')
    def FirstUnusedGid(self):
        """First Unused Gid.
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Int32: First unused gid.
        """
        return dbus.Int64(self.__libuser.getFirstUnusedGid())


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='t')
    def FirstUnusedUid(self):
        """First Unused Uid.
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Int32:
        """
        return dbus.Int64(self.__libuser.getFirstUnusedUid())


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         out_signature='as')
    def ListUserShells(self):
        """List Shell available.
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Array: shell list.
        """
        return self.__libuser.getUserShells()


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='i')
    def GroupIsLocked(self, group):
        """Check if Group is Locked.
        
        @param group: A group name to check
        
        @raise dbus.DBusException:
        
        @rtype: dbus.Int32, 1 locked or 0 unlocked.
        """
        group_entity = self.__libuser.lookupGroupByName(group)
        
        return dbus.Int32(self.__libuser.groupIsLocked(group_entity))


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def LockGroup(self, groupname, sender, connection):
        """Lock Group.
        
        @param username: A dbus.String with group name as it value.

        @raise dbus.DBusException:
        
        @rtype dbus.Int32: 1 ok or 0 fail.
        """
        #
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.lockgroup')

        group_entity = self.__libuser.lookupGroupByName(groupname)

        return dbus.Int32(self.__libuser.lockGroup(group_entity))


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def UnlockGroup(self, groupname, sender, connection):
        """ Unlock group
        
        @param groupname: A dbus.String with group name as it value.

        @raise dbus.DBusException:
        
        @rtype dbus.Int32: 1 ok or 0 fail.
        """
        check_authorization(sender, connection, self.__action)
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.unlockgroup')

        group_entity = self.__libuser.lookupGroupByName(groupname)

        return dbus.Int32(self.__libuser.unlockGroup(group_entity))


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='i')
    def UserIsLocked(self, username):
        """Check is User Locked.
        
        @param username: A dbus.String with user name as it value.

        @raise dbus.DBusException:
        
        @rtype dbus.Int32: 1 ok or 0 fail.
        """
        user_entity = self.__libuser.lookupUserByName(username)

        return dbus.Int32(self.__libuser.userIsLocked(user_entity))


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def LockUser(self, username, sender, connection):
        """Lock User.
        
        @param username: A dbus.String with user name as it value.

        @raise dbus.DBusException:
        
        @rtype dbus.Int32: 1 ok or 0 fail.
        """
        check_authorization(sender, connection, self.__action)
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.lockuser')

        user_entity = self.__libuser.lookupUserByName(username)

        return dbus.Int32(self.__libuser.LockUser(user_entity))


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='s',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def UnlockUser(self, username, sender, connection):
        """ Unlock user
        
        @param username: A dbus.String with user name as it value.

        @raise dbus.DBusException:
        
        @rtype dbus.Int32: 1 ok or 0 fail.
        """
        check_authorization(sender, connection, self.__action)
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.unlockuser')

        user_entity = self.__libuser.lookupUserByName(username)

        return dbus.Int32(self.__libuser.unlockUser(user_entity))


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='a{sv}',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def ModifyGroup(self, group_info, sender, connection):
        """Modify Group.
        
        @param group_info:A dbus.Dictionary with user information with
        the following content:

            * groupname:
            * new_groupname: This is optional.
            * members:
        
        Example:
        group_info = {
                'groupname': 'john',
                'new_groupname': 'johns'
                'members': ['john', 'users', 'wheel']
                }
        
        @raise dbus.DBusException:
        
        @rtype dbus.Int32: 1 ok or 0 fail.
        """
        check_authorization(sender, connection, self.__action)
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.modifygroup')

        group_entity = self.__libuser.lookupGroupByName(group_info['groupname'])
        group_entity.set(libuser.MEMBERNAME, group_info['members'])

        if group_info.has_key('new_groupname'):
            group_entity.set(libuser.GROUPNAME, group_info['new_groupname'])

        return dbus.Int32(self.__libuser.modifyGroup(group_entity))


    @dbus.service.method("org.mandrivalinux.mcc2.Users",
                         in_signature='a{sv}',
                         out_signature='i',
                         sender_keyword='sender',
                         connection_keyword='connection')
    def ModifyUser(self, user_info, sender, connection):
        """Modify User.
        
        @param user_info: A dbus.Dictionary with user information with
        the following content:
        
            * fullname: User full name
            * username: Yes, you guess!
            * shell: Shell to use, you can get a list of available
                    shells using ListUserShells.
        
        All shadow_* dictionaty keys is optional and only be used
        if present.
        
        Example:
        user_info = {
                'username': 'john'
                'new_username': 'johns',
                'fullname': 'Johns Does',
                'shell': '/bin/bash',
                'uid': 666,
                'gid': 666,
                'home_directory': '/home/john',
                'password': 'secret2',
                'shadow_expire': 'YYYY-MM-DD',
                'shadow_min': 0,
                'shadow_max', 99999,
                'shadow_warning': 7,
                'shadow_inactive': -1,
                'shadow_last_change': 'YYYY-MM-DD'
                }
        
        @raise dbus.DBusException:
            * org.mandrivalinux.mcc2.Users.Error.InvalidDate:
            * org.mandrivalinux.mcc2.Users.Error.YearIsTooBig:
        
        @rtype dbus.Int32: 1 ok or 0 fail.
        """
        check_authorization(sender, connection, self.__action)
        #check_authorization(sender, connection,
        #    'org.mandrivalinux.mcc2.users.modifyuser')

        user_entity = self.__libuser.lookupUserByName(user_info['username'])
        user_entity.set(libuser.GECOS, [user_info['fullname']])
        
        #TODO: Check if uid and gid can be converted to int()
        # if not raise an error
        user_entity.set(libuser.GIDNUMBER, [user_info['gid']])
        user_entity.set(libuser.UIDNUMBER, [user_info['uid']])
        user_entity.set(libuser.HOMEDIRECTORY, [user_info['home_directory']])
        user_entity.set(libuser.LOGINSHELL, [user_info['shell']])

        if user_info.has_key('new_username'):
            user_entity.set(libuser.USERNAME, [user_info['new_username']])

        if user_info.has_key('shadow_expire'):
            year = None
            month = None
            day = None

            try:
                (year, month, day) = user_info['shadow_expire'].split('-')
            except ValueError:
                msg = 'org.mandrivalinux.mcc2.Users.Error.InvalideDate'
                raise dbus.DBusException, msg

            try:
                tmp = time.mktime ([year, month, day, 0, 0, 0, 0, 0, -1])
            except OverflowError:
                msg = 'org.mandrivalinux.mcc2.Users.Error.YearIsTooBig'
                raise dbus.DBusException, msg

            seconds = 24 * 60 * 60
            days_expire = tmp / seconds
            fraction, integer = math.modf(days_expire)

            if fraction == 0.0:
                days_expire = integer
            else:
                days_expire = integer + 1

            user_entity.set(libuser.SHADOWEXPIRE, days_expire)

        if user_info.has_key('shadow_min'):
            user_entity.set(libuser.SHADOWMIN, int(user_info['shadow_min']))

        if user_info.has_key('shadow_max'):
            user_entity.set(libuser.SHADOWMAX, int(user_info['shadow_max']))

        if user_info.has_key('shadow_warning'):
            user_entity.set(
                libuser.SHADOWWARNING,
                int(user_info['shadow_warning']))

        if user_info.has_key('shadow_inactive'):
            user_entity.set(
                libuser.SHADOWINACTIVE,
                int(user_info['shadow_inactive']))

        #if user_info.has_key('shadow_last_change'):
        #    user_entity.set(
        #        libuser.SHADOWLASTCHANGE,
        #        int(user_info['shadow_last_change']))

        return self.__libuser.modifyUser(user_entity)


    def run(self):
        self._loop.run()


    @classmethod
    def main(cls):
        users = cls()
        try:
            users.run()
        except KeyboardInterrupt:
            pass