import os

from fileHelper import create_directory_if_not_exists, copy_file

from PIL import Image, IptcImagePlugin

from PySide6.QtWidgets import QFileDialog


def readImageTitle(path) -> str:
    img = Image.open(path)
    iptc = IptcImagePlugin.getiptcinfo(img)

    if iptc:
        # for k, v in iptc.items():
        #     print(f"{k}:{v.decode()}")
        # Gimp writes Documenttitle here
        if iptc.get((2, 5)):
            return  iptc.get((2, 5)).decode("utf-8")

        # Nikon Software writes title here
        if iptc and iptc.get((2, 120)):
            return iptc.get((2, 120)).decode("cp1252")

    exif_data = img._getexif()
    if exif_data:
        # for key, val in exif_data.items():
        #     if isinstance(val, bytes):
        #         val = val.decode("cp1252")
        #     if key in ExifTags.TAGS:
        #         print(f'{ExifTags.TAGS[key]}:{key}:{val}')
        #     else:
        #         print(f'{key}:{val}')

        # Windows Explorer writes title in EXIF
        if exif_data.get(40091):
            return exif_data.get(40091).decode("utf-16")
    
    return ""

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
