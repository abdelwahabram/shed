from directory_path import DirectoryPath
from pathlib import Path
import os


class Repository:
    def __init__(self):
        self.directory_path = DirectoryPath().get_path()
        self.underConstructionArea = None
    
    def create(self):
        if self.directory_path != None:
            print("error403: repo already exists")
            return False
        
        dirs = ['.shed', '.shed/blocks', '.shed/ptrs', '.shed/ptrs/portals' ]
        
        for dir_ in dirs:
            os.mkdir(dir_)
        
        with open(".shed/ptrs/portals/master", "w+") as current_pointer:
            current_pointer.write("\n")
        
        with open(".shed/CUR_PORTAL", "w") as current_portal:
            current_portal.write("ptr: ptrs/portals/master\n")
        
        self.directory_path = Path()
        print(self.directory_path)
        
        print("200: ##repository created## ")

        return True

    def add_file(self):
        pass

    def build(self):
        pass

    def show_status(self):
        pass

# A= Repository()

# A.create()
# print(A.directory_path)