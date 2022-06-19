import sys
from ui_USB_Schluessel import Ui_MainWindow

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile

from cli import cli
from lib import CryptoUtils

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    cli_pars = cli.pars_args()
    # No CLI and GUI is started
    if cli_pars == None:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    # CLI
    elif cli_pars["err"] == False:
        #   print("Cli is not ready yet.")
        if cli_pars["is_encrypt_or_encrypt"]:
            CryptoUtils.encrypt(cli_pars["password_in"],
                                cli_pars["file_in_name"],
                                cli_pars["file_out_name"],
                                )
        else:
            CryptoUtils.decrypt(cli_pars["password_in"],
                                cli_pars["file_in_name"],
                                cli_pars["file_out_name"],
                                )
        print("Finish!")
        exit(0)
    # CLI Error
    else:
        exit(1)
        
