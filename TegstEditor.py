import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class Notepad(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.current_font_size = 12  # Starting font size
        self.current_cursive_checkbox = False  # Starting cursive checkbox state
        self.current_bold_checkbox = False  # Starting bold checkbox state

        self.main_layout = QVBoxLayout()

        self.font_list_layout = QHBoxLayout()

        self.options_layout = QGridLayout()
        self.options_buttons_layout = QVBoxLayout()
        self.text_size_layout = QVBoxLayout()
        self.cursive_layout = QVBoxLayout()
        self.bold_layout = QVBoxLayout()

        self.textbox_layout = QHBoxLayout()

        self.textbox = QTextEdit()
        self.font_list = QListWidget()
        # Font size label and lineEdit
        self.text_size_label = QLabel()
        self.text_size = QLineEdit()
        # Cursive label and lineEdit
        self.cursive_label = QLabel()
        self.cursive_checkbox = QCheckBox()
        # Bold label and lineEdit
        self.bold_label = QLabel()
        self.bold_checkbox = QCheckBox()

        self.create_textbox()
        self.create_font_list()
        self.create_save_button()
        self.create_load_button()
        self.create_text_size_field()
        self.create_cursive_checkbox()
        self.create_bold_checkbox()

        self.options_layout.addLayout(self.text_size_layout, 2, 0)
        self.options_layout.addLayout(self.cursive_layout, 2, 1)
        self.options_layout.addLayout(self.bold_layout, 2, 2)
        self.options_layout.addLayout(self.options_buttons_layout, 1, 1)
        self.options_layout.addLayout(self.font_list_layout, 1, 0)
        self.main_layout.addLayout(self.options_layout, 0)
        self.main_layout.addLayout(self.textbox_layout, 1)

        self.setLayout(self.main_layout)
        self.update()

    def create_textbox(self):
        self.textbox.move(20, 20)
        self.textbox.resize(280, 200)
        self.textbox_layout.addWidget(self.textbox)
        self.textbox.setFontPointSize(self.current_font_size)

    def create_cursive_checkbox(self):
        self.cursive_label.setText("Cursive")
        self.cursive_layout.addWidget(self.cursive_label)
        self.cursive_layout.addWidget(self.cursive_checkbox)

    def create_bold_checkbox(self):
        self.bold_label.setText("Bold")
        self.bold_layout.addWidget(self.bold_label)
        self.bold_layout.addWidget(self.bold_checkbox)

    def create_font_list(self):
        self.font_list.insertItems(0, QFontDatabase().families())
        self.font_list.clicked.connect(self.set_font)
        self.font_list_layout.addWidget(self.font_list)
        self.font_list_layout.setAlignment(self.font_list, Qt.AlignLeft)

    def set_font(self):
        self.textbox.setFontFamily(self.font_list.currentItem().text())

    def create_text_size_field(self):
        self.text_size_label.setText("Font Size")
        self.text_size_layout.addWidget(self.text_size_label)
        self.text_size_layout.addWidget(self.text_size)
        self.text_size.setText(str(self.current_font_size))

    def set_cursive(self):
        if self.cursive_checkbox.isChecked() != self.current_cursive_checkbox:
            if self.cursive_checkbox.isChecked():
                self.textbox.setFontItalic(True)
                self.current_cursive_checkbox = True
            else:
                self.textbox.setFontItalic(False)
                self.current_cursive_checkbox = False

    def set_bold(self):
        if self.bold_checkbox.isChecked() != self.current_bold_checkbox:
            if self.bold_checkbox.isChecked():
                self.textbox.setFontWeight(QFont.Bold)
                self.current_bold_checkbox = True
            else:
                self.textbox.setFontWeight(QFont.Normal)
                self.current_bold_checkbox = False

    def set_font_formatting(self):
        self.set_font_size()
        self.set_cursive()
        self.set_bold()

    def set_font_size(self):
        if self.text_size.text() is not "":
            try:
                set_text_size = float(self.text_size.text())
                if set_text_size != float(self.current_font_size):
                    if set_text_size > 100:
                        set_text_size = 100
                        self.text_size.setText(str(set_text_size))
                    elif set_text_size < 1:
                        set_text_size = 1
                        self.text_size.setText(str(set_text_size))
                    self.textbox.setFontPointSize(set_text_size)
                    self.current_font_size = set_text_size
            except ValueError as er:
                pass

    def create_save_button(self):
        button = QPushButton("Save")
        self.options_buttons_layout.addWidget(button)
        button.clicked.connect(self.save)
        self.options_buttons_layout.setAlignment(button, Qt.AlignRight)

    def create_load_button(self):
        button = QPushButton("Load")
        self.options_buttons_layout.addWidget(button)
        button.clicked.connect(self.load)
        self.options_buttons_layout.setAlignment(button, Qt.AlignRight)

    def save(self):
        t = self.textbox.toHtml()
        save_location = QFileDialog.getSaveFileName(self, "Save Text", QDir.currentPath(), "Html files (*.html)")
        file = open(save_location[0], "w+")
        file.write(t)
        file.close()

    def load(self):
        save_location = QFileDialog.getOpenFileName(self, "Open Text", QDir.currentPath(),
                                                    "Html files (*.html);;Text files (*.txt)")
        file = open(save_location[0], "r")
        self.textbox.setText(file.read())
        # Focus on the textbox and ready the cursor on 'after' the last element
        self.textbox.setFocus()
        self.textbox.moveCursor(QTextCursor.End)
        print(self.textbox.fontPointSize())
        # Set the properties of the widget so they last those of the last element in the textbox
        self.text_size.setText(str(self.textbox.fontPointSize()))
        if (self.textbox.fontWeight() == QFont.Bold):
            self.bold_checkbox.setChecked(True)
        else:
            self.bold_checkbox.setChecked(False)
        if (self.textbox.fontItalic() == True):
            self.cursive_checkbox.setChecked(True)
        else:
            self.cursive_checkbox.setChecked(False)


def main():
    app = QApplication(sys.argv)
    widget = Notepad()
    widget.resize(800, 600)
    widget.setWindowTitle("Notepad, TouwaStar")
    widget.show()

    timer = QTimer()
    timer.timeout.connect(widget.set_font_formatting)
    timer.start(100)

    sys.exit(app.exec_())


main()
