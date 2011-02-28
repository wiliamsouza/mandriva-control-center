from PySide import QtGui, QtCore
from PySide import QtDeclarative

import dbus
#import dbus.mainloop.glib
#dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

import sys

from models import User, UserModel
#from mcc2.frontend.users.models import User, UserModel
#from mcc2.frontend.users.controller import


#class ServiceController(QtCore.QObject):
#
#    @QtCore.Slot(QtCore.QObject)
#    def service_selected(self, service):
#        print 'User clicked on:', service._service['Id']


def start():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    view = QtDeclarative.QDeclarativeView()
    widget = QtGui.QWidget()
    view.setViewport(widget)
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    bus = dbus.SystemBus()
    proxy = bus.get_object(
        'org.mandrivalinux.mcc2.Users',
        '/org/mandrivalinux/mcc2/Users')
    interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Users')
    
    users = []
    for user in interface.ListUsers():
        users.append(User(user))

    #userController = UserController()
    userModel = UserModel(users)

    root_context = view.rootContext()
    #root_context.setContextProperty('userController', userController)
    root_context.setContextProperty('userModel', userModel)

    view.setSource('views/Main.qml')
    window.setCentralWidget(view)
    window.show()
    app.exec_()

if __name__ == '__main__':
    start()