test_linux:
	python src/huayra-tda-player

ui:
	pyuic4 src/ui/player.ui > src/ui/Ui_frmPlayer.py
	pyuic4 src/ui/about.ui > src/ui/Ui_frmAbout.py
	pyuic4 src/ui/scan_channels.ui > src/ui/Ui_frmScanChannels.py
