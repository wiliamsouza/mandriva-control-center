import dbus

from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative


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
        fullname = fullName.property('text')
        # libuser won't respect that always the fullname will be set by username
        # if a fullname was not set.
        if fullname != "":
            user_info['fullname'] = fullname
        
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
            self.parent.groupModel.addGroup(user_info['username'])

        user_info['uid'] = self.__interface.FirstUnusedUid()
        specifyUserId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addSpecifyUserId')
        addUserId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addUserId')
        if specifyUserId.property('checked'):
            #TODO: Add exception handler here
            user_info['uid'] = int(addUserId.property('text'))

        self.__interface.AddUser(user_info)
        self.parent.userModel.addUser(userName.property('text'))
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
        specifyGroupId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addSpecifyGroupId')
        addGroupId = grid.findChild(QtDeclarative.QDeclarativeItem, 'addGroupId')
        gid = self.__interface.FirstUnusedGid()
        if specifyGroupId.property('checked'):
            #TODO: Add exception handler here
            gid = int(addGroupId.property('text'))

        self.__interface.AddGroup(groupName.property('text'), gid)
        self.parent.groupListModel.addGroup(groupName.property('text'))
        groupName.setProperty('text', '')
        specifyGroupId.setProperty('checked', False)
        addGroupId.setProperty('text', '')

    @QtCore.Slot(QtCore.QObject)
    def ModifyGroup(self, grid):
        group_info = {}
        groupName = grid.findChild(QtDeclarative.QDeclarativeItem, 'groupName')
        group_info['groupname'] = groupName.property('oldGroupName')
        group_info['new_groupname'] = groupName.property('text')
        
        members = []
        for user in self.parent.allUserModel.checked():
            members.append(user.username)

        group_info['members'] = members

        self.__interface.ModifyGroup(group_info)
        groupName.setProperty('oldGroupName', groupName.property('text'))
        self.parent.groupModel.reflesh()

    @QtCore.Slot(int, QtCore.QObject)
    def deleteUser(self, row, currentItem):
        userName = currentItem.findChild(QtDeclarative.QDeclarativeItem, 'delegateUserName')
        self.__interface.DeleteUser(userName.property('text'))
        self.parent.userModel.removeRows(row)

    @QtCore.Slot(int, QtCore.QObject)
    def deleteGroup(self, row, currentItem):
	groupName = currentItem.findChild(QtDeclarative.QDeclarativeItem, 'delegateGroupName')
	self.__interface.DeleteGroup(groupName.property('text'))
        self.parent.groupListModel.removeRow(row)

    @QtCore.Slot(QtCore.QObject)
    def reflesh(self, groupModel):
	pass

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def toggledGroup(self, model, group):
        group._toggle_checked()
        new_list = model.checked()
        print '='*20, 'New List', '='*20
        print '\n'.join(x.groupname for x in new_list)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def toggledUser(self, model, user):
        user._toggle_checked()
        new_list = model.checked()
        print '='*20, 'New List', '='*20
        print '\n'.join(x.username for x in new_list)

    @QtCore.Slot(str)
    def selectGroupByUser(self, username):
        members = self.__interface.ListGroupsByUser(username)
        self.parent.allGroupModel.selectMembers(members)

    @QtCore.Slot(str)
    def selectUserByGroup(self, groupname):
        members = self.__interface.ListUsersByGroup(groupname)
        self.parent.allUserModel.selectMembers(members)

    @QtCore.Slot()
    def quit(self):
        self.parent.quit()
