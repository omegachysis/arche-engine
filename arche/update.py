
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
        file = open("release " + tagName + ".zip", "wb")
        file.write(response.read())
        file.close()
    except:
        log.warn("Downloading of release package %s failed!"%(tagName))
        log.warn("The engine reported the following download error: ")
        log.warn(traceback.format_exc())