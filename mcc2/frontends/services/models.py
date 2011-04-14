#from PySide import QtCore
from PyQt4 import QtCore

import dbus
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()
proxy = bus.get_object('org.mandrivalinux.mcc2.Services',
                       '/org/mandrivalinux/mcc2/Services')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Services')

bus2 = dbus.SystemBus()
proxy2 = bus2.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
interface2 = dbus.Interface(proxy2, 'org.freedesktop.systemd1.Manager')
interface2.Subscribe()

class Service(QtCore.QObject):

    def __init__(self, servicePath, serviceDetails, parent):
        QtCore.QObject.__init__(self, parent)
        self.__servicePath = servicePath
        self.__serviceDetails = serviceDetails

        #unit_proxy = bus2.get_object('org.freedesktop.systemd1', self.__servicePath)
        #properties_interface = dbus.Interface(unit_proxy, 'org.freedesktop.DBus.Properties')

        properties_proxy = bus2.get_object('org.freedesktop.systemd1', self.__servicePath)
        properties_interface = dbus.Interface(properties_proxy, 'org.freedesktop.DBus.Properties')
        properties_interface.connect_to_signal('PropertiesChanged', self.on_properties_changed)

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
        self.update()

    def stop(self):
        try:
            interface.Stop(self.name, 'fail')
        except dbus.exceptions.DBusException, error:
            if error.get_dbus_name() == "org.freedesktop.DBus.Error.NoReply":
                print "Timed out"
            if error.get_dbus_name() == "org.mandrivalinux.mcc2.Services.Error.NotAuthorized":
                print 'Not Authorized'
        self.update()

    def restart(self):
        try:
            interface.Restart(self.name, 'fail')
        except dbus.exceptions.DBusException, error:
            if error.get_dbus_name() == "org.freedesktop.DBus.Error.NoReply":
                print "timed out"
            if error.get_dbus_name() == "org.mandrivalinux.mcc2.Services.Error.NotAuthorized":
                print 'Not Authorized'
        self.update()

    def on_properties_changed(self, *args, **kargs):
        self.update()

    def update(self):
        self.__serviceDetails = interface.ServiceDetails(self.__servicePath)
        self.changed.emit()

    #changed = QtCore.Signal()
    changed = QtCore.pyqtSignal()

    """
    name = QtCore.Property(unicode, __getName, notify=changed)
    description = QtCore.Property(unicode, __getDescription, notify=changed)
    loadState = QtCore.Property(unicode, __getLoadState, notify=changed)
    activeState = QtCore.Property(unicode, __getActiveState, notify=changed)
    subState = QtCore.Property(unicode, __getSubState, notify=changed)
    """

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

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__services)

    def data(self, index, role):
        if index.isValid() and role == ServiceModel.COLUMNS.index('service'):
            return self.__services[index.row()]
        return None
 
    def start(self, row):
        service = self.__services[row]
        service.start()
    
    def stop(self, row):
        service = self.__services[row]
        service.stop()

    def restart(self, row):
        service = self.__services[row]
        service.restart()

    def populate(self):
        count = 0
        for servicePath in interface.List():
            serviceDetails = interface.ServiceDetails(servicePath[6])
            # This filtering is done to avoid show up more than one .device unit
            # under different names
            if serviceDetails['Following'] == "":
                self.__services.append(Service(servicePath[6], serviceDetails, parent=self.parent))
            else:
                count = count + 1
        #print '%d .device unit removed by duplicity' % count