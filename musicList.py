import os

from fileHelper import create_directory_if_not_exists, copy_file

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog


class MusicList(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addStretch(1)

    def insertMusicList(self, newMusicList):
        for i in range(0, len(newMusicList)):
            musicItem = newMusicList[i]['path']
            musicLabel = QLabel(musicItem)
            self.layout.insertWidget(self.layout.count() - 1, musicLabel)


def createMusicList(parent):
    fileNames = QFileDialog.getOpenFileNames(
        parent, "Musik für Diashow auswählen",
        parent.active_folder, "Music Files (*.mp3 *.MP3)")[0]

    newFiles = {"musicList": []}

    if not fileNames:
        return newFiles

    parent.active_folder = os.path.dirname(fileNames[0])

    create_directory_if_not_exists(parent.dataPath)

    for fileName in fileNames:
        newPath = copy_file(fileName, parent.dataPath)

        localPath = "./data/" + os.path.basename(newPath)

        newFiles["musicList"].append({"path": localPath})

    return newFiles
