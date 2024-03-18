from PySide6.QtGui import QColor,  QColorConstants
from PySide6.QtWidgets import (
    QDialog,
    QStyle,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDialogButtonBox)


class CancelNextDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle('Bildliste wurde verändert!')

        self.resize(500, 100)

        self.setModal(True)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(),
                         QColor(QColorConstants.LightGray))
        self.setPalette(palette)

        vLayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(self.style().standardIcon(
            QStyle.SP_MessageBoxQuestion).pixmap(32, 32))
        hlayout.addWidget(icon)

        hlayout.addWidget(
            QLabel('Die Bildliste wurde verändert. Möchten Sie die Änderungen verwerfen?'))
        vLayout.addLayout(hlayout)

        buttonBox = QDialogButtonBox(self)
        buttonBox.addButton(
            'Verwerfen', QDialogButtonBox.AcceptRole)
        buttonBox.accepted.connect(self.accept)

        rejectBtn = buttonBox.addButton(
            'Abbrechen', QDialogButtonBox.RejectRole)
        buttonBox.rejected.connect(self.reject)
        rejectBtn.setDefault(True)

        vLayout.addWidget(buttonBox)

        self.setLayout(vLayout)
