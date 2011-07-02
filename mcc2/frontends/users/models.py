import time
import math

import dbus
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
#import dbus.mainloop.qt
#dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)

#from PySide import QtCore
from PyQt4 import QtCore

bus = dbus.SystemBus()
proxy = bus.get_object('org.mandrivalinux.mcc2.Users',
                       '/org/mandrivalinux/mcc2/Users')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')


class UserModel(QtCore.QAbstractListModel):

    COLUMNS = ('user',)

    def __init__(self, parent):
        QtCore.QAbstractListModel.__init__(self, parent=parent)
        self.__users = []
        self.setRoleNames(dict(enumerate(UserModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__users)

    def data(self, index, role):
        if index.isValid() and role == UserModel.COLUMNS.index('user'):
            return self.__users[index.row()]
        return None

    def add(self, userDetails):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__users), len(self.__users))
        #TODO: Add dbus exception handler here
        interface.AddUser(userDetails)
        user = User(userDetails['userName'], self)
        self.__users.append(user)
        self.endInsertRows()

    def modify(self, modifyUserDetails, groups, row):
        user = self.__users[row]
        user.fullName = modifyUserDetails['fullName']
        user.userName = modifyUserDetails['userName']
	user.userPhoto = modifyUserDetails['userPhoto']
        user.password = modifyUserDetails['password']
        user.loginShell = modifyUserDetails['loginShell']
        user.homeDirectory = modifyUserDetails['homeDirectory']
	if modifyUserDetails.has_key('expirationDate'):
            user.expirationDate = modifyUserDetails['expirationDate']
        user.shadowMin = modifyUserDetails['shadowMin']
        user.shadowMax = modifyUserDetails['shadowMax']
        user.shadowWarning = modifyUserDetails['shadowWarning'] 
        user.shadowInactive = modifyUserDetails['shadowInactive']
        user.save(groups)

    def lock(self, row):
        user = self.__users[row]
        user.lock()

    def unLock(self, row):
        user = self.__users[row]
        user.unLock()

    def delete(self, userName, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        #TODO: Add dbus exception handler here
        interface.DeleteUser(userName)
        self.__users.pop(row)
        self.endRemoveRows()

    def populate(self):
        for user in interface.ListUsers():
            self.__users.append(User(user, self))


class User(QtCore.QObject):

    def __init__(self, user, parent):
        QtCore.QObject.__init__(self, parent=parent)
        self.__user = user
        self.__modifyUserDetails = {}
        self.__userDetails = {}
        self.__isLocked = False
        self.__expirationDate = ''
        self.__shadowExpire = False
        self.update()

    def __uid(self):
        return str(self.__userDetails['uid'])

    def __gid(self):
        return str(self.__userDetails['gid'])

    #TODO: make a setGid method to change the primary group from the user

    def __getUserName(self):
        return str(self.__userDetails['userName'])

    def __setUserName(self, newUserName):
        self.__modifyUserDetails['newUserName'] = newUserName

    def __getFullName(self):
        return self.__userDetails['fullName']

    def __setFullName(self, fullName):
        self.__modifyUserDetails['fullName'] = fullName

    def __getUserPhoto(self):
        return self.__userDetails['userPhoto']

    def __setUserPhoto(self, photo):
        print '__setUserPhoto'
        self.__modifyUserDetails['userPhoto'] = photo
	self.changed.emit()


    def __getHomeDirectory(self):
        return self.__userDetails['homeDirectory']

    def __setHomeDirectory(self, homeDirectory):
        self.__modifyUserDetails['homeDirectory'] = homeDirectory

    def __getLoginShell(self):
        return self.__userDetails['loginShell']

    def __setLoginShell(self, loginShell):
        self.__modifyUserDetails['loginShell'] = loginShell

    def __getShadowExpire(self):
        return self.__shadowExpire

    def __setShadowExpire(self, shadowExpire):
        self.__shadowExpire = shadowExpire

    def __getExpirationDate(self):
        return str(self.__expirationDate)

    def __setExpirationDate(self, expirationDate):
        # TODO: convert date to epoc
        year = None
        month = None
        day = None
        (year, month, day) = expirationDate.split('-')
        try:
            tmp = time.mktime([int(year), int(month), int(day), 0, 0, 0, 0, 0, -1])
        except OverflowError:
            #TODO: Show this error to user
            print 'The year is out of range.  Please select a different year'
        seconds = 24 * 60 * 60
        days_expire = tmp / seconds
        fraction, integer = math.modf(days_expire)
        if fraction == 0.0:
            days_expire = integer
        else:
            days_expire = integer + 1
        self.__shadowExpire = True
        self.__expirationDate = days_expire
        self.__modifyUserDetails['shadowExpire'] = days_expire

    def __getShadowMin(self):
        return str(self.__userDetails['shadowMin'])

    def __setShadowMin(self, shadowMin):
        self.__modifyUserDetails['shadowMin'] = shadowMin

    def __getShadowMax(self):
        return str(self.__userDetails['shadowMax'])

    def __setShadowMax(self, shadowMax):
        self.__modifyUserDetails['shadowMax'] = shadowMax

    def __getShadowWarning(self):
        return str(self.__userDetails['shadowWarning'])

    def __setShadowWarning(self, shadowWarning):
        self.__modifyUserDetails['shadowWarning'] = shadowWarning

    def __getShadowInactive(self):
        return str(self.__userDetails['shadowInactive'])

    def __setShadowInactive(self, shadowInactive):
        self.__modifyUserDetails['shadowInactive'] = shadowInactive

    def __getShadowLastChange(self):
        days = int(self.__userDetails['shadowLastChange'])
        tmp = days * int(24 * 60 * 60)
        age = time.localtime(tmp)
        return time.strftime('%a, %d %b %Y', age)

    def __getGroups(self):
        return self.__userDetails['groups']

    def __isLocked(self):
        if interface.UserIsLocked(self.__user):
            self.__isLocked = True
        return self.__isLocked

    def setPassword(self, password):
        self.__modifyUserDetails['password'] = password

    def lock(self):
        interface.LockUser(self.__user)
        self.__isLocked = True
        self.changed.emit()

    def unLock(self):
        interface.UnLockUser(self.__user)
        self.__isLocked = False
        self.changed.emit()

    def save(self, groups):
        self.__modifyUserDetails['oldUserName'] = self.__user
	self.__modifyUserDetails['groups'] = groups
        interface.ModifyUser(self.__modifyUserDetails)
        try:
            self.__user = self.__modifyUserDetails['newUserName']
        except KeyError:
            self.__user = self.__modifyUserDetails['oldUserName']
        self.update()

    def update(self):
        self.__userDetails = interface.UserDetails(self.__user)
        if self.__userDetails['shadowExpire'] > 0:
            self.__shadowExpire = True
            days = int(self.__userDetails['shadowExpire'])
            tmp = days * int(24 * 60 * 60)
            age = time.localtime(tmp)
            self.__expirationDate = time.strftime('%Y-%m-%d', age)
        self.changed.emit()

    #changed = QtCore.Signal()
    changed = QtCore.pyqtSignal()

    """
    uid = QtCore.Property(unicode, __uid, notify=changed)
    gid = QtCore.Property(unicode, __gid, notify=changed)
    userName = QtCore.Property(unicode, __getUserName, __setUserName, notify=changed)
    fullName = QtCore.Property(unicode, __getFullName, __setFullName, notify=changed)
    homeDirectory = QtCore.Property(unicode, __getHomeDirectory, __setHomeDirectory, notify=changed)
    loginShell = QtCore.Property(unicode, __getLoginShell, __setLoginShell, notify=changed)
    shadowExpire = QtCore.Property(bool, __getShadowExpire, __setShadowExpire, notify=changed)
    expirationDate = QtCore.Property(unicode, __getExpirationDate, __setExpirationDate, notify=changed)
    shadowMin = QtCore.Property(unicode, __getShadowMin, __setShadowMin, notify=changed)
    shadowMax = QtCore.Property(unicode, __getShadowMax, __setShadowMax, notify=changed)
    shadowWarning = QtCore.Property(unicode, __getShadowWarning, __setShadowWarning, notify=changed)
    shadowInactive = QtCore.Property(unicode, __getShadowInactive, __setShadowInactive, notify=changed)
    shadowLastChange = QtCore.Property(unicode, __getShadowLastChange, notify=changed)
    groups = QtCore.Property(list, __getGroups, notify=changed)
    isLocked = QtCore.Property(bool, __isLocked, notify=changed)
    """

    uid = QtCore.pyqtProperty(unicode, __uid, notify=changed)
    gid = QtCore.pyqtProperty(unicode, __gid, notify=changed)
    userName = QtCore.pyqtProperty(unicode, __getUserName, __setUserName, notify=changed)
    fullName = QtCore.pyqtProperty(unicode, __getFullName, __setFullName, notify=changed)
    userPhoto = QtCore.pyqtProperty(unicode, __getUserPhoto, __setUserPhoto, notify=changed)
    homeDirectory = QtCore.pyqtProperty(unicode, __getHomeDirectory, __setHomeDirectory, notify=changed)
    loginShell = QtCore.pyqtProperty(unicode, __getLoginShell, __setLoginShell, notify=changed)
    shadowExpire = QtCore.pyqtProperty(bool, __getShadowExpire, __setShadowExpire, notify=changed)
    expirationDate = QtCore.pyqtProperty(unicode, __getExpirationDate, __setExpirationDate, notify=changed)
    shadowMin = QtCore.pyqtProperty(unicode, __getShadowMin, __setShadowMin, notify=changed)
    shadowMax = QtCore.pyqtProperty(unicode, __getShadowMax, __setShadowMax, notify=changed)
    shadowWarning = QtCore.pyqtProperty(unicode, __getShadowWarning, __setShadowWarning, notify=changed)
    shadowInactive = QtCore.pyqtProperty(unicode, __getShadowInactive, __setShadowInactive, notify=changed)
    shadowLastChange = QtCore.pyqtProperty(unicode, __getShadowLastChange, notify=changed)
    groups = QtCore.pyqtProperty(list, __getGroups, notify=changed)
    isLocked = QtCore.pyqtProperty(bool, __isLocked, notify=changed)

class SystemUserModel(QtCore.QAbstractListModel):

    COLUMNS = ('user',)

    def __init__(self, parent):
        QtCore.QAbstractListModel.__init__(self, parent=parent)
        self.__users = []
        self.setRoleNames(dict(enumerate(SystemUserModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__users)

    def data(self, index, role):
        if index.isValid() and role == SystemUserModel.COLUMNS.index('user'):
            return self.__users[index.row()]
        return None

    def checked(self):
        return [user for user in self.__users if user.isChecked]

    #@QtCore.Slot(list)
    @QtCore.pyqtSlot(list)
    def selectUsers(self, members):
        for user in self.__users:
            user.unCheck()
            if user.userName in members:
                user.toggleChecked()

    def populate(self):
        for user in interface.ListAllUsers():
            self.__users.append(SystemUser(user, self))


class SystemUser(QtCore.QObject):

    def __init__(self, user, parent):
        QtCore.QObject.__init__(self, parent=parent)

        self.__user = user
        self.__checked = False

    def __getUserName(self):
        return self.__user

    def __isChecked(self):
        return self.__checked

    def unCheck(self):
        self.__checked = False
        self.changed.emit()

    def toggleChecked(self):
        self.__checked = not self.__checked
        self.changed.emit()

    #changed = QtCore.Signal()
    changed = QtCore.pyqtSignal()

    """
    userName = QtCore.Property(unicode, __getUserName, notify=changed)
    isChecked = QtCore.Property(bool, __isChecked, notify=changed)
    """

    userName = QtCore.pyqtProperty(unicode, __getUserName, notify=changed)
    isChecked = QtCore.pyqtProperty(bool, __isChecked, notify=changed)

class GroupModel(QtCore.QAbstractListModel):

    COLUMNS = ('group',)

    def __init__(self, parent):
        QtCore.QAbstractListModel.__init__(self, parent=parent)
        self.__groups = []
        self.setRoleNames(dict(enumerate(GroupModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__groups)

    def data(self, index, role):
        if index.isValid() and role == GroupModel.COLUMNS.index('group'):
            return self.__groups[index.row()]
        return None

    def add(self, groupName, gid):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__groups), len(self.__groups))
        #TODO: Add dbus exception handler here
        # dbus.exceptions.DBusException: org.mandrivalinux.mcc2.Users.Error.GroupAlreadyExist
        groupId = interface.AddGroup(groupName, gid)
        group = Group(groupName, self)
        self.__groups.append(group)
        self.endInsertRows()
        return groupId

    def modify(self, groupName, members, row):
        group = self.__groups[row]
        group.groupName = groupName
        # This is a workaround because dbus won't support send a empty list
        if not members:
            members = ['']
        group.members = members
        group.save()

    def delete(self, groupName, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        #TODO: Add dbus exception handler here
        interface.DeleteGroup(groupName)
        self.__groups.pop(row)
        self.endRemoveRows()

    def populate(self, system=False):
        for group in interface.ListGroups():
            self.__groups.append(Group(group, self))


class Group(QtCore.QObject):
    """ QObject wrapper to dbus/libuser group representation """

    def __init__(self, group, parent):
        QtCore.QObject.__init__(self, parent=parent)

        self.__group = group
        self.__modifyGroupDetails = {}
        self.__groupDetails = {}
        self.update()

    def __gid(self):
        return str(self.__groupDetails['gid'])

    def __getGroupName(self):
        return self.__groupDetails['groupName']

    def __setGroupName(self, newGroupName):
        if self.__group != newGroupName:
            self.__modifyGroupDetails['newGroupName'] = newGroupName

    def __getMembers(self):
        return self.__groupDetails['members']

    def __setMembers(self, members):
        self.__modifyGroupDetails['members'] = members

    def __getStrMembers(self):
        return ', '.join(self.__groupDetails['members'])

    def save(self):
        self.__modifyGroupDetails['oldGroupName'] = self.__group
        interface.ModifyGroup(self.__modifyGroupDetails)
        try:
            self.__group = self.__modifyGroupDetails['newGroupName']
        except KeyError:
            self.__group = self.__modifyGroupDetails['oldGroupName']
        self.update()

    def update(self):
        """
        new_dict = {}
        result = interface.GroupDetails(self.__group)
        for key, value in result.items():
            if key == 'members':
                new_list = []
                for list_value in value:
                    new_list.append(str(list_value))
                new_dict[str(key)] = new_list
                break
            new_dict[str(key)] = str(value)
        self.__groupDetails = new_dict
        """
        #TODO: Add dbus exception handler here
        self.__groupDetails = interface.GroupDetails(self.__group)
        self.changed.emit()

    #changed = QtCore.Signal()
    changed = QtCore.pyqtSignal()

    """
    groupName = QtCore.Property(unicode, __getGroupName, __setGroupName,
                                notify=changed)
    gid = QtCore.Property(unicode, __gid, notify=changed)
    members = QtCore.Property(list, __getMembers, __setMembers, notify=changed)
    strMembers = QtCore.Property(unicode, __getStrMembers, notify=changed)
    """

    groupName = QtCore.pyqtProperty(unicode, __getGroupName, __setGroupName,
                                notify=changed)
    gid = QtCore.pyqtProperty(unicode, __gid, notify=changed)
    members = QtCore.pyqtProperty(list, __getMembers, __setMembers, notify=changed)
    strMembers = QtCore.pyqtProperty(unicode, __getStrMembers, notify=changed)

class SystemGroupModel(QtCore.QAbstractListModel):

    COLUMNS = ('group',)

    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent=parent)
        self.__groups = []
        self.setRoleNames(dict(enumerate(SystemGroupModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__groups)

    def data(self, index, role):
        if index.isValid() and role == SystemGroupModel.COLUMNS.index('group'):
            return self.__groups[index.row()]
        return None

    def checked(self):
        return [group for group in self.__groups if group.isChecked]

    #@QtCore.Slot(list)
    @QtCore.pyqtSlot(list)
    def selectGroups(self, groups):
        for group in self.__groups:
            group.unCheck()
            if group.groupName in groups:
                group.toggleChecked()

    def populate(self, system=False):
        for group in interface.ListAllGroups():
            self.__groups.append(SystemGroup(group, self))

class SystemGroup(QtCore.QObject):

    def __init__(self, group, parent):
        QtCore.QObject.__init__(self, parent=parent)

        self.__group = group
        self.__checked = False

    def __getGroupName(self):
        return self.__group

    def __isChecked(self):
        return self.__checked

    def unCheck(self):
        self.__checked = False
        self.changed.emit()

    def toggleChecked(self):
        self.__checked = not self.__checked
        self.changed.emit()

    #changed = QtCore.Signal()
    changed = QtCore.pyqtSignal()

    """
    groupName = QtCore.Property(unicode, __getGroupName, notify=changed)
    isChecked = QtCore.Property(bool, __isChecked, notify=changed)
    """

    groupName = QtCore.pyqtProperty(unicode, __getGroupName, notify=changed)
    isChecked = QtCore.pyqtProperty(bool, __isChecked, notify=changed)


class ShellModel(QtCore.QAbstractListModel):

    COLUMNS = ('shell',)

    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent=parent)
        self.__shells = []
        self.setRoleNames(dict(enumerate(ShellModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__shells)

    def data(self, index, role):
        if index.isValid() and role == ShellModel.COLUMNS.index('shell'):
            return self.__shells[index.row()]
        return None

    def populate(self):
        for shell in interface.ListUserShells():
            self.__shells.append(Shell(shell, self))


class Shell(QtCore.QObject):

    def __init__(self, shell, parent):
        QtCore.QObject.__init__(self, parent=parent)

        self.__shell = shell

    def __getShellName(self):
        return self.__group

    changed = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(unicode, __getShellName, notify=changed)
