from PyQt6.QtGui import QDoubleValidator, QFont
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from . import core
from . import notificator


def clear_layout(layout):
    if layout:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clear_layout(item.layout())


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        cfg = core.container.cfg

        self.notifier = core.container.notifier()
        self.main_layout = QVBoxLayout(self)

        self.setStyleSheet("background-color: #101010")

        scroll_area = QScrollArea(self)
        scroll_area.setObjectName("ScrollArea")
        scroll_area.setStyleSheet("#ScrollArea {border: 0px solid black}")
        scroll_area.setWidget(ViewFrame(self))
        scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(scroll_area)
        self.setLayout(self.main_layout)
        self.resize(cfg.window.open_width(), cfg.window.open_height())
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        render_cfg = core.container.cfg.render.main_window
        # self.setStyleSheet(f"background-color:{render_cfg.background_color()}")

    def keyPressEvent(self, event):
        modifier = ''
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            modifier += 'Ctrl+'
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            modifier += 'Shift+'
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            modifier += 'Alt+'

        # key = event.text().upper()
        # if not key:
        key = Qt.Key(event.key()).name

        notification = notificator.Notification(notificator.Messages.key_event)
        notification.key = f"{modifier}{key}"
        self.notifier.notify(notification)

        super().keyPressEvent(event)


# self.model = core.container.model()


class ViewFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = core.container.model()
        self.init_ui()

    def init_ui(self):
        self.custom_layout = QVBoxLayout()

        self.custom_layout.setSpacing(0)
        self.custom_layout.setContentsMargins(0, 0, 0, 0)

        self.custom_layout.addStretch()

        for record in self.model.records():
            record_frame = RecordFrame(record)
            self.custom_layout.addWidget(record_frame)

        self.custom_layout.addStretch()
        self.setLayout(self.custom_layout)


class RecordFrame(QFrame):
    def __init__(self, record, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.record = record
        self.model = core.container.model()
        self.init_ui()

    def init_ui(self):
        self.custom_layout = QVBoxLayout()

        self.custom_layout.setSpacing(0)
        self.custom_layout.setContentsMargins(0, 10, 0, 30)

        tags = TagsFrame(self.record.tags)
        text = TextFrame(self.record.text)

        self.custom_layout.addWidget(tags)
        self.custom_layout.addWidget(text)

        self.setLayout(self.custom_layout)

        self.setObjectName("RecordFrame")

        self.setStyleSheet(
                "#RecordFrame {"
                "  background-color: #101010; " 
                "  border-bottom: 3px solid #1E1E1E; " 
                "}"
            )


class TagsFrame(QFrame):
    def __init__(self, tags, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = core.container.model()
        self.tags = tags
        self.init_ui()

    def init_ui(self):
        self.custom_layout = QVBoxLayout()

        self.custom_layout.setSpacing(0)
        self.custom_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("        ".join(self.tags))
        label.setWordWrap(True)

        # label.setStyleSheet("color: #1E8BF7; font-size: 10px")
        label.setStyleSheet("color: #A9A9A9; font-size: 11px")

        self.custom_layout.addWidget(label)
        self.setLayout(self.custom_layout)


class TextFrame(QFrame):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = core.container.model()
        self.text = text
        self.init_ui()

    def init_ui(self):
        self.custom_layout = QVBoxLayout()

        self.custom_layout.setSpacing(0)
        self.custom_layout.setContentsMargins(0, 15, 0, 0)

        label = QLabel("\n".join(self.text))

        label.setStyleSheet("color: #F7A11E; font-size: 14px")

        self.custom_layout.addWidget(label)
        self.setLayout(self.custom_layout)