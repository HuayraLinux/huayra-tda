from PyQt4 import QtCore, QtGui
from Ui_frmPlayer import Ui_frmPlayer
import sys

class WidgetPlayer(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_frmPlayer()
        self.ui.setupUi(self)
        self.createVideoFrame()
        self.ui.layoutVideo.addWidget(self.videoframe)

    def createVideoFrame(self):
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        
