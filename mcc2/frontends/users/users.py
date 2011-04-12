from PySide import QtCore, QtGui, QtDeclarative

from models import UserModel, SystemUserModel, GroupModel, SystemGroupModel
from controllers import Controller


def start():
    import sys
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    userModel = UserModel()
    userModel.populate()
    systemUserModel = SystemUserModel()
    systemUserModel.populate()
    groupModel = GroupModel()
    groupModel.populate()
    systemGroupModel = SystemGroupModel()
    systemGroupModel.populate()

    controller = Controller()

    context = view.rootContext()
    context.setContextProperty('groupModel', groupModel)
    context.setContextProperty('systemGroupModel', systemGroupModel)
    context.setContextProperty('userModel', userModel)
    context.setContextProperty('systemUserModel', systemUserModel)
    context.setContextProperty('controller', controller)

    view.setSource('/usr/share/mandriva/mcc2/frontends/users/views/UsersAndGroups.qml')
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.setWindowTitle('Mandriva Control Center - Users and Groups')
    view.connect(view.engine(), QtCore.SIGNAL('quit()'), app, QtCore.SLOT('quit()'));
    view.show()
    app.exec_()


if __name__ == '__main__':
    start()




    """
    flags = QtCore.Qt.WindowFlags()
    flags |= QtCore.Qt.FramelessWindowHint
 
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    window.setWindowFlags(flags)
    view = QtDeclarative.QDeclarativeView()
    view.setSource('views/UsersAndGroups.qml')
    
    userModel = UserModel()
    userModel.populate()
    systemUserModel = SystemUserModel()
    systemUserModel.populate()
    groupModel = GroupModel()
    groupModel.populate()
    systemGroupModel = SystemGroupModel()
    systemGroupModel.populate()

    controller = Controller()

    context = view.rootContext()
    context.setContextProperty('groupModel', groupModel)
    context.setContextProperty('systemGroupModel', systemGroupModel)
    context.setContextProperty('userModel', userModel)
    context.setContextProperty('systemUserModel', systemUserModel)
    
    context.setContextProperty('controller', controller)
    
    widget = QtGui.QWidget()
    widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    widget.setWindowFlags(flags)
    view.setViewport(widget)
    window.setCentralWidget(view)
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    window.show()
    app.exec_()
    """
"""
class UsersAndGroupView(QtDeclarative.QDeclarativeView):

    def __init__(self):
        QtDeclarative.QDeclarativeView.__init__(self)
        self.ResizeMode = QtDeclarative.QDeclarativeView.SizeRootObjectToView
        self.setWindowTitle('Mandriva Control Center - Users and Groups')
        self.groupListModel = GroupListModel()
        self.groupListModel.populate()
        self.context = self.rootContext()
        self.context.setContextProperty('groupListModel', self.groupListModel)
        self.setSource('views/UsersAndGroups.qml')

    def closeEvent(self, event):
        print 'close event'
        event.accept()


class UsersAndGroupsGui(object):

    def __init__(self, argv):
        self.app = QtGui.QApplication(argv)
        self.view = UsersAndGroupView()
        self.view.show()

    def run(self):
        return self.app.exec_()
"""
