from PySide import QtGui, QtCore, QtDeclarative

from model import ServiceModel
from controllers import Controller


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    
    serviceModel = ServiceModel()
    serviceModel.populate()
    controller = Controller()

    context = view.rootContext()
    context.setContextProperty('controller', controller)
    context.setContextProperty('serviceModel', serviceModel)

    view.setSource('views/SystemServices.qml')
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.setWindowTitle('Mandriva Control Center - System Services')
    view.connect(view.engine(), QtCore.SIGNAL('quit()'), app, QtCore.SLOT('quit()'));
    view.show()
    app.exec_()