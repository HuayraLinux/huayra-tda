from PyQt4 import QtCore, QtGui
from Ui_frmAbout import Ui_frmAbout

class WidgetAbout(QtGui.QDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_frmAbout()
        self.ui.setupUi(self)
