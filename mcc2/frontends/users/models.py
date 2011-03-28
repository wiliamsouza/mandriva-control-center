import dbus

from PySide import QtCore


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
        return self.__shadow_expire

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

    def _groups(self):
        return self.__groups

    def _islocked(self):
        return self.__islocked

    changed = QtCore.Signal()

    uid = QtCore.Property(unicode, _uid, notify=changed)
    username = QtCore.Property(unicode, _username, notify=changed)
    fullname = QtCore.Property(unicode, _fullname, notify=changed)
    home_directory = QtCore.Property(unicode, _home_directory, notify=changed)
    login_shell = QtCore.Property(unicode, _login_shell, notify=changed)
    shadow_expire = QtCore.Property(bool, _shadow_expire, notify=changed)
    expiration_date = QtCore.Property(unicode, _expiration_date, notify=changed)
    shadow_min = QtCore.Property(unicode, _shadow_min, notify=changed)
    shadow_max = QtCore.Property(unicode, _shadow_max, notify=changed)
    shadow_warning = QtCore.Property(unicode, _shadow_warning, notify=changed)
    shadow_inactive = QtCore.Property(unicode, _shadow_inactive, notify=changed)
    shadow_last_change = QtCore.Property(unicode, _shadow_last_change, notify=changed)
    groups = QtCore.Property(list, _groups, notify=changed)
    islocked = QtCore.Property(bool ,_islocked, notify=changed)


class UserModel(QtCore.QAbstractListModel):
    COLUMNS = ('user',)

    def __init__(self, users):
        QtCore.QAbstractListModel.__init__(self)
        self.setObjectName('user')
        self._users = users
        self._users.sort()
        self.setRoleNames(dict(enumerate(UserModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._users)

    #def flags(self, index):
    #    return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
        if index.isValid() and role == UserModel.COLUMNS.index('user'):
            return self._users[index.row()]
        return None

    def removeRows(self, row, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        self._users.pop(row)
        self.endRemoveRows()

    def addUser(self, username):
        self.beginInsertRows(QtCore.QModelIndex(), len(self._users), len(self._users))
        self._users.append(User(username))
        self.endInsertRows()


class UserAll(QtCore.QObject):

    def __init__(self, username):
        QtCore.QObject.__init__(self)
        self.__username = username
        self.__ischecked = False

    def _username(self):
        return str(self.__username )

    def _ischecked(self):
        return self.__ischecked

    def uncheck(self):
        self.__ischecked = False
        self.changed.emit()

    def _toggle_checked(self):
        self.__ischecked = not self.__ischecked
        self.changed.emit()

    changed = QtCore.Signal()

    username = QtCore.Property(unicode, _username, notify=changed)
    ischecked = QtCore.Property(bool, _ischecked, notify=changed)


class UserAllModel(QtCore.QAbstractListModel):
    COLUMNS = ('user',)

    def __init__(self, users):
        QtCore.QAbstractListModel.__init__(self)
        self._users = users
        self._users.sort()
        self.setRoleNames(dict(enumerate(UserAllModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._users)

    def data(self, index, role):
        if index.isValid() and role == UserAllModel.COLUMNS.index('user'):
            return self._users[index.row()]
        return None

    def checked(self):
        return [user for user in self._users if user.ischecked]

    def selectMembers(self, members):
        for user in self._users:
            user.uncheck()
            if user.username in members:
                user._toggle_checked()

"""
class Group(QtCore.QObject):

    def __init__(self, group):
        QtCore.QObject.__init__(self)
        self._bus = dbus.SystemBus()
        self._proxy = self._bus.get_object(
            'org.mandrivalinux.mcc2.Users',
            '/org/mandrivalinux/mcc2/Users')
        self._interface = dbus.Interface(
            self._proxy,
            'org.mandrivalinux.mcc2.Users')

        self._groupDetails = self._interface.GroupDetails(group)
        self.__islocked = self._interface.GroupIsLocked(group)
        # Merge group members
        #self.__groupDetails['members'].append = self.__interface.ListUsersByGroup(group)

    def _gid(self):
        return str(self._groupDetails['gid'])

    def _groupname(self):
        return str(self._groupDetails['groupName'])

    def _members(self):
        return self._groupDetails['members']

    def _islocked(self):
        return self.__islocked

    def _reflesh(self):
        self.changed.emit()

    changed = QtCore.Signal()

    gid = QtCore.Property(unicode, _gid, notify=changed)
    groupname = QtCore.Property(unicode, _groupname, notify=changed)
    members = QtCore.Property(list, _members, notify=changed)
    islocked = QtCore.Property(unicode ,_islocked, notify=changed)
"""


class Group(QtCore.QObject):

    def __init__(self, group):
        QtCore.QObject.__init__(self)

        self.__group = group

        self.__bus = dbus.SystemBus()

        self.__proxy = self.__bus.get_object(
            'org.mandrivalinux.mcc2.Users',
            '/org/mandrivalinux/mcc2/Users')

        self.__interface = dbus.Interface(
            self.__proxy,
            'org.mandrivalinux.mcc2.Users')

        self.__modifyGroupDetails = {}
        self.update()

    def __gid(self):
        return str(self.__groupDetails['gid'])

    def __getGroupName(self):
        return str(self.__groupDetails['groupName'])

    def __setGroupName(self, newGroupName):
        self.__modifyGroupDetails['newGroupName'] = newGroupName

    def __getMembers(self):
        return self.__groupDetails['members']

    def __setMembers(self, members):
        self._modifyGroupDetails['members'] = members

    def save(self):
        self.__modifyGroupDetails['oldGroupName'] = self.__group
        self.__interface.ModifyGroup(self.__modifyGroupDetails)
        self.__group = self.__modifyGroupDetails['newGroupName']
        self.update()

    def update(self):
        self.__groupDetails = self.__interface.GroupDetails(self.__group)
        self.changed.emit()

    changed = QtCore.Signal()

    gid = QtCore.Property(unicode, __gid, notify=changed)
    groupname = QtCore.Property(unicode, __getGroupName, __setGroupName,
                                notify=changed)
    members = QtCore.Property(list, __getMembers, __setMembers, notify=changed)


class GroupListModel(QtCore.QAbstractListModel):

    COLUMNS = ('group',)

    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        self.__groups = []
        self.setRoleNames(dict(enumerate(GroupListModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__groups)

    def data(self, index, role):
        if index.isValid() and role == GroupListModel.COLUMNS.index('group'):
            return self.__groups[index.row()]
        return None

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        #self.beginRemoveRows(parent, row, row)
        self.__groups.pop(row)
        #self.endRemoveRows()

    def addGroup(self, groupname):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__groups), len(self.__groups))
        self.__groups.append(Group(groupname))
        self.endInsertRows()

    def populate(self):
        bus = dbus.SystemBus()
        proxy = bus.get_object(
            'org.mandrivalinux.mcc2.Users',
            '/org/mandrivalinux/mcc2/Users')
        interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')

        for group in interface.ListGroups():
            self.__groups.append(Group(group))


"""
class GroupModel(QtCore.QAbstractListModel):
    COLUMNS = ('group',)

    def __init__(self, groups):
        QtCore.QAbstractListModel.__init__(self)
        self._groups = groups
        self._groups.sort()
        self.setRoleNames(dict(enumerate(GroupModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._groups)

    #def flags(self, index):
    #    return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
        if index.isValid() and role == GroupModel.COLUMNS.index('group'):
            return self._groups[index.row()]
        return None

    def removeRows(self, row, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        self._groups.pop(row)
        self.endRemoveRows()

    def addGroup(self, groupname):
        self.beginInsertRows(QtCore.QModelIndex(), len(self._groups), len(self._groups))
        self._groups.append(Group(groupname))
        self.endInsertRows()

    def reflesh(self):
        for group in self._groups:
            group._reflesh()
"""

class GroupAll(QtCore.QObject):

    def __init__(self, groupname):
        QtCore.QObject.__init__(self)
        self.__groupname = groupname
        self.__ischecked = False

    def _groupname(self):
        return str(self.__groupname )

    def _ischecked(self):
        return self.__ischecked

    def uncheck(self):
        self.__ischecked = False
        self.changed.emit()

    def _toggle_checked(self):
        self.__ischecked = not self.__ischecked
        self.changed.emit()

    changed = QtCore.Signal()

    groupname = QtCore.Property(unicode, _groupname, notify=changed)
    ischecked = QtCore.Property(bool, _ischecked, notify=changed)


class GroupAllModel(QtCore.QAbstractListModel):
    COLUMNS = ('group',)

    def __init__(self, groups):
        QtCore.QAbstractListModel.__init__(self)
        self._groups = groups
        self._groups.sort()
        self.setRoleNames(dict(enumerate(GroupAllModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._groups)

    def data(self, index, role):
        if index.isValid() and role == GroupAllModel.COLUMNS.index('group'):
            return self._groups[index.row()]
        return None

    def checked(self):
        return [group for group in self._groups if group.ischecked]

    def selectMembers(self, members):
        for group in self._groups:
            group.uncheck()
            if group.groupname in members:
                group._toggle_checked()