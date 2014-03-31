from PyQt4 import QtCore, QtGui
from Ui_frmScanChannels import Ui_frmScan

class WidgetScanChannels(QtGui.QWidget):
    def __init__(self, scanner_class, config):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_frmScan()
        self.ui.setupUi(self)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)
        self.scanner_class = scanner_class
        self.scanner = None
        self.scanRunning = False
        self.connect(self.ui.btnScan, QtCore.SIGNAL("clicked()"), self.startScan)
        self.connect(self.ui.btnStop, QtCore.SIGNAL("clicked()"), self.terminateScan)
        self.connect(self.ui.btnBack, QtCore.SIGNAL("clicked()"), self.goBack)  
        self.ui.btnStop.hide()
        self.config = config

    def updateUI(self):
        if self.scanRunning:
            if self.scanner.terminated():
                self.scanFinalized()
            val = self.ui.progressBar.value()
            if self.ui.progressBar.invertedAppearance():
                val -= 5
                if val < 0:
                    self.ui.progressBar.setInvertedAppearance(False)
                    val = 0
            else:
                val += 5
                if val > 100:
                    self.ui.progressBar.setInvertedAppearance(True)
                    val = 100
            self.ui.progressBar.setValue(val)

    def scanFinalized(self):
        if not self.scanner.terminatedOk():
            return
        self.config.save(self.scanner.result())
        self.freeScan()
        
    def terminateScan(self):
        self.scanner.cancel()
        self.freeScan()

    def freeScan(self):
        self.scanner = None
        self.scanRunning = False
        self.ui.lblInfo.setText("listo para escanear !")
        self.timer.stop()
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setInvertedAppearance(False)
        self.ui.btnStop.hide()
        self.ui.btnScan.show()

    def startScan(self):
        self.scanRunning = True
        self.scanner = self.scanner_class("/etc/huayra-tda/isdb-t.txt")
        self.ui.lblInfo.setText("escaneando !")
        self.timer.start()
        self.ui.btnScan.hide()
        self.ui.btnStop.show()

    def goBack(self):
        self.emit(QtCore.SIGNAL("back"))
