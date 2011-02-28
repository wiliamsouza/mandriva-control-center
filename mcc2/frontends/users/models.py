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
        
    def _username(self):
        return str(self.__userDetails['username'])

    def _fullname(self):
        return str(self.__userDetails['fullname'])

    def _home_directory(self):
        return str(self.__userDetails['home_directory'])

    def _login_shell(self):
        return str(self.__userDetails['login_shell'])

    changed = QtCore.Signal()

    username = QtCore.Property(unicode, _username, notify=changed)
    fullname = QtCore.Property(unicode, _fullname, notify=changed)
    home_directory = QtCore.Property(unicode, _home_directory, notify=changed)
    login_shell = QtCore.Property(unicode, _login_shell, notify=changed)


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