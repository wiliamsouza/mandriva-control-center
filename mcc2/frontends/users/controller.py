from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative

import dbus

class Controller(QtCore.QObject):

    def __init__(self, parent):
        QtCore.QObject.__init__(self)
        self.parent = parent

        self.__bus = dbus.SystemBus()
        self.__proxy = self.__bus.get_object(
            'org.mandrivalinux.mcc2.Users',
            '/org/mandrivalinux/mcc2/Users')
        self.__interface = dbus.Interface(
            self.__proxy,
            'org.mandrivalinux.mcc2.Users')

    @QtCore.Slot(QtCore.QObject)
    def addUser(self, grid):
        user_info = {}
        fullName = grid.findChild(QtDeclarative.QDeclarativeItem, 'addFullName').property('text')
        user_info['fullname'] = fullName
        userName = grid.findChild(QtDeclarative.QDeclarativeItem, 'addUserName').property('text')
        user_info['username'] = userName
        password = grid.findChild(QtDeclarative.QDeclarativeItem, 'addPassword').property('text')
        confirmPassword = grid.findChild(QtDeclarative.QDeclarativeItem, 'addConfirmPassword').property('text')

        #TODO Find a way to show a message to gui from here
        if password == confirmPassword:
            user_info['password'] = password
        else:
            pass

        loginShell = grid.findChild(QtDeclarative.QDeclarativeItem, 'addLoginShell').property('text')
        user_info['shell'] = loginShell

        # TODO: Turn this in a checkbox component
        createHomeDirectory = grid.findChild(QtDeclarative.QDeclarativeItem, 'addCreateHomeDirectory').property('checked')
        print createHomeDirectory
        #if createHomeDirectory is True:
        #    user_info['create_home'] = True
        #else:
        #    user_info['create_home'] = False

        homeDirectory = grid.findChild(QtDeclarative.QDeclarativeItem, 'addHomeDirectory').property('text')
        user_info['home_directory'] = homeDirectory

        # TODO: Turn this in a checkbox component
        privateGroup = grid.findChild(QtDeclarative.QDeclarativeItem, 'addCreatePrivateGroup').property('checked')
        print privateGroup

        # TODO: Turn this in a checkbox component
        specifyUserId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addSpecifyUserId').property('checked')
        print specifyUserId

        userId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addUserId')

        # Get the FirstUnusedUid
        uid = self.__interface.FirstUnusedUid()

        # Create a group with the same name of the user automaticaly
        #if privateGroup is True
        #    gid = self.__interface.FirstUnusedGid()
        """
        user_info = {
            'fullname': fullName.property('text'),
            'username': userName.property('text'),
            'shell': loginShell.property('text'),
            'uid': uid,
            'gid': gid,
            'create_home': True,
            'home_directory': '/home/john',
            'password': 'secret'
            }
        """
    @QtCore.Slot()
    def quit(self):
        self.parent.quit()
