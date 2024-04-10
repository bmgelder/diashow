Simple javascript diashow player with Python/QT desktop app to produce the used control file

The player allows the images to be displayed in any order and shows the title/description of the image file at the bottom left.

The player expects a control file fileList.js and a directory data with images in its directory.

The control file is a Javascript structure and not JSON. This allows it to be imported directly into HTML using the script tag and avoids problems with CORS.

After starting by double-clicking on index.html, you will find the control for background music at the bottom right. A modern browser refuses to start music without user action. So you have to become active. The control disappears when you move out with the mouse. Don't worry, it will reappear when you move the mouse to the bottom right.

Next photo: left mouse button or right arrow key

Back: right mouse button or left arrow key

Toggle Autoplay: Middle mouse button or up arrow key

The autoplay is set to 4 seconds. You can change the time span with a test editor. Search for 4000 in index.html and enter the desired ms.

The control file is generated with a Python/QT (pyside6) app. Jou need to install pyside6, json5, pillow

Some icons by https://p.yusukekamiyamane.com/. Licensed under a Creative Commons Attribution 3.0 licence.
Some Icons by https://icons8.de/

The start script is diashow.py. First select a directory with the player. Then you can add images (individually or as a list). If an image is selected in the image list, images are inserted first. Otherwise pictures will be added at the end.

If an image is selected, you can edit the title.

The background music (mp3) is selected with the Musik tab.
