import json
import os
import datetime

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from PIL import ImageQt, Image

from . import core

import io


class Record:
    def __init__(self, tags, text):
        self.tags = tags
        self.text = text


class DataModel(QObject):
    # crop_rect_changed = pyqtSignal()
    # pixmap_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

    def load_noter_file(self):
        path = core.container.cfg.noter_file()
        with open(path, "r") as f:
            return json.load(f)

    def records(self):
        noter = self.load_noter_file()
        return [Record(item["tags"], item["text"]) for item in noter]