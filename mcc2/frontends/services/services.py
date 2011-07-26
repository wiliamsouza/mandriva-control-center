#!/usr/bin/env python

import sys

from PyQt4 import QtGui, QtCore, QtDeclarative

from mcc2.frontends.services.controllers import Controller
from mcc2.frontends.services.models import ServiceModel
from mcc2.frontends.services.proxy import ProxyServiceModel


class SystemServicesView(QtDeclarative.QDeclarativeView):

    def __init__(self, parent=None):
        QtDeclarative.QDeclarativeView.__init__(self, parent)

        self.proxyServiceModel = ProxyServiceModel(parent=self)
        self.serviceModel = ServiceModel(self.proxyServiceModel)
        self.serviceModel.populate()
        self.proxyServiceModel.setSourceModel(self.serviceModel)

        self.controller = Controller(self)

        self.context = self.rootContext()
        self.context.setContextProperty('controller', self.controller)
        self.context.setContextProperty('serviceModel', self.proxyServiceModel)

        self.setSource(QtCore.QUrl('/usr/share/mandriva/mcc2/frontends/services/views/SystemServices.qml'))
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.setWindowTitle('Mandriva Control Center - System Services')


def start():

    app = QtGui.QApplication(sys.argv)

    locale = QtCore.QLocale.system()
    translator = QtCore.QTranslator()

    i18n_file = 'SystemServices_' + locale.name() + '.qm'
    i18n_path = '/usr/share/mandriva/mcc2/frontends/services/views/i18n/'

    if (translator.load(i18n_file, i18n_path)):
        app.installTranslator(translator)

    view = SystemServicesView()
    view.show()
    app.exec_()


if __name__ == '__main__':
    start()
