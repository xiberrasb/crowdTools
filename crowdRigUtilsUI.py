import maya.OpenMayaUI as omui
from PySide import QtCore, QtGui
from shiboken import wrapInstance
import crowdRigUtils as cru

try :
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError :
	def _fromUtf8(s) :
		return s
try :
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig) :
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError :
	def _translate(context, text, disambig) :
		return QtGui.QApplication.translate(context, text, disambig)


class Ui_CrowdRigTools_Dg(object) :
	def setupUi(self, CrowdRigTools_Dg) :
		CrowdRigTools_Dg.setObjectName(_fromUtf8("CrowdRigTools_Dg"))
		CrowdRigTools_Dg.resize(180, 152)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(CrowdRigTools_Dg.sizePolicy().hasHeightForWidth())
		CrowdRigTools_Dg.setSizePolicy(sizePolicy)
		CrowdRigTools_Dg.setMaximumSize(QtCore.QSize(180, 152))
		self.gridLayout = QtGui.QGridLayout(CrowdRigTools_Dg)
		self.gridLayout.setContentsMargins(0, -1, 0, -1)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
		self.buttonBox = QtGui.QDialogButtonBox(CrowdRigTools_Dg)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
		self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)
		self.DeleteCrowdRig_Btn = QtGui.QPushButton(CrowdRigTools_Dg)
		self.DeleteCrowdRig_Btn.setObjectName(_fromUtf8("DeleteCrowdRig_Btn"))
		self.gridLayout.addWidget(self.DeleteCrowdRig_Btn, 4, 1, 1, 1)
		self.CreateRig_Btn = QtGui.QPushButton(CrowdRigTools_Dg)
		self.CreateRig_Btn.setObjectName(_fromUtf8("CreateRig_Btn"))
		self.gridLayout.addWidget(self.CreateRig_Btn, 0, 1, 1, 1)
		self.ConnectJoints_Btn = QtGui.QPushButton(CrowdRigTools_Dg)
		self.ConnectJoints_Btn.setObjectName(_fromUtf8("ConnectJoints_Btn"))
		self.gridLayout.addWidget(self.ConnectJoints_Btn, 1, 1, 1, 1)
		self.DisconnectJoints_Btn = QtGui.QPushButton(CrowdRigTools_Dg)
		self.DisconnectJoints_Btn.setObjectName(_fromUtf8("DisconnectJoints_Btn"))
		self.gridLayout.addWidget(self.DisconnectJoints_Btn, 3, 1, 1, 1)
		spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)

		self.retranslateUi(CrowdRigTools_Dg)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CrowdRigTools_Dg.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CrowdRigTools_Dg.reject)
		QtCore.QObject.connect(self.CreateRig_Btn, QtCore.SIGNAL(_fromUtf8("released()")), CrowdRigTools_Dg.update)
		QtCore.QObject.connect(self.ConnectJoints_Btn, QtCore.SIGNAL(_fromUtf8("released()")), CrowdRigTools_Dg.update)
		QtCore.QObject.connect(self.DeleteCrowdRig_Btn, QtCore.SIGNAL(_fromUtf8("released()")), CrowdRigTools_Dg.update)
		QtCore.QObject.connect(self.DisconnectJoints_Btn, QtCore.SIGNAL(_fromUtf8("released()")),
							   CrowdRigTools_Dg.update)
		QtCore.QMetaObject.connectSlotsByName(CrowdRigTools_Dg)

	def retranslateUi(self, CrowdRigTools_Dg) :
		CrowdRigTools_Dg.setWindowTitle(_translate("CrowdRigTools_Dg", "Crowd Rig Tools", None))
		self.DeleteCrowdRig_Btn.setText(_translate("CrowdRigTools_Dg", "Delete Crowd Rig", None))
		self.CreateRig_Btn.setText(_translate("CrowdRigTools_Dg", "Create Crowd Rig", None))
		self.DisconnectJoints_Btn.setText(_translate("CrowdRigTools_Dg", "Disconnect joints", None))
		self.ConnectJoints_Btn.setText(_translate("CrowdRigTools_Dg", "Connect Joints", None))


class ControlMainWindow(QtGui.QDialog) :
	def confirm(self) :
		msg = "Are you sure?"
		reply = QtGui.QMessageBox.question(self, 'Message', msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes :
			cru.deletecrowdrig()
		else :
			pass

	def __init__(self, parent = None) :
		super(ControlMainWindow, self).__init__(parent)
		self.setWindowFlags(QtCore.Qt.Tool)
		self.ui = Ui_CrowdRigTools_Dg()
		self.ui.setupUi(self)

		self.ui.CreateRig_Btn.released.connect(cru.createcrowdrig)
		self.ui.ConnectJoints_Btn.released.connect(cru.connectjoints)
		self.ui.DeleteCrowdRig_Btn.released.connect(cru.confirm)
		self.ui.DisconnectJoints_Btn.released.connect(cru.disconnectjoints)


def maya_main_window() :
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window_ptr), QtGui.QWidget)


myWin = ControlMainWindow(parent=maya_main_window())
myWin.show()