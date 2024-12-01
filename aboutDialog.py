from PySide6.QtGui import QColor,  QColorConstants
from PySide6.QtWidgets import (
    QDialog,
    QStyle,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDialogButtonBox)

class AboutDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle('Info')
        self.resize(300, 200)

        self.setModal(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(),
                         QColor(QColorConstants.Svg.paleturquoise))
        self.setPalette(palette)
        vLayout = QVBoxLayout()

        label = QLabel('''App Diashow 1.0\n
                       MIT License\n
                       © 2024 Boris M. Gelder\n
                       https://github.com/bmgelder/diashow.git\n\n
                       Icons copied from https://icons8.de/ and\n
                       https://p.yusukekamiyamane.com/\n''')
        vLayout.addWidget(label)

        buttonBox = QDialogButtonBox(self)
        buttonBox.addButton('OK', QDialogButtonBox.AcceptRole)
        buttonBox.accepted.connect(self.accept)

        vLayout.addWidget(buttonBox)

        self.setLayout(vLayout)
