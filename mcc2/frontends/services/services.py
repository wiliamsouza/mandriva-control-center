#from PySide import QtGui, QtCore, QtDeclarative
from PyQt4 import QtGui, QtCore, QtDeclarative

from mcc2.frontends.services.models import ServiceModel
from mcc2.frontends.services.proxy import ProxyServiceModel
from mcc2.frontends.services.controllers import Controller


def start():
    import sys
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()

    serviceModel = ServiceModel(view)
    serviceModel.populate()
    proxyServiceModel = ProxyServiceModel(serviceModel, parent=view)

    controller = Controller(view)

    context = view.rootContext()
    context.setContextProperty('controller', controller)
    context.setContextProperty('serviceModel', proxyServiceModel)

    view.setSource(QtCore.QUrl('/usr/share/mandriva/mcc2/frontends/services/views/SystemServices.qml'))
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.setWindowTitle('Mandriva Control Center - System Services')
    view.connect(view.engine(), QtCore.SIGNAL('quit()'), app, QtCore.SLOT('quit()'));
    view.show()
    app.exec_()

if __name__ == '__main__':
    start()