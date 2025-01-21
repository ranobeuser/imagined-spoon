import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox, QRadioButton, QGroupBox, QHBoxLayout

class TextStylerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Стилевой редактор текста")

        self.layout = QVBoxLayout()


        self.label = QLabel("Примените стиль к этому тексту")
        self.layout.addWidget(self.label)

        self.color_combo = QComboBox()
        self.color_combo.addItems(["Черный", "Красный", "Зеленый", "Синий"])
        self.color_combo.currentIndexChanged.connect(self.update_text_style)
        self.layout.addWidget(self.color_combo)

        self.bold_checkbox = QCheckBox("Жирный")
        self.bold_checkbox.stateChanged.connect(self.update_text_style)
        self.layout.addWidget(self.bold_checkbox)

        self.italic_checkbox = QCheckBox("Курсив")
        self.italic_checkbox.stateChanged.connect(self.update_text_style)
        self.layout.addWidget(self.italic_checkbox)


        self.size_group = QGroupBox("Размер текста")
        self.size_layout = QHBoxLayout()

        self.size_small = QRadioButton("Маленький")
        self.size_medium = QRadioButton("Средний")
        self.size_large = QRadioButton("Большой")

        self.size_small.setChecked(True) 
        self.size_small.toggled.connect(self.update_text_style)
        self.size_medium.toggled.connect(self.update_text_style)
        self.size_large.toggled.connect(self.update_text_style)

        self.size_layout.addWidget(self.size_small)
        self.size_layout.addWidget(self.size_medium)
        self.size_layout.addWidget(self.size_large)
        self.size_group.setLayout(self.size_layout)
        self.layout.addWidget(self.size_group)

        self.setLayout(self.layout)

        self.update_text_style()  

    def update_text_style(self):

        color = self.color_combo.currentText().lower()

        if color == "черный":
            color = "black"
        elif color == "красный":
            color = "red"
        elif color == "зеленый":
            color = "green"
        elif color == "синий":
            color = "blue"


        font_weight = "normal"
        if self.bold_checkbox.isChecked():
            font_weight = "bold"
        font_italic = "italic" if self.italic_checkbox.isChecked() else "normal"


        font_size = 12
        if self.size_medium.isChecked():
            font_size = 16
        elif self.size_large.isChecked():
            font_size = 20

        self.label.setStyleSheet(f"color: {color}; font-weight: {font_weight}; font-style: {font_italic}; font-size: {font_size}px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextStylerApp()
    window.show()
    sys.exit(app.exec())
