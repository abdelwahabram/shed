
import hashlib, zlib, json
from pathlib import Path
import os.path, time, math

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


def updateCurrentPortalHead(ptr):
    currentPortalHandle = open(".shed/CUR_PORTAL", "r")
    
    currentPortal = currentPortalHandle.readline()

    currentShellHandle = open(f".shed/{currentPortal[5:-1]}", "w")
    currentShellHandle.write(f"{ptr}\n")
    currentShellHandle.close()


def getCurrentShellHash():

    currentPortalHandle = open(".shed/CUR_PORTAL", "r")

    currentPortal = currentPortalHandle.readline()

    currentShellHandle = open(f".shed/{currentPortal[5:-1]}", "r")

    currentShell = currentShellHandle.readline()

    return currentShell[:-1]


def getCurrentPortalTreeHash():

    currentShellHash = getCurrentShellHash()

    currentShellContentHandle = open(f".shed/shells/{currentShellHash}", "rb")

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

    content = f"tree {treeHash}\nparent {parentHash}\nauthor {authorName} <{authorEmail}> {currentTime} {timeOffset}\ncommitter {authorName} <{authorEmail}> {currentTime} {timeOffset}\n\n{message}\n"
    # the author and the commiter are the same except for a couple of cases ref:https://stackoverflow.com/questions/6755824/what-is-the-difference-between-author-and-committer-in-git
    
    content = bytes(content, 'utf-8')

    header = bytes(f"commit {len(content)}", 'utf-8')

    blobContent = header +b'\x00'+ content
    fileName = hashlib.sha1(blobContent).hexdigest()
    

    compressedContent = zlib.compress(blobContent)

    with open(f".shed/shells/{fileName}", "wb") as blob:
        blob.write(compressedContent)
    
    updateCurrentPortalHead(fileName)
    return


def repositoryExists():
    path = '.shed/'

    if os.path.exists(path):
        return True
    
    print(" no repo yet, initialize one??")
    return False


def readTree(treeHash, parent = "", output = []):

    with open(f".shed/shells/{treeHash}", "rb") as treeHandle:
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
            readTree(hexValue, f"{parent}/{fileName}" if parent else f"{fileName}", output)
    return


class User:
    def __init__(self):
        self.name = "abdo"
        self.email = "abdo@shed.com"


class TreePath:
    def __init__(self):
        self.isBlob = False
        self.hash = ""
        self.leafs = {}
    
    def addPath(self, path, hash):
        # path = path.split(sep="/")
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
        treeContent = {}
        for file, tree in self.leafs.items():
            treeContent[file] = tree.buildTree()
        content =b""
        for file, data in treeContent.items():
            hash = bytes.fromhex(data[1])
            # content += f"{data[0]} {file}\0{hash}"
            startOfLine = f"{data[0]} {file}\0"
            startOfLine = bytes(startOfLine, 'utf-8')
            content+= startOfLine + hash
        # print(content)
        header = bytes(f"tree {len(content)}\x00", 'utf-8')
        # print(header)
        treeObject = header + content
        fileName = hashlib.sha1(treeObject)
        fileName = fileName.hexdigest()
        # print(f"{file}: {fileName}")
        treeObject = treeObject
        print(treeObject)
        compressedObject = zlib.compress(treeObject)
        # print(compressedObject)
        with open(f".shed/shells/{fileName}", "wb") as blob:
            blob.write(compressedObject)
        return ["40000", fileName]


class UNDER_CONSTRUCTION_AREA_MAINTAINER:
    def __init__(self):
        self.currentShell = {}
        self.newShell = {}
    

    def prepareArea(self):
        if not repositoryExists():
            return
        
        constructionAreaPath = Path(".shed/UNDER_CONSTRUCTION_AREA")

        if constructionAreaPath.is_file():
            
            with open(".shed/UNDER_CONSTRUCTION_AREA", "r") as stored:
                jsonObject = json.load(stored)

                self.currentShell = jsonObject["currentShell"]
                self.newShell = jsonObject["newShell"]
            
            return 


        treeHash = getCurrentPortalTreeHash()

        output = []
        readTree(treeHash, "", output)

        # read the files from the tree and list them into currentShell
        for file in output:
            mode, fileName, fileHash = file

            self.currentShell[fileName] = {"hash": fileHash, "mode": mode}

            self.newShell[fileName] = {"hash": fileHash, "mode": mode, "status":"no change"}


        jsonObject = {"currentShell": self.currentShell, "newShell": self.newShell}
        with open(".shed/UNDER_CONSTRUCTION_AREA", "w") as out:
            json.dump(jsonObject, out)
        

    def addFile(self, fileName):

        if not repositoryExists():
            return
        
        
        with open(fileName, "r") as fileObject:
            content = fileObject.read()
        
        header = f"blob {len(content.encode('utf-8'))}\0"

        blobContent = bytes(header + content, 'utf-8')

        hashObj = hashlib.sha1(blobContent)
        hexValue = hashObj.hexdigest()
        

        if fileName not in self.newShell:
            
            self.newShell[fileName] = {"hash": hexValue, "mode":100644, "status": "created"}
            self.writeUnderConstructionArea()

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

                self.writeUnderConstructionArea()
                print("changes undone")
                return
        

        self.newShell[fileName] = {"hash":hexValue, "mode": 100644, "status": "modified"}
        self.writeUnderConstructionArea()


        compressed = zlib.compress(blobContent)
        path = Path(f'.shed/shells/{hexValue}')
        if path.is_file():
            print("updates was tracked successfuly")
            return
        with open(path, "wb") as blob:
            blob.write(compressed)
        print("updates was tracked successfuly")
    

    def build(self, message):

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
        parentHash = getCurrentShellHash()

        
        # we need to config user ==> create a temp user class and configure it later
        currentUser = User()

        currentTime = int(time.time())

        timeOffset = getTimeOffset()
        
        commitData = [treeHash, parentHash, currentUser.name, currentUser.email, currentTime, timeOffset, message]
        # commitData = ["3af7257939102e630a0a689e6444e4db5300a594","82e887d82baa77dac5fcd56306eade9bfe99276f","Abd_el_wahab","63767622+abdelwahabram@users.noreply.github.com", "1712329881", "+0200", 'created basic repository initializer']

        createCommitBlob(commitData)
        
        UnderConstructionPath = Path(".shed/UNDER_CONSTRUCTION_AREA")

        UnderConstructionPath.unlink()

        self.prepareArea()

        print("#changes was comitted successfully#")

        return
        

    def writeUnderConstructionArea(self):
        jsonObject = {"currentShell": self.currentShell, "newShell": self.newShell}
        with open(".shed/UNDER_CONSTRUCTION_AREA", "w") as out:
            json.dump(jsonObject, out)



a = UNDER_CONSTRUCTION_AREA_MAINTAINER()

a.prepareArea()

a.addFile("source/init.py")
print("############################################")

a.build("msg2")
