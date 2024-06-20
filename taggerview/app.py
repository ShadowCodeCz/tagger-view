import json
import os
import ctypes
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import *

# import app_core
import qdarktheme
import datetime

from . import core
from . import gui
from . import notificator
import apphelpers as app_helpers


class ApplicationCLI:
    @staticmethod
    def run(arguments):
        cfg = core.container.cfg
        # cfg.from_json(app_helpers.cli_arguments_to_dict(arguments))

        cfg_dict = read_json(arguments.configuration)
        cfg_dict["noter_file"] = arguments.noter_file
        cfg.from_dict(cfg_dict)

        print(cfg())
        app = Application()
        app.run()

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

class Controller:
    def __init__(self):
        self.notifier = core.container.notifier()


class Application:
    def __init__(self, logger=core.container.logger()):
        self.app = None
        self.logger = logger
        self.window = None
        self.arguments = None
        self.controller = Controller()

    def run(self):
        self.app = QApplication([])
        qdarktheme.setup_theme(corner_shape="sharp")
        self.window = gui.MainWindow()
        self.window.setWindowTitle(f"Template Gui App")
        self.set_logo()

        self.window.show()
        self.app.exec()

    def set_logo(self):
        my_app_id = f'shadowcode.{core.container.app_description().name}.0.1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
        path = os.path.join(core.container.package_paths().image_directory(), 'logo.png')
        self.window.setWindowIcon(QIcon(path))
        self.app.setWindowIcon(QIcon(path))



