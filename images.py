import os
import shutil
from PIL import Image, IptcImagePlugin
from PySide6.QtWidgets import QFileDialog


def readImageTitle(path):
    img = Image.open(path)
    # Nikon Software writes title in IPTC
    iptc = IptcImagePlugin.getiptcinfo(img)
    if iptc:
        return iptc.get((2, 120)).decode("cp1252")

    # Windows Explorer writes title in EXIF
    exif_data = img._getexif()
    if exif_data:
        return exif_data.get(270)


def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def copy_file(src_path, dst_path):
    newPath = dst_path + "/" + os.path.basename(src_path)
    if not os.path.exists(newPath):
        shutil.copy2(src_path, newPath)
    return newPath


def createFileList(parent):
    fileNames = QFileDialog.getOpenFileNames(
        parent, "Bilder für Diashow auswählen",
        parent.active_folder, "Image Files (*.jpg *.JPG *.jpeg *.JPEG *.png *.PNG)")[0]

    newFiles = {"fileList": []}

    if not fileNames:
        return newFiles

    parent.active_folder = os.path.dirname(fileNames[0])

    create_directory_if_not_exists(parent.dataPath)

    lastTitle = None

    # Show title only once for multiple images with the same title

    for fileName in fileNames:
        title = readImageTitle(fileName)
        if title == lastTitle:
            title = None
        else:
            lastTitle = title

        newPath = copy_file(fileName, parent.dataPath)

        localPath = "./data/" + os.path.basename(newPath)

        newFiles["fileList"].append({"path": localPath, "title": title})

    return newFiles
