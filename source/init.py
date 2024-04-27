import os

class RepositoryInitializer:
    def __init__(self):
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
