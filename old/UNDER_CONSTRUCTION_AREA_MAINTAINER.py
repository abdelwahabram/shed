
import hashlib, zlib, json
from pathlib import Path
import os, time, math
from init import findRepository

def getTimeOffset():
    
    timeOffsetInSeconds = time.localtime().tm_gmtoff

    timeOffsetInHours = timeOffsetInSeconds / 3600

    westOfGMT = True if timeOffsetInHours < 0 else False

    timeOffsetInHours = abs(timeOffsetInHours)
    
    fraction, whole = math.modf(timeOffsetInHours)

    hours = int(whole)
    minutes = int(fraction * 60)

    HH = f"{hours}" if hours > 9 else f"0{hours}"
    MM = f"{minutes}" if minutes > 9 else f"0{minutes}"

    return "-"+HH+MM if westOfGMT else "+"+HH+MM


def updateCurrentPortalHead(ptr, repositoryPath):

    currentPortalPath = repositoryPath.joinpath(".shed/CUR_PORTAL")

    with open(currentPortalPath, "r") as currentPortalHandle:
        currentPortal = currentPortalHandle.readline()

    currentPointerPath = repositoryPath.joinpath(f".shed/{currentPortal[5:-1]}")

    with open(currentPointerPath, "w") as currentShellHandle:
        currentShellHandle.write(f"{ptr}\n")


def getCurrentPortal(repositoryPath):

    currentPortalPath = repositoryPath.joinpath(".shed/CUR_PORTAL")

    with open(currentPortalPath, "r") as currentPortalHandle:
        currentPortal = currentPortalHandle.readline()[5:-1]
    
    return currentPortal


def getCurrentShellHash(repositoryPath):

    currentPortal = getCurrentPortal(repositoryPath)

    currentPointerPath = repositoryPath.joinpath(f".shed/{currentPortal}")

    with open(currentPointerPath, "r") as currentShellHandle:
        currentShell = currentShellHandle.readline()

    return currentShell[:-1]


def getCurrentPortalTreeHash(repositoryPath):

    currentShellHash = getCurrentShellHash(repositoryPath)
    
    if currentShellHash == "":
        # if this is a fresh repository with no commits before
        return False

    currentShellPath = repositoryPath.joinpath(f".shed/shells/{currentShellHash}")

    with open(currentShellPath, "rb") as currentShellContentHandle:
        currentShellContent = currentShellContentHandle.read()

    decompressedShell = zlib.decompress(currentShellContent).decode().splitlines()

    treeHash = decompressedShell[0][-40:]

    return treeHash


def createCommitBlob(commitData):

    treeHash = commitData[0]

    parentHash = commitData[1]

    authorName = commitData[2]

    authorEmail = commitData[3]

    currentTime = commitData[4]

    timeOffset = commitData[5]

    message = commitData[6]

    repositoryPath = commitData[7]

    # the first commit has no parent ==> we ommit this part
    parent = f"parent {parentHash}\n" if parentHash else ""

    content = f"tree {treeHash}\n{parent}author {authorName} <{authorEmail}> {currentTime} {timeOffset}\ncommitter {authorName} <{authorEmail}> {currentTime} {timeOffset}\n\n{message}\n"
    # the author and the commiter are the same except for a couple of cases ref:https://stackoverflow.com/questions/6755824/what-is-the-difference-between-author-and-committer-in-git
    
    content = bytes(content, 'utf-8')

    header = bytes(f"commit {len(content)}", 'utf-8')

    blobContent = header +b'\x00'+ content
    fileName = hashlib.sha1(blobContent).hexdigest()
    

    compressedContent = zlib.compress(blobContent)

    filePath = repositoryPath.joinpath(f".shed/shells/{fileName}")

    with open(filePath, "wb") as blob:
        blob.write(compressedContent)
    print(fileName)
    updateCurrentPortalHead(fileName, repositoryPath)
    return


def repositoryExists():
    path = '.shed/'

    if os.path.exists(path):
        return True
    
    print(" no repo yet, initialize one??")
    return False


def readTree(treeHash, repositoryPath, parent = "", output = []):

    treePath = repositoryPath.joinpath(f".shed/shells/{treeHash}")
    with open(treePath, "rb") as treeHandle:
        treeContents = treeHandle.read()

        decompressedTree = zlib.decompress(treeContents)
        decompressedTree = decompressedTree.split(b"\x00", 1)[1]
    
    while decompressedTree:
        decompressedTree = decompressedTree.split(b" ", 1)

        mode = decompressedTree[0].decode()

        decompressedTree = decompressedTree[1].split(b"\x00", 1)

        fileName = decompressedTree[0].decode()

        hexValue = decompressedTree[1][:20].hex()

        decompressedTree = decompressedTree[1][20:]
        if mode == "100644":
            output.append([mode, f"{parent}/{fileName}" if parent else f"{fileName}", hexValue])
        else:
            readTree(hexValue, repositoryPath, f"{parent}/{fileName}" if parent else f"{fileName}", output)
    return


def listAllFiles(repositoryPath, currentDirectory):

    # currentList = os.listdir("." if not parent else f"{parent}/.")
    currentDirectoryContents = os.listdir(currentDirectory)
    output = []
    for item in currentDirectoryContents:
        if item[0] == ".": continue

        # filePath = repositoryPath.relative_to(currentDirectory.joinpath(f""))
        filePath = currentDirectory.joinpath(f"{item}").resolve().relative_to(repositoryPath)

        if filePath.is_file():
        
            output.append(str(filePath))
            continue

        output += listAllFiles(repositoryPath, filePath)
    
    return output


def createFileBlobContent(filePath):
    with open(filePath, "r") as fileObject:
        content = fileObject.read()
    
    header = f"blob {len(content.encode('utf-8'))}\0"

    blobContent = bytes(header + content, 'utf-8')

    return blobContent


def hashFileBlobContent(blobContent):

    hashObj = hashlib.sha1(blobContent)

    hexValue = hashObj.hexdigest()

    return hexValue


class User:
    def __init__(self):
        self.name = ""
        self.email = ""

        if Path(".shed/shedUserConf.json").is_file():
            self.loadUserData()
            return
        self.setUserData()
    
    def loadUserData(self):
        with open(".shed/shedUserConf.json", "r") as userConfiguration:
            user = json.load(userConfiguration)
        
        self.name = user["name"]

        self.email = user["email"]
    
    def setUserData(self, name = "", email = ""):
        self.name = name if name else self.name
        self.email = email if email else self.email

        user = {"name": self.name, "email": self.email}

        with open(".shed/shedUserConf.json", "w+") as userConfiguration:
            json.dump(user, userConfiguration)



class TreePath:
    def __init__(self):
        self.isBlob = False
        self.hash = ""
        self.leafs = {}
    
    def addPath(self, path, hash):
        if not path:
            self.isBlob = True
            self.hash = hash
            return
        
        if path[0] not in self.leafs:
            self.leafs[path[0]] = TreePath()

        return self.leafs[path[0]].addPath(path[1:], hash)
    
    def traverse(self):
        for name, leaf in self.leafs.items():
            print(name)
            leaf.traverse()
    
    def buildTree(self):
        if self.isBlob:
            return ["100644", self.hash]
        
        subTreeMetaData = {}
        for treeName, treeObject in self.leafs.items():
            subTreeMetaData[treeName] = treeObject.buildTree()
        
        content =b""
        for treeName, treeData in subTreeMetaData.items():
            mode, hexHash = treeData

            hashValue = bytes.fromhex(hexHash)

            line = bytes(f"{mode} {treeName}\0",'utf-8') + hashValue

            content += line
        
        header = bytes(f"tree {len(content)}\x00", 'utf-8')

        treeBlobContent = header + content

        treeBlobName = hashlib.sha1(treeBlobContent).hexdigest()

        compressedObject = zlib.compress(treeBlobContent)
        
        with open(f".shed/shells/{treeBlobName}", "wb") as blob:
            blob.write(compressedObject)
        
        return ["40000", treeBlobName]


class UNDER_CONSTRUCTION_AREA_MAINTAINER:
    def __init__(self):
        self.currentShell = {}
        self.newShell = {}
    

    def prepareArea(self):

        repositoryPath = findRepository()
        if repositoryPath == False:
            print("error404: repo not found")
            return False
        
        # constructionAreaPath = Path()
        constructionAreaPath = repositoryPath.joinpath(".shed/UNDER_CONSTRUCTION_AREA")
        if constructionAreaPath.is_file():
            
            with open(constructionAreaPath, "r") as stored:
                jsonObject = json.load(stored)

                self.currentShell = jsonObject["currentShell"]
                self.newShell = jsonObject["newShell"]
            
            return 


        treeHash = getCurrentPortalTreeHash(repositoryPath)

        if treeHash == False:
            # if there's no commit before then the we write an empty self.currentShell dict

            self.writeUnderConstructionArea(repositoryPath)

            return
        
        output = []
        readTree(treeHash, repositoryPath, "", output)

        # read the files from the tree and list them into currentShell
        for file in output:
            mode, fileName, fileHash = file

            self.currentShell[fileName] = {"hash": fileHash, "mode": mode}

            self.newShell[fileName] = {"hash": fileHash, "mode": mode, "status":"no change"}


        self.writeUnderConstructionArea(repositoryPath)
        

    def addFile(self, filePath):

        # if not repositoryExists():
        #     return

        repositoryPath = findRepository()

        if repositoryPath == False:
            print("error404: repo not found")
            return False

        blobContent = createFileBlobContent(filePath)

        hexValue = hashFileBlobContent(blobContent)
        
        path = repositoryPath.joinpath(f'.shed/shells/{hexValue}')

        if not path.is_file():

            compressedContent = zlib.compress(blobContent)

            with open(path, "wb") as blob:
                
                blob.write(compressedContent)
        
        fileName = str(filePath.resolve().relative_to(repositoryPath))
        print(fileName)

        if fileName not in self.newShell:
            
            self.newShell[fileName] = {"hash": hexValue, "mode":100644, "status": "created"}
            self.writeUnderConstructionArea(repositoryPath)

            print("file added successfully")

            return

        # if the same hash in newShell >>> keep it 
        if hexValue == self.newShell[fileName]["hash"]:
            print("no changes detected")
            return

        # if it's the old value in currentShell >> > no change
        if fileName in self.currentShell:
            
            if hexValue == self.currentShell[fileName]["hash"]:

                self.newShell[fileName]["hash"] = hexValue
                self.newShell[fileName]["status"] = "no change"

                self.writeUnderConstructionArea(repositoryPath)
                print("changes undone")
                return
        

        self.newShell[fileName] = {"hash":hexValue, "mode": 100644, "status": "modified"}
        self.writeUnderConstructionArea(repositoryPath)

        print("updates was tracked successfuly")
    

    def build(self, message):
        repositoryPath = findRepository()

        if repositoryPath == False:
            print("error404: no repo found")
            return False

        isChanged = False
        for fileMetadata in self.newShell.values():

            if fileMetadata["status"] != "no change":

                isChanged = True
                break
        

        if not isChanged:

            print("no changes lately")
            return


        # create a tree data structure to store the data of
        # the commit tree and its subtrees
        treePath = TreePath()

        for filePath, fileMetaData in self.newShell.items():

            parentsList = filePath.split(sep="/")
            treePath.addPath(parentsList, fileMetaData["hash"])
        

        treeHash = treePath.buildTree()[1]
        
        # to be fixed later ==> the first commit ever has no parent
        parentHash = getCurrentShellHash(repositoryPath)

        
        # we need to config user ==> create a temp user class and configure it later
        currentUser = User()
        currentUser.setUserData("abdo", "body@shed.com")

        currentTime = int(time.time())

        timeOffset = getTimeOffset()
        
        commitData = [treeHash, parentHash, currentUser.name, currentUser.email, currentTime, timeOffset, message, repositoryPath]
        # commitData = ["3af7257939102e630a0a689e6444e4db5300a594","82e887d82baa77dac5fcd56306eade9bfe99276f","Abd_el_wahab","63767622+abdelwahabram@users.noreply.github.com", "1712329881", "+0200", 'created basic repository initializer']

        createCommitBlob(commitData)
        
        UnderConstructionPath = repositoryPath.joinpath(".shed/UNDER_CONSTRUCTION_AREA")

        UnderConstructionPath.unlink()

        self.prepareArea()

        print("#changes was comitted successfully#")

        return
        

    def writeUnderConstructionArea(self, repositoryPath):
        jsonObject = {"currentShell": self.currentShell, "newShell": self.newShell}

        constructionAreaPath = repositoryPath.joinpath(".shed/UNDER_CONSTRUCTION_AREA")
        with open(constructionAreaPath, "w") as out:
            json.dump(jsonObject, out)


    def showStatus(self):

        repositoryPath = findRepository()
        if repositoryPath == False:
            print("error404: repo not found")
            return False

        filesList = listAllFiles(repositoryPath, repositoryPath)
        # iterate all the files and create blob content and hash it
        # compare the hash with the value in newShell and currentShell

        underConstructionFiles = []
        modifiedFiles = []
        notTrackedFiles = []

        for fileName in filesList:
            if fileName not in self.newShell:
                notTrackedFiles.append(fileName)
                continue

            fileBlobContent = createFileBlobContent(fileName)
            fileHashHex = hashFileBlobContent(fileBlobContent)

            if fileHashHex != self.newShell[fileName]["hash"]:
                modifiedFiles.append(fileName)
            
            if self.newShell[fileName]["status"] != "no change":
                underConstructionFiles.append(fileName)
        currentPortal = getCurrentPortal(repositoryPath).split("/")[-1]
        print(f"current portal ==> {currentPortal}")
        print("added files: ")
        for file in underConstructionFiles:
            print(file)
        
        print("modified files: ")
        for file in modifiedFiles:
            print(file)
        
        print("no tracked files: ")
        for file in notTrackedFiles:
            print(file)
        return



a = UNDER_CONSTRUCTION_AREA_MAINTAINER()

a.prepareArea()

initPyPath = Path("source/init.py")

print(initPyPath.is_file())

a.addFile(initPyPath)
# a.showStatus()
# # print("############################################")
# # a.addFile("source/hash.py")
# # a.showStatus()
# # print("############################################")
# a.build("testing adding repo path")
a.showStatus()

# print(findRepository())