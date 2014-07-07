# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/scan_channels.ui'
#
# Created: Mon Jul  7 15:55:50 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmScan(object):
    def setupUi(self, frmScan):
        frmScan.setObjectName(_fromUtf8("frmScan"))
        frmScan.resize(412, 270)
        self.verticalLayout = QtGui.QVBoxLayout(frmScan)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.lblInfo = QtGui.QLabel(frmScan)
        self.lblInfo.setMaximumSize(QtCore.QSize(800, 350))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblInfo.setFont(font)
        self.lblInfo.setText(_fromUtf8(""))
        self.lblInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblInfo.setWordWrap(True)
        self.lblInfo.setObjectName(_fromUtf8("lblInfo"))
        self.verticalLayout.addWidget(self.lblInfo)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.progressBar = QtGui.QProgressBar(frmScan)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setFormat(_fromUtf8(""))
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnBack = QtGui.QPushButton(frmScan)
        self.btnBack.setObjectName(_fromUtf8("btnBack"))
        self.horizontalLayout.addWidget(self.btnBack)
        self.btnStop = QtGui.QPushButton(frmScan)
        self.btnStop.setObjectName(_fromUtf8("btnStop"))
        self.horizontalLayout.addWidget(self.btnStop)
        self.btnScan = QtGui.QPushButton(frmScan)
        self.btnScan.setObjectName(_fromUtf8("btnScan"))
        self.horizontalLayout.addWidget(self.btnScan)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(frmScan)
        QtCore.QMetaObject.connectSlotsByName(frmScan)

    def retranslateUi(self, frmScan):
        frmScan.setWindowTitle(QtGui.QApplication.translate("frmScan", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBack.setText(QtGui.QApplication.translate("frmScan", "Volver", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStop.setText(QtGui.QApplication.translate("frmScan", "Detener", None, QtGui.QApplication.UnicodeUTF8))
        self.btnScan.setText(QtGui.QApplication.translate("frmScan", "Comenzar", None, QtGui.QApplication.UnicodeUTF8))

