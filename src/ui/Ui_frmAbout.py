# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Mon Mar 17 14:52:17 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmAbout(object):
    def setupUi(self, frmAbout):
        frmAbout.setObjectName(_fromUtf8("frmAbout"))
        frmAbout.setWindowModality(QtCore.Qt.ApplicationModal)
        frmAbout.resize(708, 321)
        frmAbout.setModal(True)
        self.label = QtGui.QLabel(frmAbout)
        self.label.setGeometry(QtCore.QRect(340, 70, 361, 51))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(frmAbout)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 341, 311))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("imagenes/splash.png")))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(frmAbout)
        self.label_3.setGeometry(QtCore.QRect(340, 120, 361, 131))
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(frmAbout)
        QtCore.QMetaObject.connectSlotsByName(frmAbout)

    def retranslateUi(self, frmAbout):
        frmAbout.setWindowTitle(QtGui.QApplication.translate("frmAbout", "Acerca de Huayra TDA (Bebote V)", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmAbout", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; color:#737373;\">Huayra TDA </span></p><p align=\"center\"><span style=\" font-size:11pt; color:#737373;\">Sintonizador de Television Digital Abierta</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmAbout", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; color:#737373;\">Desarrollado por CENITAL para Conectar Igualdad</span></p><p align=\"center\"><span style=\" font-size:11pt; color:#737373;\">(c) 2014 Miguel García, Claudio Andaur</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

