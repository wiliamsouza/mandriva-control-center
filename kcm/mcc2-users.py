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

        self.view = QtDeclarative.QDeclarativeView(self)

        self.userModel = UserModel(self.view)
        self.userModel.populate()
        self.systemUserModel = SystemUserModel(self.view)
        self.systemUserModel.populate()
        self.groupModel = GroupModel(self.view)
        self.groupModel.populate()
        self.systemGroupModel = SystemGroupModel(self.view)
        self.systemGroupModel.populate()

        self.controller = Controller(self.view)

        self.context = self.view.rootContext()
        self.context.setContextProperty('groupModel', self.groupModel)
        self.context.setContextProperty('systemGroupModel', self.systemGroupModel)
        self.context.setContextProperty('userModel', self.userModel)
        self.context.setContextProperty('systemUserModel', self.systemUserModel)
        self.context.setContextProperty('controller', self.controller)

        self.view.setSource(QtCore.QUrl('/usr/share/mandriva/mcc2/frontends/users/views/UsersAndGroups.qml'))
        #view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.view.setWindowTitle('Mandriva Control Center - Users and Groups')


def CreatePlugin(widget_parent, parent, component_data):
    return ServicesModule(component_data, parent)