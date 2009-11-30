from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog, QDesktopServices
from PyQt4.QtCore import QUrl

import uic
import ankiqt
from ankiqt import mw

class ConfigDialog(QDialog):
    def __init__(self, config):
        QDialog.__init__(self)
        self.window = uic.Ui_ConfigAnnikkiDialog()
        self.window.setupUi(self)
        self.config = config
        if self.config.username:
            self.window.usernameEdit.setText(self.config.username)
        if self.config.password:
            self.window.passwordEdit.setText(self.config.password)
        self.show()

    def accept(self):
        self.config.username = str(self.window.usernameEdit.text())
        self.config.password = str(self.window.passwordEdit.text())
        self.config.save()
        self.done(0)

    def reject(self):
        self.accept()

    def helpRequested(self):
        QDesktopServices.openUrl(QUrl(ankiqt.appWiki +
                                      "AnnikkiPreferences"))
