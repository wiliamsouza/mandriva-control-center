#from PySide import QtCore
from PyQt4 import QtCore

class Controller(QtCore.QObject):

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

    #@QtCore.Slot(QtCore.QObject)
    @QtCore.pyqtSlot(QtCore.QObject)
    def service_selected(self, service):
        print 'User clicked on:', service.name

    #@QtCore.Slot(QtCore.QObject, int)
    @QtCore.pyqtSlot(QtCore.QObject, int)
    def start_service(self, serviceModel, currentIndex):
        serviceModel.start(currentIndex)

    #@QtCore.Slot(QtCore.QObject, int)
    @QtCore.pyqtSlot(QtCore.QObject, int)
    def stop_service(self, serviceModel, currentIndex):
        serviceModel.stop(currentIndex)

    #@QtCore.Slot(QtCore.QObject, int)
    @QtCore.pyqtSlot(QtCore.QObject, int)
    def restart_service(self, serviceModel, currentIndex):
        serviceModel.restart(currentIndex)

    #@QtCore.Slot(QtCore.QObject, str)
    @QtCore.pyqtSlot(QtCore.QObject, str)
    def search(self, proxyServiceModel, text):
        proxyServiceModel.setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString))