# Simple Appsuite

- (some images)

## about this project
- this app was meant to embed and use [portable urxvt](https://github.com/appstew/appimage-urxvt/tree/main), a [webbrowser]() in one window using x11 window ID.
- this can also be used for embedding other linux apps, including qt apps

## how to use

## how to build on linux
```bash
sudo apt install python3-gi pkg-config gcc libcairo2-dev python3-dev libgirepository1.0-dev gir1.2-gtk-3.0 gir1.2-wnck-3.0
pip install -r requirements-linux.txt
```
- and then 
```
python3 embed2.py
```
- if above command works do the next:
```
pyinstaller --add-data source:source --windowed --onefile embed2.py
```

## to-do
- upload some images made using obsidian-excalidraw
- complete and arrange this project in ubuntu01-appimage
- test built app in fedora-silverblue
- complete and upload this project and README.md
- add feature to change main page background
- add simple file explorer
- add simple text/markdown editor
