import glob, os, pathlib
# print(glob.glob("./*/*"))

# print(os.listdir("."))

def listAllFiles(parent = ""):

    currentList = os.listdir("." if not parent else f"{parent}/.")

    output = []
    for item in currentList:
        if item[0] == ".": continue

        filePath = item if not parent else parent + "/" + item

        if pathlib.Path(filePath).is_file():
        
            output.append(filePath)
            continue

        output += listAllFiles(filePath)
    
    return output

print(listAllFiles())