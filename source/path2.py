import os


## basic path setup
path = os.path.abspath(__file__)
# /media/appstew/239G/raw100.img/appimage-making/success/appsuite/app.py

path = os.path.dirname(path)
# /media/appstew/239G/raw100.img/appimage-making/success/appsuite
# appimage 일 경우 다른 경로

os.chdir(path)

# including images resources in appimage itself 
imagepath = os.path.join(path, 'images')
iconspath = os.path.join(path, 'images', 'uxwing.com')
configpath = os.path.join(path, '.config')
homepath = os.environ['HOME']
# /$HOME/.appstew 를 appstew 앱의 기본경로로 쓸 것이다.
appstewPath = os.path.join(homepath, '.appstew')
# 브라우저의 탭리스트 파일
# tablistpath = os.path.join(appstewPath, 'tablist')
# icons
myiconpath = os.path.join(appstewPath, 'images')