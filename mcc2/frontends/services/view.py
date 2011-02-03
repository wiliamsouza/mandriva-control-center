import sys
import dbus

from PySide import QtGui, QtCore
from PySide import QtDeclarative

import dbus
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from model import ServiceWrapper, ServiceModel
#from controller import ServiceController

from PySide import QtCore

bus = dbus.SystemBus()
proxy = bus.get_object(
    'org.mandrivalinux.mcc2.Services',
    '/org/mandrivalinux/mcc2/Services')
interface = dbus.Interface(proxy, 'org.mandrivalinux.mcc2.Services')

class ServiceController(QtCore.QObject):
    @QtCore.Slot(QtCore.QObject)
    def service_selected(self, service):
        print 'User clicked on:', service._service['Id']

    @QtCore.Slot(QtCore.QObject)
    def start_service(self, service):
        service = service.property('text')
        print 'Starting', service
        try:
            interface.Start(service, 'fail')
        except dbus.exceptions.DBusException, error:
            if error.get_dbus_name() == "org.freedesktop.DBus.Error.NoReply":
                print "timed out"
            if error.get_dbus_name() == "org.mandrivalinux.mcc2.Services.Error.NotAuthorized":
                print 'Not Authorized'

    @QtCore.Slot(QtCore.QObject)
    def stop_service(self, service):
        service = service.property('text')
        print 'Stoping:', service
        try:
            interface.Stop(service, 'fail')
        except dbus.exceptions.DBusException, error:
            if error.get_dbus_name() == "org.freedesktop.DBus.Error.NoReply":
                print "Timed out"
            if error.get_dbus_name() == "org.mandrivalinux.mcc2.Services.Error.NotAuthorized":
                print 'Not Authorized'

    @QtCore.Slot(QtCore.QObject)
    def restart_service(self, service):
        service = service.property('text')
        print 'Restarting:', service
        try:
            interface.Restart(service, 'fail')
        except dbus.exceptions.DBusException, error:
            if error.get_dbus_name() == "org.freedesktop.DBus.Error.NoReply":
                print "timed out"
            if error.get_dbus_name() == "org.mandrivalinux.mcc2.Services.Error.NotAuthorized":
                print 'Not Authorized'

def start():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    view = QtDeclarative.QDeclarativeView()
    widget = QtGui.QWidget()
    view.setViewport(widget)
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

    services = []
    for service in interface.List():
        details = interface.ServiceDetails(service[6])
        services.append(ServiceWrapper(details))

    service_controller = ServiceController()
    service_model = ServiceModel(services)

    rc = view.rootContext()
    rc.setContextProperty('serviceController', service_controller)
    rc.setContextProperty('serviceModel', service_model)
    view.setSource('/usr/share/mcc2/mcc2/frontends/services/qml/Services.qml')
    window.setCentralWidget(view)
    window.show()
    app.exec_()

if __name__ == '__main__':
    start()