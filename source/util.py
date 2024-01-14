import os, shutil, errno

##setstylesheet color
grey = "background-color: rgb(192, 191, 188);"
yellow = "background-color: hsla(60, 90%, 60%, .6);"
red = "background-color: hsla(6, 60%, 60%, 1);"
indigo = "background-color: hsla(240, 60%, 50%, 1);"
blue = "background-color: hsla(240, 85%, 60%, 1);"

def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print ('Error: Creating dir. ' +  dir)


def copyFile(srcFile, destDir):
    try:
        if os.path.exists(srcFile):
            shutil.copy(srcFile, destDir)
    except OSError as err:
        print ('Error: Copying file    ' + srcFile + '   to   ' + destDir)


def copyFolder(src, dst):

    print("")
    try:
        if os.path.exists(src):
            #os.popen('cp -r ' + src + ' ' + dst)
            shutil.copytree(src, dst)
    except OSError as err:
        if err.errno == errno.ENOTDIR:
            shutil.copy2(src, dst)
            
        else:
            print("ree " + "Error: % s" % err)





