# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'correctiveTool_v1.0_01.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(471, 741)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 10, 411, 721))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setObjectName("gridLayout")
        self.oriGeo_Label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.oriGeo_Label_2.setObjectName("oriGeo_Label_2")
        self.gridLayout.addWidget(self.oriGeo_Label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.baseGeo_Label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.baseGeo_Label_2.setObjectName("baseGeo_Label_2")
        self.gridLayout.addWidget(self.baseGeo_Label_2, 0, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 2, 1, 1, 5)
        self.oriGeo_Btn_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.oriGeo_Btn_2.setStyleSheet("background-color:rgb(142,188,255);color:black;")
        self.oriGeo_Btn_2.setObjectName("oriGeo_Btn_2")
        self.gridLayout.addWidget(self.oriGeo_Btn_2, 1, 5, 1, 1)
        self.baseGeo_Btn_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.baseGeo_Btn_2.setStyleSheet("background-color:rgb(142,188,255);color:black;")
        self.baseGeo_Btn_2.setObjectName("baseGeo_Btn_2")
        self.gridLayout.addWidget(self.baseGeo_Btn_2, 0, 5, 1, 1)
        self.baseGeo_LineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.baseGeo_LineEdit_2.setObjectName("baseGeo_LineEdit_2")
        self.gridLayout.addWidget(self.baseGeo_LineEdit_2, 0, 1, 1, 4)
        self.oriGeo_LineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.oriGeo_LineEdit_2.setObjectName("oriGeo_LineEdit_2")
        self.gridLayout.addWidget(self.oriGeo_LineEdit_2, 1, 1, 1, 4)
        self.pushButton_14 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_14.setStyleSheet("background-color:rgb(142,188,255);color:black;")
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout.addWidget(self.pushButton_14, 3, 5, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_10.setStyleSheet("background-color:rgb(142,188,255);color:black;")
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 3, 4, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.line = QtWidgets.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_5.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.radioButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_2.setEnabled(False)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_2.addWidget(self.radioButton_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_5.addWidget(self.line_2)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setSpacing(7)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.tabWidget = QtWidgets.QTabWidget(self.layoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.layoutWidget1 = QtWidgets.QWidget(self.tab)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 0, 404, 451))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_12.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_12.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_12.setSpacing(3)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.pushButton_30 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_30.setStyleSheet("background-color:rgb(142,188,255);color:black;")
        self.pushButton_30.setObjectName("pushButton_30")
        self.verticalLayout_12.addWidget(self.pushButton_30)
        self.splitter_4 = QtWidgets.QSplitter(self.layoutWidget1)
        self.splitter_4.setMinimumSize(QtCore.QSize(400, 0))
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.listWidget_14 = QtWidgets.QListWidget(self.splitter_4)
        self.listWidget_14.setObjectName("listWidget_14")
        self.listWidget_15 = QtWidgets.QListWidget(self.splitter_4)
        self.listWidget_15.setObjectName("listWidget_15")
        self.verticalLayout_12.addWidget(self.splitter_4)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.layoutWidget_7 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget_7.setGeometry(QtCore.QRect(0, 0, 404, 451))
        self.layoutWidget_7.setObjectName("layoutWidget_7")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.layoutWidget_7)
        self.verticalLayout_14.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_14.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_14.setSpacing(3)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.pushButton_32 = QtWidgets.QPushButton(self.layoutWidget_7)
        self.pushButton_32.setStyleSheet("background-color:rgb(142,188,255);color:black;")
        self.pushButton_32.setObjectName("pushButton_32")
        self.verticalLayout_14.addWidget(self.pushButton_32)
        self.splitter_9 = QtWidgets.QSplitter(self.layoutWidget_7)
        self.splitter_9.setMinimumSize(QtCore.QSize(400, 0))
        self.splitter_9.setOrientation(QtCore.Qt.Vertical)
        self.splitter_9.setObjectName("splitter_9")
        self.listWidget_24 = QtWidgets.QListWidget(self.splitter_9)
        self.listWidget_24.setObjectName("listWidget_24")
        self.listWidget_25 = QtWidgets.QListWidget(self.splitter_9)
        self.listWidget_25.setObjectName("listWidget_25")
        self.verticalLayout_14.addWidget(self.splitter_9)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.layoutWidget_6 = QtWidgets.QWidget(self.tab_3)
        self.layoutWidget_6.setGeometry(QtCore.QRect(0, 0, 404, 451))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.layoutWidget_6)
        self.verticalLayout_13.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_13.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_13.setSpacing(3)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.pushButton_31 = QtWidgets.QPushButton(self.layoutWidget_6)
        self.pushButton_31.setStyleSheet("background-color:rgb(142,188,255);color:black;")
        self.pushButton_31.setObjectName("pushButton_31")
        self.verticalLayout_13.addWidget(self.pushButton_31)
        self.splitter_5 = QtWidgets.QSplitter(self.layoutWidget_6)
        self.splitter_5.setMinimumSize(QtCore.QSize(400, 0))
        self.splitter_5.setOrientation(QtCore.Qt.Vertical)
        self.splitter_5.setObjectName("splitter_5")
        self.listWidget_16 = QtWidgets.QListWidget(self.splitter_5)
        self.listWidget_16.setObjectName("listWidget_16")
        self.listWidget_17 = QtWidgets.QListWidget(self.splitter_5)
        self.listWidget_17.setObjectName("listWidget_17")
        self.verticalLayout_13.addWidget(self.splitter_5)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.layoutWidget2 = QtWidgets.QWidget(self.tab_4)
        self.layoutWidget2.setGeometry(QtCore.QRect(0, 0, 404, 451))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_4.setStyleSheet("background-color:rgb(142,188,255);color:black;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.pushButton_4)
        self.splitter_3 = QtWidgets.QSplitter(self.layoutWidget2)
        self.splitter_3.setMinimumSize(QtCore.QSize(400, 0))
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.listWidget_12 = QtWidgets.QListWidget(self.splitter_3)
        self.listWidget_12.setObjectName("listWidget_12")
        self.listWidget_13 = QtWidgets.QListWidget(self.splitter_3)
        self.listWidget_13.setObjectName("listWidget_13")
        self.verticalLayout_4.addWidget(self.splitter_3)
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout_11.addWidget(self.tabWidget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_6.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_6.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_6.addWidget(self.lineEdit_3)
        self.verticalLayout_11.addLayout(self.horizontalLayout_6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_11 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout.addWidget(self.pushButton_11)
        self.pushButton_12 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_12.setObjectName("pushButton_12")
        self.horizontalLayout.addWidget(self.pushButton_12)
        self.pushButton_13 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout.addWidget(self.pushButton_13)
        self.verticalLayout_11.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_11.addWidget(self.label)
        self.verticalLayout_5.addLayout(self.verticalLayout_11)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.oriGeo_Label_2.setText(_translate("Form", "Ori Geo:"))
        self.label_4.setText(_translate("Form", "blendShape:"))
        self.baseGeo_Label_2.setText(_translate("Form", "Base Geo:"))
        self.oriGeo_Btn_2.setText(_translate("Form", "Load"))
        self.baseGeo_Btn_2.setText(_translate("Form", "Load"))
        self.pushButton_14.setText(_translate("Form", "Del"))
        self.pushButton_10.setText(_translate("Form", "Add"))
        self.label_3.setText(_translate("Form", "Driver Type :"))
        self.radioButton.setText(_translate("Form", "ADV"))
        self.radioButton_2.setText(_translate("Form", "Defined"))
        self.pushButton_30.setText(_translate("Form", "Create Target"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Arm"))
        self.pushButton_32.setText(_translate("Form", "Create Target"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Leg"))
        self.pushButton_31.setText(_translate("Form", "Create Target"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Finger"))
        self.pushButton_4.setText(_translate("Form", "Create Target"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "torso"))
        self.label_7.setText(_translate("Form", "Rotate:"))
        self.pushButton_11.setText(_translate("Form", "Sculpt"))
        self.pushButton_12.setText(_translate("Form", "Mirror"))
        self.pushButton_13.setText(_translate("Form", "Exit"))
        self.label.setText(_translate("Form", "Copyright(C) 2022 Rigging | QBJ"))
