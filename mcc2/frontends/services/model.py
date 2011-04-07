from PySide import QtCore

import dbus
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()
proxy = bus.get_object('org.mandrivalinux.mcc2.Services',
                       '/org/mandrivalinux/mcc2/Services')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Services')

class Service(QtCore.QObject):
    def __init__(self, servicePath, serviceDetails):
        QtCore.QObject.__init__(self)
        self.__servicePath = servicePath
        self.__serviceDetails = serviceDetails

    def _name(self):
        return self.__serviceDetails['Id']

    def _description(self):
        return self.__serviceDetails['Description']

    def _load_state(self):
        return self.__serviceDetails['LoadState']

    def _active_state(self):
        return self.__serviceDetails['ActiveState']

    def _sub_state(self):
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

    def update(self):
        self.__serviceDetails = interface.ServiceDetails(self.__servicePath)
        self.changed.emit()

    changed = QtCore.Signal()

    name = QtCore.Property(unicode, _name, notify=changed)
    description = QtCore.Property(unicode, _description, notify=changed)
    load_state = QtCore.Property(unicode, _load_state, notify=changed)
    active_state = QtCore.Property(unicode, _active_state, notify=changed)
    sub_state = QtCore.Property(unicode, _sub_state, notify=changed)


class ServiceModel(QtCore.QAbstractListModel):
    COLUMNS = ('service',)

    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
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
                self.__services.append(Service(servicePath[6], serviceDetails))
            else:
                count = count + 1
        print '%d .device unit removed by duplicity' % count