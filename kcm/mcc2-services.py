#!/usr/bin/env python
import sys
sys.path.append('/usr/share/mandriva/')

from PyQt4 import QtGui, QtCore, QtDeclarative

from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication, KMainWindow, KCModule

from mcc2.frontends.services.models import ServiceModel
from mcc2.frontends.services.proxy import ProxyServiceModel
from mcc2.frontends.services.controllers import Controller


class ServicesModule(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        self.view = QtDeclarative.QDeclarativeView(self)

        self.proxyServiceModel = ProxyServiceModel(parent=self)
        self.serviceModel = ServiceModel(self.proxyServiceModel)
        self.serviceModel.populate()
        self.proxyServiceModel.setSourceModel(self.serviceModel)

        self.controller = Controller(self)

        self.context = self.view.rootContext()
        self.context.setContextProperty('controller', self.controller)
        self.context.setContextProperty('serviceModel', self.proxyServiceModel)

        self.view.setSource(QtCore.QUrl('/usr/share/mandriva/mcc2/frontends/services/views/SystemServices.qml'))
        self.view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        self.view.setWindowTitle('Mandriva Control Center - System Services')

        #self.connect(self.view, QtCore.SIGNAL("clientClosed()"), self.onClose)
        #self.connect(self.view, QtCore.SIGNAL("clientIsEmbedded()"), self.isLoaded)

    """
    def onClose(self):
        print "*"*80
        print "onClose"
        self.view.destroy()

    def isLoaded(self):
        print "*"*80
        print "isLoaded"
        self.view.setFocus()
        self.view.adjustSize()
    """

def CreatePlugin(widget_parent, parent, component_data):
    return ServicesModule(component_data, parent)