
def getVersion():
    return tuple([int(i) for i in open("arche/version.txt", "r").read().split(".")])

def getLatestRelease():
    pass