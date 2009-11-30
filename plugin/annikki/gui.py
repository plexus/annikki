from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog, QDesktopServices
from PyQt4.QtCore import QUrl

import uic
import ankiqt
from ankiqt import mw

class ConfigDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.window = uic.Ui_ConfigAnnikkiDialog()
        self.window.setupUi(self)
        self.config = mw.config
        if self.config.has_key('annikki.username'):
            self.window.usernameEdit.setText(self.config['annikki.username'])
        if self.config.has_key('annikki.password'):
            self.window.passwordEdit.setText(self.config['annikki.password'])
        self.show()

    def accept(self):
        self.config['annikki.username'] = self.window.usernameEdit.text()
        self.config['annikki.password'] = self.window.passwordEdit.text()
        self.config.save()
        self.done(0)

    def reject(self):
        self.accept()

    def helpRequested(self):
        QDesktopServices.openUrl(QUrl(ankiqt.appWiki +
                                      "AnnikkiPreferences"))
