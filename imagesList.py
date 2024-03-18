import os
import re
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor,  QColorConstants
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame)


class ClickableWidget(QWidget):
    def __init__(self, mainWindow, imagesList):
        super().__init__()

        self.mainWindow = mainWindow
        self.imagesList = imagesList

        self.setEnabled(True)   # Enable mouse events
        self.setAutoFillBackground(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            palette = self.palette()
            # Toggle background color
            if palette.color(self.backgroundRole()) == QColorConstants.LightGray:
                palette.setColor(self.backgroundRole(),
                                 QColor(QColorConstants.White))
                # No Image selected: Append to the end of the list
                self.mainWindow.atImage = len(
                    self.mainWindow.controlData["fileList"]) + 1
                self.setPalette(palette)
                return

            # Set image selected
            palette.setColor(self.backgroundRole(),
                             QColor(QColorConstants.LightGray))
            self.setPalette(palette)

            # Reset background color of the previous selected image if any
            if self.mainWindow.atImage <= len(self.mainWindow.controlData["fileList"]):
                oldWiget = self.imagesList.verticalLayout.itemAt(
                    self.mainWindow.atImage - 1).layout().itemAt(0).widget()
                oldPalette = oldWiget.palette()
                oldPalette.setColor(oldWiget.backgroundRole(),
                                    QColor(QColorConstants.White))
                oldWiget.setPalette(oldPalette)

            itemNumber = re.search(r'\d+',
                                   self.layout().itemAt(0).layout().itemAt(0).widget().text())
            self.mainWindow.atImage = int(itemNumber.group())


class ImagesList(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        # Create a vertical layout
        self.verticalLayout = QVBoxLayout(self)
        self.setLayout(self.verticalLayout)
        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addStretch(1)

    # Create an image layout
    def createImageLayout(self, atItem, fileItem):
        # Create vertical layout for image widget and separator line
        verticalLayout = QVBoxLayout()

        # Create Widget to select image
        clickableWidget = ClickableWidget(self.mainWindow, self)

        # Create image layout
        horizontalLayout = QHBoxLayout()
        clickableWidget.setLayout(horizontalLayout)

        # Add sequence number, filename, and title
        innerVerticalLayout = QVBoxLayout()

        sequenceNumberLabel = QLabel(f"Bildnr. {atItem}")
        filenameLabel = QLabel(fileItem['path'])
        titleLabel = QLabel(fileItem['title'])
        innerVerticalLayout.addWidget(sequenceNumberLabel)
        innerVerticalLayout.addWidget(filenameLabel)
        innerVerticalLayout.addWidget(titleLabel)
        innerVerticalLayout.addStretch()

        # Add the inner layout to the horizontal layout
        horizontalLayout.addLayout(innerVerticalLayout)
        horizontalLayout.addSpacing(20)

        # Add Image
        imageLabel = QLabel(self)
        pixmap = QPixmap(fileItem['path'])
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
        imageLabel.setPixmap(pixmap)
        horizontalLayout.addWidget(imageLabel)

        verticalLayout.addWidget(clickableWidget)

        # Horizontal line
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setFrameShadow(QFrame.Sunken)
        verticalLayout.addWidget(hLine)

        return verticalLayout

    def insertImagesList(self, atItem, newFileList):
        for i in range(0, len(newFileList)):
            # Create image layout
            imageLayout = self.createImageLayout(atItem + i, newFileList[i])

            # Add the horizontal layout to the vertical layout
            self.verticalLayout.insertLayout(
                atItem - 1 + i, imageLayout)
            if self.mainWindow.isInit:
                self.mainWindow.image_count_label.setText(
                    f"Anzahl Bilder: {i + 1}")
            else:
                self.mainWindow.image_count_label.setText(
                    f"Anzahl Bilder: {len(self.mainWindow.controlData['fileList']) + i + 1}")
            QApplication.processEvents()

        if self.mainWindow.isInit:
            return

        for i in range(atItem + len(newFileList) - 1,
                       len(self.mainWindow.controlData['fileList']) + len(newFileList)):
            # Update sequence number
            self.verticalLayout.itemAt(i).layout().itemAt(
                0).widget().layout().itemAt(0).layout().itemAt(0).widget().setText(f"Bildnr. {i + 1}")
            QApplication.processEvents()

# End of ImagesList
