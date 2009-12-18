# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/config.ui'
#
# Created: Thu Dec 17 16:22:30 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ConfigAnnikkiDialog(object):
    def setupUi(self, ConfigAnnikkiDialog):
        ConfigAnnikkiDialog.setObjectName("ConfigAnnikkiDialog")
        ConfigAnnikkiDialog.resize(302, 146)
        self.verticalLayoutWidget = QtGui.QWidget(ConfigAnnikkiDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 281, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.usernameEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.usernameEdit.setObjectName("usernameEdit")
        self.horizontalLayout.addWidget(self.usernameEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(70, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.passwordEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.horizontalLayout_4.addWidget(self.passwordEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.buttonBox = QtGui.QDialogButtonBox(ConfigAnnikkiDialog)
        self.buttonBox.setGeometry(QtCore.QRect(8, 110, 281, 25))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Help)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(ConfigAnnikkiDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ConfigAnnikkiDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ConfigAnnikkiDialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("helpRequested()"), ConfigAnnikkiDialog.helpRequested)
        QtCore.QMetaObject.connectSlotsByName(ConfigAnnikkiDialog)

    def retranslateUi(self, ConfigAnnikkiDialog):
        ConfigAnnikkiDialog.setWindowTitle(QtGui.QApplication.translate("ConfigAnnikkiDialog", "Annikki Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ConfigAnnikkiDialog", "<b>Annikki.org login</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ConfigAnnikkiDialog", "<a href=\"http://www.annikki.org/signup\">Sign up!</a>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ConfigAnnikkiDialog", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ConfigAnnikkiDialog", "Password", None, QtGui.QApplication.UnicodeUTF8))

