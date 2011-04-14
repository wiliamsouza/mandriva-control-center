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

        view = QtDeclarative.QDeclarativeView(self)

        serviceModel = ServiceModel(view)
        serviceModel.populate()
        proxyServiceModel = ProxyServiceModel(serviceModel, parent=view)

        controller = Controller(view)

        context = view.rootContext()
        context.setContextProperty('controller', controller)
        context.setContextProperty('serviceModel', proxyServiceModel)

        view.setSource(QtCore.QUrl('/usr/share/mandriva/mcc2/frontends/services/views/SystemServices.qml'))
        #view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        view.setWindowTitle('Mandriva Control Center - System Services')


def CreatePlugin(widget_parent, parent, component_data):
    return ServicesModule(component_data, parent)