from PySide import QtCore

import dbus

class User(QtCore.QObject):
    def __init__(self, user):
        QtCore.QObject.__init__(self)
        self.__bus = dbus.SystemBus()
        self.__proxy = self.__bus.get_object(
            'org.mandrivalinux.mcc2.Users',
            '/org/mandrivalinux/mcc2/Users')
        self.__interface = dbus.Interface(
            self.__proxy,
            'org.mandrivalinux.mcc2.Users')

        self.__userDetails = self.__interface.UserDetails(user)
        self.__groups = self.__interface.ListGroupsByUser(user)
        
        #TODO: move this logic to users backend and return a dbus.Boolean
        self.__islocked = False
        if self.__interface.UserIsLocked(user):
            self.__islocked = True

	self.__expiration_date = ''
        self.__shadow_expire = False
        if self.__userDetails['shadow_expire'] > 0:
            self.__shadow_expire = True
            self.__expiration_date = self.__userDetails['shadow_expire']

    def _uid(self):
        return str(self.__userDetails['uid'])

    def _username(self):
        return str(self.__userDetails['username'])

    def _fullname(self):
        return str(self.__userDetails['fullname'])

    def _home_directory(self):
        return str(self.__userDetails['home_directory'])

    def _login_shell(self):
        return str(self.__userDetails['login_shell'])

    def _shadow_expire(self):
        return self.__userDetails['shadow_expire']

    def _expiration_date(self):
            return str(self.__expiration_date)

    def _shadow_min(self):
        return str(self.__userDetails['shadow_min'])

    def _shadow_max(self):
        return str(self.__userDetails['shadow_max'])

    def _shadow_warning(self):
        return str(self.__userDetails['shadow_warning'])

    def _shadow_inactive(self):
        return str(self.__userDetails['shadow_inactive'])

    def _shadow_last_change(self):
        return str(self.__userDetails['shadow_last_change'])

    #def _groups(self):
    #    return self.__groups

    def _islocked(self):
        return self.__islocked

    changed = QtCore.Signal()

    uid = QtCore.Property(unicode, _uid, notify=changed)
    username = QtCore.Property(unicode, _username, notify=changed)
    fullname = QtCore.Property(unicode, _fullname, notify=changed)
    home_directory = QtCore.Property(unicode, _home_directory, notify=changed)
    login_shell = QtCore.Property(unicode, _login_shell, notify=changed)
    shadow_expire = QtCore.Property(unicode, _shadow_expire, notify=changed)
    expiration_date = QtCore.Property(unicode, _expiration_date, notify=changed)
    shadow_min = QtCore.Property(unicode, _shadow_min, notify=changed)
    shadow_max = QtCore.Property(unicode, _shadow_max, notify=changed)
    shadow_warning = QtCore.Property(unicode, _shadow_warning, notify=changed)
    shadow_inactive = QtCore.Property(unicode, _shadow_inactive, notify=changed)
    shadow_last_change = QtCore.Property(unicode, _shadow_last_change, notify=changed)
    #groups = QtCore.Property(_groups, notify=changed)
    islocked = QtCore.Property(bool ,_islocked, notify=changed)


class UserModel(QtCore.QAbstractListModel):
    COLUMNS = ('user',)

    def __init__(self, user):
        QtCore.QAbstractListModel.__init__(self)
        self._user = user
        self.setRoleNames(dict(enumerate(UserModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._user)

    def data(self, index, role):
        if index.isValid() and role == UserModel.COLUMNS.index('user'):
            return self._user[index.row()]
        return None


class Group(QtCore.QObject):
    def __init__(self, group):
        QtCore.QObject.__init__(self)
        self.__bus = dbus.SystemBus()
        self.__proxy = self.__bus.get_object(
            'org.mandrivalinux.mcc2.Users',
            '/org/mandrivalinux/mcc2/Users')
        self.__interface = dbus.Interface(
            self.__proxy,
            'org.mandrivalinux.mcc2.Users')

        self.__groupDetails = self.__interface.GroupDetails(group)
        # Merge group members
        #self.__groupDetails['members'].append = self.__interface.ListUsersByGroup(group)
        self.__islocked = self.__interface.GroupIsLocked(group)

    def _gid(self):
        return str(self.__groupDetails['gid'])

    def _groupname(self):
        return str(self.__groupDetails['groupname'])

    #TODO: How to use list with QtCore.Property
    #def _members(self):
    #    return str(self.__groupDetails['members'])

    def _islocked(self):
        return str(self.__islocked)

    changed = QtCore.Signal()

    gid = QtCore.Property(unicode, _gid, notify=changed)
    groupname = QtCore.Property(unicode, _groupname, notify=changed)
    #members = QtCore.Property(_members, notify=changed)
    islocked = QtCore.Property(unicode ,_islocked, notify=changed)


class GroupModel(QtCore.QAbstractListModel):
    COLUMNS = ('group',)

    def __init__(self, group):
        QtCore.QAbstractListModel.__init__(self)
        self._group = group
        self.setRoleNames(dict(enumerate(GroupModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._group)

    def data(self, index, role):
        if index.isValid() and role == GroupModel.COLUMNS.index('group'):
            return self._group[index.row()]
        return None
