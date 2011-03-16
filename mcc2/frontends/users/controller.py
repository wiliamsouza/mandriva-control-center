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

        fullName = grid.findChild(QtDeclarative.QDeclarativeItem, 'addFullName')
        user_info['fullname'] = fullName.property('text')
        
        userName = grid.findChild(QtDeclarative.QDeclarativeItem, 'addUserName')
        user_info['username'] = userName.property('text')

        password = grid.findChild(QtDeclarative.QDeclarativeItem, 'addPassword')
        confirmPassword = grid.findChild(QtDeclarative.QDeclarativeItem, 'addConfirmPassword')
        #TODO Find a way to show a message to gui from here
        if password.property('text') == confirmPassword.property('text'):
            user_info['password'] = password.property('text')
        else:
            print "Password mismatch!"

        loginShell = grid.findChild(QtDeclarative.QDeclarativeItem, 'addLoginShell')
        user_info['shell'] = loginShell.property('text')

        createHomeDirectory = grid.findChild(QtDeclarative.QDeclarativeItem, 'addCreateHomeDirectory')
        user_info['create_home'] = createHomeDirectory.property('checked')

        homeDirectory = grid.findChild(QtDeclarative.QDeclarativeItem, 'addHomeDirectory')
        user_info['home_directory'] = homeDirectory.property('text')

        privateGroup = grid.findChild(QtDeclarative.QDeclarativeItem, 'addCreatePrivateGroup')
        if privateGroup.property('checked'):
            gid = self.__interface.FirstUnusedGid()
            #TODO: Add exception handler here
            user_info['gid'] = self.__interface.AddGroup(user_info['username'], gid)

        # Get the FirstUnusedUid
        user_info['uid'] = self.__interface.FirstUnusedUid()

        specifyUserId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addSpecifyUserId')
        addUserId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addUserId')
        if specifyUserId.property('checked'):
            #TODO: Add exception handler here
            user_info['uid'] = int(addUserId.property('text'))

        print user_info
        print self.__interface.AddUser(user_info)

        fullName.setProperty('text', '')
        userName.setProperty('text', '')
        password.setProperty('text', '')
        confirmPassword.setProperty('text', '')
        loginShell.setProperty('text', '/bin/bash')
        createHomeDirectory.setProperty('checked', True)
        homeDirectory.setProperty('text', '/home/')
        privateGroup.setProperty('checked', True)
        specifyUserId.setProperty('checked', False)
        addUserId.setProperty('text', '')

    @QtCore.Slot(QtCore.QObject)
    def addGroup(self, grid):

        groupName = grid.findChild(QtDeclarative.QDeclarativeItem, 'addGroupName')

        # Get the FirstUnusedGid
        gid = self.__interface.FirstUnusedGid()

        specifyGroupId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addSpecifyGroupId')
        addGroupId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addGroupId')
        if specifyGroupId.property('checked'):
            #TODO: Add exception handler here
            gid = int(addGroupId.property('text'))

        #print groupName, gid
        self.__interface.AddGroup(groupName.property('text'), gid)

        groupName.setProperty('text', '')
        specifyGroupId.setProperty('checked', False)
        addGroupId.setProperty('text', '')
        self.parent.groupModel.refresh()

    @QtCore.Slot(QtCore.QObject)
    def reflesh(self, groupModel):
        print 'refreshing'
        groupModel.refresh()

    @QtCore.Slot()
    def quit(self):
        self.parent.quit()
