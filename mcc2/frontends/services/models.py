import dbus
import dbus.mainloop.glib

from PyQt4 import QtCore

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()
proxy = bus.get_object('org.mandrivalinux.mcc2.Services',
                       '/org/mandrivalinux/mcc2/Services')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Services')

proxy2 = bus.get_object('org.freedesktop.systemd1',
                        '/org/freedesktop/systemd1')
interface2 = dbus.Interface(proxy2, 'org.freedesktop.systemd1.Manager')
interface2.Subscribe()


class Service(QtCore.QObject):

    def __init__(self, servicePath, serviceDetails, parent):
        QtCore.QObject.__init__(self, parent)

        self.__servicePath = servicePath
        self.__serviceDetails = serviceDetails
	self.path = servicePath

    def __getName(self):
        return self.__serviceDetails['Id']

    def __getDescription(self):
        return self.__serviceDetails['Description']

    def __getLoadState(self):
        return self.__serviceDetails['LoadState']

    def __getActiveState(self):
        return self.__serviceDetails['ActiveState']

    def __getSubState(self):
        return self.__serviceDetails['SubState']

    def start(self):
        try:
            interface.Start(self.name, 'fail')
        except dbus.exceptions.DBusException, error:
            if error.get_dbus_name() == "org.freedesktop.DBus.Error.NoReply":
                print "timed out"
            if error.get_dbus_name() == "org.mandrivalinux.mcc2.Services.Error.NotAuthorized":
                print 'Not Authorized'

    def stop(self):
        try:
            interface.Stop(self.name, 'fail')
        except dbus.exceptions.DBusException, error:
            if error.get_dbus_name() == "org.freedesktop.DBus.Error.NoReply":
                print "Timed out"
            if error.get_dbus_name() == "org.mandrivalinux.mcc2.Services.Error.NotAuthorized":
                print 'Not Authorized'

    def restart(self):
        try:
            interface.Restart(self.name, 'fail')
        except dbus.exceptions.DBusException, error:
            if error.get_dbus_name() == "org.freedesktop.DBus.Error.NoReply":
               print "timed out"
            if error.get_dbus_name() == "org.mandrivalinux.mcc2.Services.Error.NotAuthorized":
                print 'Not Authorized'

    def update(self):
        self.__serviceDetails = interface.ServiceDetails(self.__servicePath)
        self.changed.emit()

    changed = QtCore.pyqtSignal()

    name = QtCore.pyqtProperty(unicode, __getName, notify=changed)
    description = QtCore.pyqtProperty(unicode, __getDescription, notify=changed)
    loadState = QtCore.pyqtProperty(unicode, __getLoadState, notify=changed)
    activeState = QtCore.pyqtProperty(unicode, __getActiveState, notify=changed)
    subState = QtCore.pyqtProperty(unicode, __getSubState, notify=changed)


class ServiceModel(QtCore.QAbstractListModel):
    COLUMNS = ('service',)

    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.parent = parent
        self.__services = []
        self.setRoleNames(dict(enumerate(ServiceModel.COLUMNS)))

        bus.add_signal_receiver(
                    self.on_properties_changed,
                    path_keyword='unit_path',
                    signal_name='PropertiesChanged',
                    dbus_interface='org.freedesktop.DBus.Properties',
                    bus_name='org.freedesktop.systemd1')


    def on_properties_changed(self, *args, **kargs):
        for service in self.__services:
            if service.path == kargs['unit_path']:
                service.update()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__services)

    def data(self, index, role):
        if index.isValid() and role == ServiceModel.COLUMNS.index('service'):
            return self.__services[index.row()]
        return None

    def _getService(self, row, serviceName):
	service = self.__services[row]
	if service.name != serviceName:
	    for service_ in self.__services:
		if service_.name == serviceName:
		    service = service_
	return service

    def start(self, row, serviceName):
        service = self._getService(row, serviceName)
        service.start()

    def stop(self, row, serviceName):
        service = self._getService(row, serviceName)
        service.stop()

    def restart(self, row, serviceName):
        service = self._getService(row, serviceName)
        service.restart()

    def populate(self):
        services = []
        for servicePath in interface.List():
            serviceDetails = interface.ServiceDetails(servicePath[6])
            # This filtering is done to avoid show up more than one .device
            # unit under different names
            if serviceDetails['Following'] == "":
                services.append(Service(servicePath[6],
                                        serviceDetails,
                                        parent=self.parent))
        self.__services = sorted(services, key=lambda service: service.name)
