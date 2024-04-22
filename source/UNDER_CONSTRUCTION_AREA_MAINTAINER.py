
import hashlib, zlib, json
from pathlib import Path
import os.path, time, math

def getTimeOffset():
    # dddddddd
    timeOffsetInSeconds = time.localtime().tm_gmtoff
    timeOffsetInHours = timeOffsetInSeconds / 3600
    westOfGMT = True if timeOffsetInHours < 0 else False
    timeOffsetInHours = abs(timeOffsetInHours)
    # hours = int(timeOffsetInHours)
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
def getCurrentPortalHash():
    currentPortalHandle = open(".shed/CUR_PORTAL", "r")
    currentPortal = currentPortalHandle.readline()
    
    # go to the current portal
    currentShellHandle = open(f".shed/{currentPortal[5:-1]}", "r")
    currentShell = currentShellHandle.readline()
    # go the hash of the cur portal
    # open the shell
    currentShellContentHandle = open(f".shed/shells/{currentShell[:-1]}", "rb")
    currentShellContent = currentShellContentHandle.read()
    # unzip it
    decompressedShell = zlib.decompress(currentShellContent).decode().splitlines()
    print(decompressedShell)
    # git the tree hash
    # lineCounter = 0
    # while lineCounter < 2:
    #     treeHash = decompressedShell.readline()
    #     lineCounter += 1
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
    print(content)
    content = bytes(content, 'utf-8')
    header = bytes(f"commit {len(content)}", 'utf-8')
    data = header +b'\x00'+ content
    fileName = hashlib.sha1(data).hexdigest()
    print(fileName)

    # ['commit 309\x00tree ', 'parent ', 'author  <> 1712329881 +0200', 'committer Abd_el_wahab <63767622+abdelwahabram@users.noreply.github.com>  ', '', ]
    # zib and save
    store = zlib.compress(data)
    with open(f".shed/shells/{fileName}", "wb") as blob:
        blob.write(store)
    
    updateCurrentPortalHead(fileName)
    pass

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
        print(content)
        header = bytes(f"tree {len(content)}\x00", 'utf-8')
        print(header)
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

class UNDER_CONSTRUCTION_AREA_MAINTAINER:
    def __init__(self):
        self.currentShell = {}
        self.newShell = {}
        pass

    def prepareArea(self):
        constructionAreaPath = Path(".shed/UNDER_CONSTRUCTION_AREA")

        if constructionAreaPath.is_file():
            
            with open(".shed/UNDER_CONSTRUCTION_AREA", "r") as stored:
                jsonObject = json.load(stored)

                self.currentShell = jsonObject["currentShell"]
                self.newShell = jsonObject["newShell"]
            
            return 


        treeHash = getCurrentPortalHash()

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
        # pass
        # check if repo exisits
        path = '.shed/'
        if not os.path.exists(path):
            print(" no repo yet, initialize one??")
            return

        # check if file not ignored one

        # check if file changed ==> compare the hash with the one in current and new shell
        # hash the content to create object name
        hash = ""
        fileObject = open(fileName, "r")
        content = fileObject.read()
        header = f"blob {len(content.encode('utf-8'))}\0"
        shellName = header + content
        print(shellName)
        hashObj = hashlib.sha1(shellName.encode())
        hashName = hashObj.hexdigest()
        print(hashName)

        if fileName not in self.newShell:
            print("a")
            self.newShell[fileName] = {"hash": hashName, "mode":100644, "status": "created"}
            jsonObject = {"currentShell": self.currentShell, "newShell": self.newShell}
            with open(".shed/UNDER_CONSTRUCTION_AREA", "w") as out:
                json.dump(jsonObject, out)
            return

        # if the same hash in newShell >>> keep it 
        if hashName == self.newShell[fileName]["hash"]:
            print("b")
            return

        # if it's the old value in currentShell >> > no change
        if fileName in self.currentShell:
            print("c")
            if hashName == self.currentShell[fileName]["hash"]:
                self.newShell[fileName]["hash"] = hashName
                self.newShell[fileName]["status"] = "no change"

                jsonObject = {"currentShell": self.currentShell, "newShell": self.newShell}
                with open(".shed/UNDER_CONSTRUCTION_AREA", "w") as out:
                    json.dump(jsonObject, out)
                return
        

        
        print(45)
        # otherwise add it to the new shell
        self.newShell[fileName] = {"hash":hashName, "mode": 100644, "status": "modified"}
        
        jsonObject = {"currentShell": self.currentShell, "newShell": self.newShell}
        with open(".shed/UNDER_CONSTRUCTION_AREA", "w") as out:
            json.dump(jsonObject, out)


        

        # zib the content and save the object
        data = shellName.encode('utf-8')

        compressed = zlib.compress(data)
        path = Path(f'.shed/shells/{hashName}')
        if path.is_file():
            return
        with open(path, "wb") as blob:
            blob.write(compressed)
        # add the file name to the indext
        #########update the under const area after that
    
    def build(self, message):
        # check if idx file exists
        path = Path(".shed/UNDER_CONSTRUCTION_AREA")
        if not path.is_file():
            print("no changes lately")
            return
        # check if new Changes exist

        isChanged = False
        for file in self.newShell.values():
            if file["status"] != "no change":
                isChanged = True
                break
        if not isChanged:
            print("no changes lately")
            return



        # create an adjacency tree for the newShell
        treePath = TreePath()
        for filePath, data in self.newShell.items():
            path = filePath.split(sep="/")
            treePath.addPath(path, data["hash"])
        
        print(555)
        print(message)
        treePath.traverse()
        treeHash = treePath.buildTree()[1]
        print(treeHash)
        parentHash = getCurrentPortalHash()
        print(parentHash)
        # iterate the list and create a shell pointing to the root tree as a commit in git
        # now we have the tree hash, the parent tree hash
        # we need to config user ==> create a temp user class and configure it later
        currentUser = User()
        # and access time and transform it into secnds
        currentTime = int(time.time())
        # print(currentTime)
        # print(time.altzone)
        # print(time.timezone)
        # print(time.tzname)
        # print(time.localtime().tm_gmtoff)
        # print(tzlocal.get_localzone())
        timeOffset = getTimeOffset()
        print(timeOffset)
        commitData = [treeHash, parentHash, currentUser.name, currentUser.email, currentTime, timeOffset, message]
        # commitData = ["3af7257939102e630a0a689e6444e4db5300a594","82e887d82baa77dac5fcd56306eade9bfe99276f","Abd_el_wahab","63767622+abdelwahabram@users.noreply.github.com", "1712329881", "+0200", 'created basic repository initializer']

        createCommitBlob(commitData)
        # update idxFile ==> delete
        print(5555)
        UnderConstructionPath = Path(".shed/UNDER_CONSTRUCTION_AREA")
        UnderConstructionPath.unlink()
        # update the currentPortal head
        



a = UNDER_CONSTRUCTION_AREA_MAINTAINER()
a.prepareArea()
# a.add
# a.addFile("source/init.py")

# a.build("msg")
