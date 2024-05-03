import os, pathlib

def findRepository():
    path = pathlib.Path()

    while True:

        repositoryPath = path.joinpath(".shed")
        if repositoryPath.exists():
            return path.resolve()
        
        # if this is a mounting point: return false
        if os.path.ismount(path):

            return False

        path = path.parent.resolve()
    return False

# print(findRepository())

class RepositoryInitializer:
    def __init__(self)->bool:
        foundRepositoryPath = findRepository()
        if foundRepositoryPath != False:
            print("error403: repository already exists")
            return
        self.initializeRepository()
    

    def initializeRepository(self):
        
        dirs = ['.shed', '.shed/shells', '.shed/ptrs', '.shed/ptrs/portals' ]
        for dir in dirs:
            os.mkdir(dir)
        
        with open(".shed/ptrs/portals/master", "w+") as currentShellHash:
            currentShellHash.write("\n")
        
        with open(".shed/CUR_PORTAL", "w") as currentPortal:
            currentPortal.write("ptr: ptrs/portals/master\n")



A = RepositoryInitializer()
