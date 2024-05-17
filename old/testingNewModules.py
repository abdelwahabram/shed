import pathlib
from pathlib import Path
a= Path("old/init.py")
print(a.exists())
# a = a.resolve()
print(a.parts)

def rel(path):
    print(path.resolve())
    a = path
    b = a.parents
    print(len(b))
    print(b[-2].resolve())
    print(b[1].resolve())
    # print(path.)
    # # b = list(path.parts)
    # # print(Path(b[i] for i in range(len(b))))
    # # c = Path().joinpath(b)
    # print(Path.joinpath(path.parts[1:]))
    # # print(path.parents[1].resolve())
    # # print("dd"+path.root)
    
    # # n = Path().joinpath(path.parts[1:])
    
    # # print(n.exists())
    # # print(n)


rel(a)














































































































# import glob, os, pathlib
# # print(glob.glob("./*/*"))

# # print(os.listdir("."))

# def listAllFiles(parent = ""):

#     currentList = os.listdir("." if not parent else f"{parent}/.")

#     output = []
#     for item in currentList:
#         if item[0] == ".": continue

#         filePath = item if not parent else parent + "/" + item

#         if pathlib.Path(filePath).is_file():
        
#             output.append(filePath)
#             continue

#         output += listAllFiles(filePath)
    
#     return output

# print(listAllFiles())