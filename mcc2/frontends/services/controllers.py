from PyQt4 import QtCore


class Controller(QtCore.QObject):

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

    @QtCore.pyqtSlot(QtCore.QObject, str, int)
    def start_service(self, serviceModel, serviceName, currentIndex):
        serviceModel.start(currentIndex, serviceName)

    @QtCore.pyqtSlot(QtCore.QObject, str, int)
    def stop_service(self, serviceModel, serviceName, currentIndex):
        serviceModel.stop(currentIndex, serviceName)

    @QtCore.pyqtSlot(QtCore.QObject, str, int)
    def restart_service(self, serviceModel, serviceName, currentIndex):
        serviceModel.restart(currentIndex, serviceName)

    @QtCore.pyqtSlot(QtCore.QObject, str)
    def search(self, proxyServiceModel, text):
        regex = QtCore.QRegExp(text,
                               QtCore.Qt.CaseInsensitive,
                               QtCore.QRegExp.RegExp)
        proxyServiceModel.setFilterRegExp(regex)
