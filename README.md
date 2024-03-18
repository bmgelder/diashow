Simple javascript diashow player with Python/QT desktop app to produce the used control file

The player allows the images to be displayed in any order and shows the title/description of the image file at the bottom left.

The player expects a control file fileList.js and a directory data with images in its directory.

The control file is a Javascript structure and not JSON. This allows it to be imported directly into HTML using the script tag and avoids problems with CORS.

The control file is generated with a Python/QT (pyside6) app. Jou need to install pyside6, json5, pillow 

The start script is diashow.py. First select a directory with the player. Then you can add images (individually or as a list). If an image is selected in the image list, images are inserted first.
