#!/usr/bin/env python
import sys
sys.path.append('/usr/share/mandriva/')

from PyQt4 import QtGui, QtCore, QtDeclarative

from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication, KMainWindow, KCModule

from mcc2.frontends.users.models import UserModel, SystemUserModel, GroupModel, SystemGroupModel
from mcc2.frontends.users.controllers import Controller


class ServicesModule(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        view = QtDeclarative.QDeclarativeView(self)

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

        view.setSource(QtCore.QUrl('/usr/share/mandriva/mcc2/frontends/users/views/UsersAndGroups.qml'))
        #view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        view.setWindowTitle('Mandriva Control Center - Users and Groups')


def CreatePlugin(widget_parent, parent, component_data):
    return ServicesModule(component_data, parent)