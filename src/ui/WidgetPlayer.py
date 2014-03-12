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
        self.connect(self.ui.btnShowChannelsList, QtCore.SIGNAL("clicked()"), self.showHideChannelsList)
        self.connect(self.ui.btnChannelUp, QtCore.SIGNAL("clicked()"), self.channelUp)
        self.connect(self.ui.btnChannelDown, QtCore.SIGNAL("clicked()"), self.channelDown)
                
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

    def showHideChannelsList(self):
        if self.ui.listViewChannels.isHidden():
            self.ui.listViewChannels.show()
        else:
            self.ui.listViewChannels.hide()

    def channelUp(self):
        self.player.gotoChannelUp()

    def channelDown(self):
        self.player.gotoChannelDown()

    def paintEvent(self, pe):
        opt = QtGui.QStyleOption()
        opt.init(self)
        p = QtGui.QPainter(self)
        s = self.style()
        s.drawPrimitive(QtGui.QStyle.PE_Widget, opt, p, self)
        #  QStyleOption o;                                                                                                                                                                  
#  o.initFrom(this);                                                                                                                                                                
#  QPainter p(this);                                                                                                                                                                
#  style()->drawPrimitive(QStyle::PE_Widget, &o, &p, this);                                                                                                                         
#};
