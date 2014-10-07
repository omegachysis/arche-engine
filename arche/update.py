
import logging
import traceback

log = logging.getLogger("R.Update")

def getVersion():
    return _versionStringToTuple(open("arche/version.txt", "r").read())

def _versionStringToTuple(versionString):
    return tuple([int(i) for i in versionString.split(".")])

def getLatestVersion():
    url = "https://raw.githubusercontent.com/omegachysis/arche-engine/master/arche/version.txt"
    import urllib.request
    response = urllib.request.urlopen(url)
    versionString = str(response.read())[2:-1]
    return _versionStringToTuple(versionString)

def canUpdate():
    return getVersion()[0:2]!=getLatestVersion()[0:2]

def update():
    tagName = "v" + ".".join([str(i) for i in getLatestVersion()[0:2]])
    try:
        url = "https://github.com/omegachysis/arche-engine/archive/" + tagName + ".zip"
        log.info("Downloading release package %s"%(url))
        import urllib.request
        response = urllib.request.urlopen(url)
        from os import mkdir
        from os import path
        if not path.exists("_updatePackages/"):
            mkdir("_updatePackages/")
        file = open("_updatePackages/" + updateFilename, "wb")
        file.write(response.read())
        file.close()
        log.info("Download complete!")
    except:
        log.error("Updating of release package %s failed!"%(tagName))
        log.error("The engine reported the following update error: ")
        log.error(traceback.format_exc())
##        import zipfile
##        log.info("Extracting release contents...")
##        with zipfile.ZipFile("_updatePackages/" + updateFilename, "r") as z:
##            z.extractall("_updatePackages/")
##        log.info("Extracted release contents!")
##        log.info("Backing up current installation...")
##        from shutil import copytree
##        from shutil import rmtree
##        rmtree("_updateBackup/", True)
##        copytree(".", "_updateBackup/")
##        log.info("Installing update...")
##        rmtree(".", True)
##        copytree("_updatePackages/{}/".format(releasePackageName), ".")
##        log.info("Update installed!")
##    except:
##        log.error("Updating of release package %s failed!"%(tagName))
##        log.error("The engine reported the following update error: ")
##        log.error(traceback.format_exc())
