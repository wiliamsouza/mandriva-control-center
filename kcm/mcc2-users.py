#!/usr/bin/env python

import sys
sys.path.append('/usr/share/mandriva/')

from PyQt4 import QtGui

#from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KCModule

from mcc2.frontends.users.users import UsersView


class UsersModule(KCModule):

    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        self.vbox = QtGui.QVBoxLayout(self)
        self.view = UsersView(self)
        self.vbox.addWidget(self.view)


def CreatePlugin(widget_parent, parent, component_data):
    return UsersModule(component_data, parent)