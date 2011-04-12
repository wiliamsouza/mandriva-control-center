from PySide import QtGui


class ProxyServiceModel(QtGui.QSortFilterProxyModel):
    
    def __init__(self, serviceModel, parent=None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.serviceModel = serviceModel
        self.setSourceModel(serviceModel)
        self.setDynamicSortFilter(True)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.serviceModel.index(sourceRow, 0)
        service = self.serviceModel.data(index, 0)
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