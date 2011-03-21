import sys

import dbus

from PySide import QtGui, QtCore
from PySide import QtDeclarative
from PySide import QtOpenGL

from models import User, UserModel, Group, GroupModel
#from mcc2.frontend.users.models import User, UserModel, Group, GroupModel
from controller import Controller
#from mcc2.frontend.users.controller import Controller


class UsersGui(object):

    def __init__(self, argv):
        self.app = QtGui.QApplication(argv)
        self.view = QtDeclarative.QDeclarativeView()
        self.view.setResizeMode(
            QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.bus = dbus.SystemBus()
        self.proxy = self.bus.get_object(
            'org.mandrivalinux.mcc2.Users',
            '/org/mandrivalinux/mcc2/Users')
        self.interface = dbus.Interface(
            self.proxy, 'org.mandrivalinux.mcc2.Users')

        users = []
        for user in self.interface.ListUsers():
            users.append(User(user))

        allUsers = []
        for user in self.interface.ListAllUsers():
            allUsers.append(User(user))

        groups = []
        for group in self.interface.ListGroups():
            groups.append(Group(group))

        allGroups = []
        for group in self.interface.ListAllGroups():
            allGroups.append(Group(group))


        self.controller = Controller(self)
        self.userModel = UserModel(users)
        self.allUserModel = UserModel(allUsers)
        self.groupModel = GroupModel(groups)
        self.allGroupModel = GroupModel(allGroups)

        self.root_context = self.view.rootContext()
        self.root_context.setContextProperty('controller', self.controller)
        self.root_context.setContextProperty('userModel', self.userModel)
        self.root_context.setContextProperty('allUserModel', self.allUserModel)
        self.root_context.setContextProperty('groupModel', self.groupModel)
        self.root_context.setContextProperty('allGroupModel', self.allGroupModel)

        self.view.setSource('views/Main.qml')
        self.view.setWindowTitle('Mandriva Control Center - Users and Groups')
        self.view.show()

    def run(self):
        return self.app.exec_()

    def quit(self):
        self.app.quit()

if __name__ == '__main__':
    gui = UsersGui(sys.argv)
    gui.run()
