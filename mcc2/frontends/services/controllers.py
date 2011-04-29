from PyQt4 import QtCore


class Controller(QtCore.QObject):

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

    @QtCore.pyqtSlot(QtCore.QObject, int)
    def start_service(self, serviceModel, currentIndex):
        serviceModel.start(currentIndex)

    @QtCore.pyqtSlot(QtCore.QObject, int)
    def stop_service(self, serviceModel, currentIndex):
        serviceModel.stop(currentIndex)

    @QtCore.pyqtSlot(QtCore.QObject, int)
    def restart_service(self, serviceModel, currentIndex):
        serviceModel.restart(currentIndex)

    @QtCore.pyqtSlot(QtCore.QObject, str)
    def search(self, proxyServiceModel, text):
        regex = QtCore.QRegExp(text,
                               QtCore.Qt.CaseInsensitive,
                               QtCore.QRegExp.FixedString)
        proxyServiceModel.setFilterRegExp(regex)