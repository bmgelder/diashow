# Only for Command line args
import sys
import os

from controlFile import openCreateControlFile, saveControlFile
from images import createFileList
from scrollAreaImages import ScrollAreaImages
from cancelNextDialog import CancelNextDialog

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QInputDialog,
    QTabWidget,
    QWidget,
    QFileDialog,
    QStatusBar,
    QLabel,
    QStyle)


class MainWindow(QMainWindow):
    # Subclass QMainWindow to customize your application's main window
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Steuerdatei für Diashow")

        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.move(rect.width() // 4, 0)

        titleBarHeight = self.style().pixelMetric(
            QStyle.PM_TitleBarHeight)

        self.resize(900, rect.height() - (titleBarHeight * 2))

        # Action add images
        self.add_image_action = QAction(
            QIcon("plus.png"), "Bilder hinzufügen", self)
        self.add_image_action.setToolTip(
            "Bilder für Diashow hinzufügen")
        self.add_image_action.triggered.connect(self.addImages)

        # Action edit title
        self.edit_title_action = QAction(
            QIcon("icons8-bearbeiten-30.png"), "Titel ändern", self)
        self.edit_title_action.setToolTip(
            "Titel des Bildes ändern")
        self.edit_title_action.triggered.connect(self.editTitle)
        self.edit_title_action.setDisabled(True)

        # Action save
        self.save_action = QAction(
            QIcon("disc.png"), "Speichern", self)
        self.save_action.setToolTip("Steuerdatei speichern")
        self.save_action.triggered.connect(self.saveControlFile)
        self.save_action.setDisabled(True)

        self.atImage = 1
        self.active_folder = os.getcwd()

        dirName = QFileDialog.getExistingDirectory(
            parent=self, caption="Verzeichnis für Steuerdatei auswählen",
            dir=self.active_folder, options=QFileDialog.ShowDirsOnly)

        if dirName == "":   # Cancel
            sys.exit()

        self.active_folder = dirName
        os.chdir(dirName)   # Be careful: Icon files are not longer found

        self.isInit = True
        self.controlFilename = dirName + "/fileList.js"
        self.dataPath = dirName + "/data"
        self.setWindowTitle(f"Steuerdatei {os.path.split(dirName)[1]} [*]")
        self.controlData = openCreateControlFile(self.controlFilename)

        toolbar = self.addToolBar("Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        toolbar.setMovable(False)
        toolbar.addAction(self.add_image_action)
        toolbar.addAction(self.edit_title_action)
        toolbar.addAction(self.save_action)

        self.statusBar = QStatusBar(self)
        self.image_count_label = QLabel("Anzahl Bilder: 0")
        self.statusBar.addPermanentWidget(self.image_count_label)
        self.statusBar.showMessage(f"Steuerdatei: {self.controlFilename}")
        self.statusBar.setStyleSheet("background-color: lightgray")
        self.setStatusBar(self.statusBar)

        self.show()

        # Create a tab widget
        self.tab_widget = QTabWidget(self)

        # Create image tab
        self.scrollArea = ScrollAreaImages(self)
        self.scrollArea.insertImagesList(
            self.atImage, self.controlData["fileList"])
        self.atImage = len(self.controlData["fileList"]) + 1

        self.musicTab = QWidget()

        # Add tabs to the tab widget
        self.tab_widget.addTab(self.scrollArea, "Bilder")
        self.tab_widget.addTab(self.musicTab, "Musik")

        # Set the tab widget as the central widget of the main window
        self.setCentralWidget(self.tab_widget)
        # Connect the currentChanged signal to a slot
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        self.isInit = False

    def addImages(self):
        newFiles = createFileList(self)
        if len(newFiles["fileList"]) > 0:
            self.setWindowModified(True)
            self.save_action.setEnabled(True)
            self.scrollArea.insertImagesList(
                self.atImage, newFiles["fileList"])
            self.controlData["fileList"][self.atImage -
                                         1: self.atImage - 1] = newFiles["fileList"]
            self.statusBar.showMessage(
                f"{len(newFiles['fileList'])} Bilder hinzugefügt")
            self.atImage = self.atImage + len(newFiles["fileList"])

    def editTitle(self):
        currentTitle = self.controlData["fileList"][self.atImage - 1]["title"]

        editDlg = QInputDialog(self)
        editDlg.setInputMode(QInputDialog.InputMode.TextInput)
        editDlg.setLabelText("Titel ändern:")
        editDlg.setTextValue(currentTitle)

        if editDlg.exec() == 1:
            newTitle = editDlg.textValue()
            self.controlData["fileList"][self.atImage - 1]["title"] = newTitle
            self.scrollArea.updateTitle(self.atImage, newTitle)
            self.setWindowModified(True)
            self.save_action.setEnabled(True)
            self.statusBar.showMessage(
                f"Titel geändert: {newTitle}")

    def saveControlFile(self):
        saveControlFile(self.controlFilename, self.controlData)
        self.setWindowModified(False)
        self.save_action.setDisabled(True)
        self.statusBar.showMessage(
            f"Steuerdatei: {self.controlFilename} gespeichert")

    def on_tab_changed(self, index):
        if index == 0:
            self.add_image_action.setText("Bilder hinzufügen")
            self.add_image_action.setEnabled(True)
            self.add_image_action.setToolTip(
                "Bilder für Diashow hinzufügen")
        else:
            self.add_image_action.setText("Musik hinzufügen")
            self.add_image_action.setDisabled(True)
            self.add_image_action.setToolTip(
                "Musik für Diashow hinzufügen")

    def closeEvent(self, event):
        if self.isWindowModified():
            dialog = CancelNextDialog(self)
            dialog.adjustPosition(self)

            result = dialog.exec()

            if result == 1:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


# Create an application
app = QApplication(sys.argv)

# Create a widget
window = MainWindow()
# window.show()

# Execute the application
app.exec()
