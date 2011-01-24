from PySide import QtCore

class ServiceWrapper(QtCore.QObject):
    def __init__(self, service):
        QtCore.QObject.__init__(self)
        self._service = service

    def _name(self):
        return self._service['Id']

    def _description(self):
        return self._service['Description']

    def _load_state(self):
        return self._service['LoadState']

    def _active_state(self):
        return self._service['ActiveState']

    def _sub_state(self):
        return self._service['SubState']

    changed = QtCore.Signal()

    name = QtCore.Property(unicode, _name, notify=changed)
    description = QtCore.Property(unicode, _description, notify=changed)
    load_state = QtCore.Property(unicode, _load_state, notify=changed)
    active_state = QtCore.Property(unicode, _active_state, notify=changed)
    sub_state = QtCore.Property(unicode, _sub_state, notify=changed)

class ServiceModel(QtCore.QAbstractListModel):
    COLUMNS = ('service',)

    def __init__(self, service):
        QtCore.QAbstractListModel.__init__(self)
        self._service = service
        self.setRoleNames(dict(enumerate(ServiceModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._service)

    def data(self, index, role):
        if index.isValid() and role == ServiceModel.COLUMNS.index('service'):
            return self._service[index.row()]
        return None