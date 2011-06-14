#!/usr/bin/env python

import sys

from PyQt4 import QtCore, QtGui, QtDeclarative

from mcc2.frontends.users.controllers import Controller
from mcc2.frontends.users.models import (UserModel, SystemUserModel,
                                         GroupModel, SystemGroupModel,
					 ShellModel)


class UsersView(QtDeclarative.QDeclarativeView):

    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeView.__init__(self, parent)

        self.userModel = UserModel(self)
        self.userModel.populate()
        self.systemUserModel = SystemUserModel(self)
        self.systemUserModel.populate()
        self.groupModel = GroupModel(self)
        self.groupModel.populate()
	self.shellModel = ShellModel(self)
	self.shellModel.populate()
        self.systemGroupModel = SystemGroupModel(self)
        self.systemGroupModel.populate()

        self.controller = Controller(self)

        self.context = self.rootContext()
        self.context.setContextProperty('groupModel', self.groupModel)
        self.context.setContextProperty('systemGroupModel', self.systemGroupModel)
        self.context.setContextProperty('userModel', self.userModel)
        self.context.setContextProperty('systemUserModel', self.systemUserModel)
	self.context.setContextProperty('shellModel', self.shellModel)
        self.context.setContextProperty('controller', self.controller)

        self.setSource(QtCore.QUrl('/usr/share/mandriva/mcc2/frontends/users/views/UsersAndGroups.qml'))

        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.setWindowTitle('Mandriva Control Center - Users and Groups')


def start():

    app = QtGui.QApplication(sys.argv)

    locale = QtCore.QLocale.system()
    translator = QtCore.QTranslator()

    i18n_file = 'UsersAndGroups_' + locale.name() + '.qm'
    i18n_path = '/usr/share/mandriva/mcc2/frontends/users/views/i18n/'

    if (translator.load(i18n_file, i18n_path)):
        app.installTranslator(translator)

    view = UsersView()
    view.show()
    app.exec_()


if __name__ == '__main__':
    start()
