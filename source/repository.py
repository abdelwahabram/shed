from directory_path import DirectoryPath
from under_construction_area import UnderConstructionArea
from user import User
from pathlib import Path
import os


class Repository:
    def __init__(self):
        self.directory_path = DirectoryPath()
        
        if DirectoryPath().get_path() != None:
            self.user = User(directory_path = self.directory_path.get_path())
            self.under_construction_area = UnderConstructionArea(directory_path = self.directory_path, user = self.user)
    
    
    def create(self):
        if self.directory_path.get_path() != None:
            print("error403: repo already exists")
            return False
        
        dirs = ['.shed', '.shed/blocks', '.shed/ptrs', '.shed/ptrs/portals' ]
        
        for dir_ in dirs:
            os.mkdir(dir_)
        
        with open(".shed/ptrs/portals/master", "w+") as current_pointer:
            current_pointer.write("\n")
        
        with open(".shed/CUR_PORTAL", "w") as current_portal:
            current_portal.write("ptr: ptrs/portals/master\n")
        
        # self.directory_path = Path()
        # print(self.directory_path)
        self.directory_path.set_path(Path())
        
        self.user = User(directory_path = self.directory_path.get_path())
        self.under_construction_area = UnderConstructionArea(directory_path = self.directory_path, user = self.user)
        
        print("200: ##repository created## ")

        return True


    def add_file(self, file_path):
        self.under_construction_area.create()
        return self.under_construction_area.add_file(file_path)


    def build(self, message):
        self.under_construction_area.create()
        return self.under_construction_area.build(message)


    def show_status(self):
        self.under_construction_area.create()
        return self.under_construction_area.show_status()
