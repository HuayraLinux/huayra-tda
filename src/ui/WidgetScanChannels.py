from PyQt4 import QtCore, QtGui
from Ui_frmScanChannels import Ui_Form

class WidgetScanChannels(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        ui = Ui_Form()
        ui.setupUi(self)
