# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player.ui'
#
# Created: Fri Feb 28 16:00:00 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmPlayer(object):
    def setupUi(self, frmPlayer):
        frmPlayer.setObjectName(_fromUtf8("frmPlayer"))
        frmPlayer.resize(412, 270)
        self.verticalLayout = QtGui.QVBoxLayout(frmPlayer)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.layoutVideo = QtGui.QHBoxLayout()
        self.layoutVideo.setObjectName(_fromUtf8("layoutVideo"))
        self.verticalLayout.addLayout(self.layoutVideo)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnChannelDown = QtGui.QPushButton(frmPlayer)
        self.btnChannelDown.setObjectName(_fromUtf8("btnChannelDown"))
        self.horizontalLayout.addWidget(self.btnChannelDown)
        self.btnChannelUp = QtGui.QPushButton(frmPlayer)
        self.btnChannelUp.setObjectName(_fromUtf8("btnChannelUp"))
        self.horizontalLayout.addWidget(self.btnChannelUp)
        self.sldVolume = QtGui.QSlider(frmPlayer)
        self.sldVolume.setOrientation(QtCore.Qt.Horizontal)
        self.sldVolume.setObjectName(_fromUtf8("sldVolume"))
        self.horizontalLayout.addWidget(self.sldVolume)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(frmPlayer)
        QtCore.QMetaObject.connectSlotsByName(frmPlayer)

    def retranslateUi(self, frmPlayer):
        frmPlayer.setWindowTitle(QtGui.QApplication.translate("frmPlayer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btnChannelDown.setText(QtGui.QApplication.translate("frmPlayer", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.btnChannelUp.setText(QtGui.QApplication.translate("frmPlayer", "+", None, QtGui.QApplication.UnicodeUTF8))

