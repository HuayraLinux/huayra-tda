# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player.ui'
#
# Created: Mon Jun  2 13:44:14 2014
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
        frmPlayer.setEnabled(True)
        frmPlayer.resize(591, 458)
        frmPlayer.setMaximumSize(QtCore.QSize(100000, 100000))
        frmPlayer.setToolTip(_fromUtf8(""))
        frmPlayer.setAutoFillBackground(False)
        frmPlayer.setStyleSheet(_fromUtf8("QWidget#frmPlayer{\n"
"background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f8f8f8, stop: 0.3 #f1f1f1, stop: 1 #e8e8e8);\n"
"\n"
"}\n"
"\n"
"#layoutVideo{\n"
"    border: 1px solid #e9e9e9;\n"
"    border-radius:6px;\n"
"}\n"
"\n"
"#sldVolume::groove:horizontal {\n"
"     border: 1px solid #b1b1b1;\n"
"    height: 12px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
"   background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);\n"
"   position: absolute;\n"
"    left:4px; right:4px;\n"
"    border-radius: 5px;\n"
" }\n"
"\n"
"#sldVolume::handle:horizontal {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2b4040, stop:0.8 #4bd0d3, stop:1 #86F9FF);\n"
"    /*image: url(\"./imagenes/handle.png\");*/\n"
"/*    background-image: url(\"./imagenes/handle.svg\");*/\n"
"     border: 1px solid #7c7c7c;\n"
"     width: 12px;\n"
"    height:12px;\n"
"     margin: 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"     border-radius: 5px;\n"
" }\n"
"\n"
"#sldVolume::add-page:horizontal { /* color del slider ANTES que pase el handle*/\n"
"     background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #808080, stop:1 #c4c4c4);\n"
"    padding: 2px;\n"
"    margin: 2px;\n"
"    border-radius: 5px;\n"
"    /*border: 1px solid #5c5c5c;*/\n"
" }\n"
"\n"
"#sldVolume::sub-page:horizontal {/* color del slider DESPUES que pase el handle*/\n"
"     background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4bd0d3, stop:0.2 #3b9b9e, stop:0.8 #4bd0d3, stop:1 #2b4040);\n"
"    /*border:1px solid #5c5c5c;*/\n"
"    border-radius: 5px;\n"
"    padding: 2px;\n"
"    margin: 2px;\n"
" }\n"
"\n"
"#listViewChannels{\n"
"    background-image:url(\"./imagenes/vaca.svg\");\n"
"}\n"
"\n"
"QPushButton{\n"
"    border: 1px solid #c1c1c1;\n"
"    border-radius:6px;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f8f8f8, stop: 0.3 #f1f1f1, stop: 1 #e8e8e8);\n"
"    margin: 2px;\n"
"    padding: 2px;\n"
"    min-width: 24px;\n"
"    min-height: 18px;\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(frmPlayer)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.layoutVideo = QtGui.QHBoxLayout()
        self.layoutVideo.setSpacing(0)
        self.layoutVideo.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.layoutVideo.setContentsMargins(-1, 0, -1, -1)
        self.layoutVideo.setObjectName(_fromUtf8("layoutVideo"))
        spacerItem = QtGui.QSpacerItem(0, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.layoutVideo.addItem(spacerItem)
        self.verticalLayout.addLayout(self.layoutVideo)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnChannelDown = QtGui.QPushButton(frmPlayer)
        self.btnChannelDown.setMaximumSize(QtCore.QSize(32, 32))
        self.btnChannelDown.setStyleSheet(_fromUtf8("color: rgb(125, 60, 255);"))
        self.btnChannelDown.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../usr/share/icons/huayra-limbo/scalable/actions/down.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnChannelDown.setIcon(icon)
        self.btnChannelDown.setIconSize(QtCore.QSize(16, 16))
        self.btnChannelDown.setObjectName(_fromUtf8("btnChannelDown"))
        self.horizontalLayout.addWidget(self.btnChannelDown)
        self.btnChannelUp = QtGui.QPushButton(frmPlayer)
        self.btnChannelUp.setMaximumSize(QtCore.QSize(32, 32))
        self.btnChannelUp.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../usr/share/icons/huayra-limbo/scalable/actions/up.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnChannelUp.setIcon(icon1)
        self.btnChannelUp.setIconSize(QtCore.QSize(16, 16))
        self.btnChannelUp.setObjectName(_fromUtf8("btnChannelUp"))
        self.horizontalLayout.addWidget(self.btnChannelUp)
        self.lblVolumen = QtGui.QLabel(frmPlayer)
        self.lblVolumen.setText(_fromUtf8(""))
        self.lblVolumen.setPixmap(QtGui.QPixmap(_fromUtf8("imagenes/volumen.svg")))
        self.lblVolumen.setObjectName(_fromUtf8("lblVolumen"))
        self.horizontalLayout.addWidget(self.lblVolumen)
        self.sldVolume = QtGui.QSlider(frmPlayer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sldVolume.sizePolicy().hasHeightForWidth())
        self.sldVolume.setSizePolicy(sizePolicy)
        self.sldVolume.setMaximumSize(QtCore.QSize(700, 16777215))
        self.sldVolume.setMaximum(100)
        self.sldVolume.setOrientation(QtCore.Qt.Horizontal)
        self.sldVolume.setObjectName(_fromUtf8("sldVolume"))
        self.horizontalLayout.addWidget(self.sldVolume)
        self.lblVolumenVal = QtGui.QLabel(frmPlayer)
        self.lblVolumenVal.setObjectName(_fromUtf8("lblVolumenVal"))
        self.horizontalLayout.addWidget(self.lblVolumenVal)
        spacerItem1 = QtGui.QSpacerItem(40, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnShowChannelsList = QtGui.QPushButton(frmPlayer)
        self.btnShowChannelsList.setMaximumSize(QtCore.QSize(30, 32))
        self.btnShowChannelsList.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../usr/share/icons/huayra-limbo/scalable/actions/top.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnShowChannelsList.setIcon(icon2)
        self.btnShowChannelsList.setIconSize(QtCore.QSize(16, 16))
        self.btnShowChannelsList.setObjectName(_fromUtf8("btnShowChannelsList"))
        self.horizontalLayout.addWidget(self.btnShowChannelsList)
        self.btnFullScreen = QtGui.QPushButton(frmPlayer)
        self.btnFullScreen.setMaximumSize(QtCore.QSize(32, 32))
        self.btnFullScreen.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../usr/share/icons/huayra-limbo/scalable/actions/view-fullscreen.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnFullScreen.setIcon(icon3)
        self.btnFullScreen.setIconSize(QtCore.QSize(16, 16))
        self.btnFullScreen.setObjectName(_fromUtf8("btnFullScreen"))
        self.horizontalLayout.addWidget(self.btnFullScreen)
        self.lblHuayra = QtGui.QLabel(frmPlayer)
        self.lblHuayra.setMinimumSize(QtCore.QSize(20, 20))
        self.lblHuayra.setMaximumSize(QtCore.QSize(24, 24))
        self.lblHuayra.setText(_fromUtf8(""))
        self.lblHuayra.setPixmap(QtGui.QPixmap(_fromUtf8("imagenes/huayra-tda.svg")))
        self.lblHuayra.setScaledContents(False)
        self.lblHuayra.setObjectName(_fromUtf8("lblHuayra"))
        self.horizontalLayout.addWidget(self.lblHuayra)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listViewChannels = QtGui.QListView(frmPlayer)
        self.listViewChannels.setEnabled(True)
        self.listViewChannels.setMaximumSize(QtCore.QSize(16777215, 200))
        self.listViewChannels.setAutoFillBackground(False)
        self.listViewChannels.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listViewChannels.setObjectName(_fromUtf8("listViewChannels"))
        self.verticalLayout.addWidget(self.listViewChannels)

        self.retranslateUi(frmPlayer)
        QtCore.QMetaObject.connectSlotsByName(frmPlayer)

    def retranslateUi(self, frmPlayer):
        frmPlayer.setWindowTitle(QtGui.QApplication.translate("frmPlayer", "Huayra - Television Digital Abierta ", None, QtGui.QApplication.UnicodeUTF8))
        self.btnChannelDown.setToolTip(QtGui.QApplication.translate("frmPlayer", "Canal Abajo", None, QtGui.QApplication.UnicodeUTF8))
        self.btnChannelUp.setToolTip(QtGui.QApplication.translate("frmPlayer", "Canal Arriba", None, QtGui.QApplication.UnicodeUTF8))
        self.lblVolumen.setToolTip(QtGui.QApplication.translate("frmPlayer", "Volumen", None, QtGui.QApplication.UnicodeUTF8))
        self.sldVolume.setToolTip(QtGui.QApplication.translate("frmPlayer", "Control de volumen", None, QtGui.QApplication.UnicodeUTF8))
        self.lblVolumenVal.setText(QtGui.QApplication.translate("frmPlayer", "30%", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFullScreen.setToolTip(QtGui.QApplication.translate("frmPlayer", "Pantalla Completa", None, QtGui.QApplication.UnicodeUTF8))

