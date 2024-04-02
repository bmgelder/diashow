from imagesList import ImagesList
from PySide6.QtWidgets import QScrollArea


class ScrollAreaImages(QScrollArea):
    def __init__(self, mainWindow):
        super().__init__()
        self.setWidgetResizable(True)
        self.imagesList = ImagesList(mainWindow)
        self.setWidget(self.imagesList)

    def insertImagesList(self, atItem, fileList):
        self.imagesList.insertImagesList(atItem, fileList)

    def updateTitle(self, atItem, newTitle):
        self.imagesList.updateTitle(atItem, newTitle)
# End of ScrollAreaImages
