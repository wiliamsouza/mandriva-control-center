#from PySide import QtGui
from PyQt4 import QtGui


class ProxyServiceModel(QtGui.QSortFilterProxyModel):

    def __init__(self, parent=None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.setDynamicSortFilter(True)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        self.serviceModel = self.sourceModel()
        index = self.serviceModel.index(sourceRow, self.serviceModel.COLUMNS.index('service'))
        service = self.serviceModel.data(index, self.serviceModel.COLUMNS.index('service'))
        regex = self.filterRegExp()
        if regex.indexIn(service.name) != -1:
            return True
        return False

    def start(self, row):
        self.serviceModel.start(row)

    def stop(self, row):
        self.serviceModel.stop(row)

    def restart(self, row):
        self.serviceModel.restart(row)
