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
        print fullName
        
        userName = grid.findChild(QtDeclarative.QDeclarativeItem, 'addUserName').property('text')
        user_info['username'] = userName
        print userName

        password = grid.findChild(QtDeclarative.QDeclarativeItem, 'addPassword').property('text')
        confirmPassword = grid.findChild(QtDeclarative.QDeclarativeItem, 'addConfirmPassword').property('text')
        #TODO Find a way to show a message to gui from here
        if password == confirmPassword:
            user_info['password'] = password
        else:
            print "Password mismatch!"

        loginShell = grid.findChild(QtDeclarative.QDeclarativeItem, 'addLoginShell').property('text')
        user_info['shell'] = loginShell
        print loginShell

        createHomeDirectory = grid.findChild(QtDeclarative.QDeclarativeItem, 'addCreateHomeDirectory').property('checked')
        user_info['create_home'] = createHomeDirectory
        print createHomeDirectory

        homeDirectory = grid.findChild(QtDeclarative.QDeclarativeItem, 'addHomeDirectory').property('text')
        user_info['home_directory'] = homeDirectory
        print homeDirectory

        privateGroup = grid.findChild(QtDeclarative.QDeclarativeItem, 'addCreatePrivateGroup').property('checked')
        print privateGroup
        if privateGroup:
            print 'Creating a new group'
            gid = self.__interface.FirstUnusedGid()
            #TODO: Add exception handler here
            user_info['gid'] = int(self.__interface.AddGroup(user_info['username'], gid))

        # Get the FirstUnusedUid
        user_info['uid'] = self.__interface.FirstUnusedUid()

        specifyUserId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addSpecifyUserId').property('checked')
        print specifyUserId
        if specifyUserId:
            #TODO: Add exception handler here
            user_info['uid'] = int(grid.findChild(QtDeclarative.QDeclarativeItem, 'addUserId').property('text'))

        print user_info
        print self.__interface.AddUser(user_info)

    @QtCore.Slot(QtCore.QObject)
    def addGroup(self, grid):

        groupName = grid.findChild(QtDeclarative.QDeclarativeItem, 'addGroupName').property('text')
        print groupName

        # Get the FirstUnusedGid
        gid = self.__interface.FirstUnusedGid()

        specifyGroupId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addSpecifyGroupId').property('checked')
        print specifyGroupId
        if specifyGroupId:
            #TODO: Add exception handler here
            gid = int(grid.findChild(QtDeclarative.QDeclarativeItem, 'addGroupId').property('text'))

        print groupName, gid
        print self.__interface.AddGroup(groupName, gid)

    @QtCore.Slot()
    def quit(self):
        self.parent.quit()
