import dbus

from PySide import QtCore
from PySide.QtDeclarative import QDeclarativeItem


bus = dbus.SystemBus(private=True)
proxy = bus.get_object('org.mandrivalinux.mcc2.Users',
                       '/org/mandrivalinux/mcc2/Users')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')


class Controller(QtCore.QObject):

    def __init__(self):
        QtCore.QObject.__init__(self)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def addGroup(self, groupModel, groupForm):
        groupName = groupForm.findChild(QDeclarativeItem, 'groupNameAddForm')
        specifyGid = groupForm.findChild(QDeclarativeItem, 'specifyGidAddForm')
        groupId = groupForm.findChild(QDeclarativeItem, 'groupIdAddForm')

        gid = interface.FirstUnusedGid()
        if specifyGid.property('checked'):
            #TODO: Add exception handler here
            gid = int(groupId.property('text'))

        groupModel.add(groupName.property('text'), gid)

        groupName.setProperty('text', '')
        specifyGid.setProperty('checked', False)
        groupId.setProperty('text', '')
 
    @QtCore.Slot(QtCore.QObject, QtCore.QObject, QtCore.QObject, int)
    def modifyGroup(self, groupModel, systemUserModel, editGroupForm, currentIndex):
        groupName = editGroupForm.findChild(QDeclarativeItem, 'groupName')
        members = []
        for user in systemUserModel.checked():
            members.append(user.userName)
        groupModel.modify(groupName.property('text'), members, currentIndex)
 
    @QtCore.Slot(QtCore.QObject, QtCore.QObject, int)
    def deleteGroup(self, groupModel, currentItem, currentIndex):
        groupName = currentItem.findChild(QDeclarativeItem, 'delegateGroupName')
        groupModel.delete(groupName.property('text'), currentIndex)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def toggledUser(self, systemUserModel, user):
        user.toggleChecked()

    @QtCore.Slot(QtCore.QObject, QtCore.QObject, QtCore.QObject)
    def addUser(self, userModel, userForm, groupModel):
        userDetails = {}

        fullName = userForm.findChild(QDeclarativeItem, 'fullNameAddForm')
        userName = userForm.findChild(QDeclarativeItem, 'userNameAddForm')
        password = userForm.findChild(QDeclarativeItem, 'passwordAddForm')
        confirmPassword = userForm.findChild(QDeclarativeItem, 'confirmPasswordAddForm')
        loginShell = userForm.findChild(QDeclarativeItem, 'loginShellAddForm')
        createHomeDirectory = userForm.findChild(QDeclarativeItem, 'createHomeDirectoryAddForm')
        homeDirectory = userForm.findChild(QDeclarativeItem, 'homeDirectoryAddForm')
        createPrivateGroup = userForm.findChild(QDeclarativeItem, 'createPrivateGroupAddForm')
        specifyUserId = userForm.findChild(QDeclarativeItem, 'specifyUserIdAddForm')
        userId = userForm.findChild(QDeclarativeItem, 'userIdAddForm')

        if fullName.property('text') != '':
            userDetails['fullName'] = fullName.property('text')

        if userName.property('text') != '':
            userDetails['userName'] = userName.property('text')
        else:
            #TODO Show up an error message to warn the user
            # test if minimum user name length was entered
            pass

        if password.property('text') == confirmPassword.property('text'):
            if password.property('text') != '':
                userDetails['password'] = password.property('text')
            else:
                #TODO Show up an error message to warn the user
                # test if minimum user name length was entered
                pass
        else:
            #TODO Show up an error message to warn the user
            # test if minimum user name length was entered
            pass

        if loginShell.property('text') != '':
            userDetails['loginShell'] = loginShell.property('text')
        else:
            #TODO Show up an error message to warn the user
            pass

        if createHomeDirectory.property('checked'):
            userDetails['createHome'] = True
            userDetails['homeDirectory'] = homeDirectory.property('text')

        gid = interface.FirstUnusedGid()
        if createPrivateGroup.property('checked'):
            userDetails['gid'] = gid

        userDetails['uid'] = interface.FirstUnusedUid()
        if specifyUserId.property('checked'):
            userDetails['uid'] = userId.property('text')

        userModel.add(userDetails)
        groupModel.add(userName.property('text'), gid)

        fullName.setProperty('text', '')
        userName.setProperty('text', '')
        password.setProperty('text', '')
        confirmPassword.setProperty('text', '')
        loginShell.setProperty('text', '/bin/bash')
        createHomeDirectory.setProperty('checked', True)
        homeDirectory.setProperty('text', '/home/')
        createPrivateGroup.setProperty('checked', True)
        specifyUserId.setProperty('checked', False)
        userId.setProperty('text', '')

    @QtCore.Slot(QtCore.QObject, QtCore.QObject, int)
    def modifyUser(self, userModel, editUserForm, currentIndex):
        modifyUserDetails = {}
        fullName = editUserForm.findChild(QDeclarativeItem, 'fullName')
        userName = editUserForm.findChild(QDeclarativeItem, 'userName')
        password = editUserForm.findChild(QDeclarativeItem, 'password')
        confirmPassword = editUserForm.findChild(QDeclarativeItem, 'confirmPassword')
        loginShell = editUserForm.findChild(QDeclarativeItem, 'loginShell')
        homeDirectory = editUserForm.findChild(QDeclarativeItem, 'homeDirectory')
        shadowExpire = editUserForm.findChild(QDeclarativeItem, 'shadowExpire')
        expirationDate = editUserForm.findChild(QDeclarativeItem, 'expirationDate')
        blockAccount = editUserForm.findChild(QDeclarativeItem, 'blockAccount')
        shadowMin = editUserForm.findChild(QDeclarativeItem, 'shadowMin')
        shadowMax = editUserForm.findChild(QDeclarativeItem, 'shadowMax')
        shadowWarning = editUserForm.findChild(QDeclarativeItem, 'shadowWarning')
        shadowInactive = editUserForm.findChild(QDeclarativeItem, 'shadowInactive')

        modifyUserDetails['fullName'] = fullName.property('text')

        if userName.property('text') != '':
            modifyUserDetails['userName'] = userName.property('text')
        else:
            #TODO Show up an error message to warn the user
            # test if minimum user name length was entered
            pass

        if password.property('text') == confirmPassword.property('text'):
            modifyUserDetails['password'] = password.property('text')
            """
            if password.property('text') != '':
                
            else:
                #TODO Show up an error message to warn the user
                # test if minimum user name length was entered
                pass
            """
        else:
            #TODO Show up an error message to warn the user
            # test if minimum user name length was entered
            pass

        if loginShell.property('text') != '':
            modifyUserDetails['loginShell'] = loginShell.property('text')
        else:
            #TODO Show up an error message to warn the user
            pass

        modifyUserDetails['homeDirectory'] = homeDirectory.property('text')

        #TODO: Implement the possibility to chose the primary group membership

        if shadowExpire.property('checked'):
            modifyUserDetails['expirationDate'] = expirationDate.property('text')

        if blockAccount.property('checked'):
            userModel.lock(currentIndex)
        else:
            userModel.unLock(currentIndex)
        
        modifyUserDetails['shadowMin'] = shadowMin.property('text')
        modifyUserDetails['shadowMax'] = shadowMax.property('text')
        modifyUserDetails['shadowWarning'] = shadowWarning.property('text') 
        modifyUserDetails['shadowInactive'] = shadowInactive.property('text')

        userModel.modify(modifyUserDetails, currentIndex)

    @QtCore.Slot(QtCore.QObject, QtCore.QObject, int)
    def deleteUser(self, userModel, currentItem, currentIndex):
        userName = currentItem.findChild(QDeclarativeItem, 'delegateUserName')
        userModel.delete(userName.property('text'), currentIndex)
        
    @QtCore.Slot(QtCore.QObject, QtCore.QObject)
    def toggledGroup(self, systemGroupModel, group):
        group.toggleChecked()