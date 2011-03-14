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
        #TODO: Make a check if OpenGL is supported
        #self.widget = QtOpenGL.QGLWidget()
        self.widget = QtGui.QWidget()
        self.view.setViewport(self.widget)
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


        _controller = Controller(self)
        userModel = UserModel(users)
        allUserModel = UserModel(allUsers)
        groupModel = GroupModel(groups)
        allGroupModel = GroupModel(allGroups)

        self.root_context = self.view.rootContext()
        self.root_context.setContextProperty('controller', _controller)
        self.root_context.setContextProperty('userModel', userModel)
        self.root_context.setContextProperty('allUserModel', allUserModel)
        self.root_context.setContextProperty('groupModel', groupModel)
        self.root_context.setContextProperty('allGroupModel', allGroupModel)

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
