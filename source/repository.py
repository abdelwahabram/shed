from source.directory_path import DirectoryPath
from source.under_construction_area import UnderConstructionArea
from source.user import User
from pathlib import Path
import os, shutil


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

    
    def show_difference(self):
        self.under_construction_area.create()
        self.under_construction_area.show_difference()
        return
    
    
    def turn_into_git_repository(self):
        
        if self.directory_path.get_path() == None:
            print("error403: repo already exists")
            return False
        
        dirs = ['.', '.git/objects', '.git/refs', '.git/refs/heads', '.git/refs/remotes' ]
        
        dirs_paths = [self.directory_path.get_path().joinpath(dir_) for dir_ in dirs]
        
        for dir_path in dirs_paths:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        blocks_path = self.directory_path.get_path().joinpath(".shed/blocks")
        
        blocks = blocks_path.glob("*")
        
        for block_path in blocks:
            block_name = str(block_path.relative_to(blocks_path))
            
            object_dir = block_name[:2]
            
            object_file = block_name[2:]
            
            object_dir_path = self.directory_path.get_path().joinpath(f".git/objects/{object_dir}")
            
            object_dir_path.mkdir(parents=True, exist_ok=True)
            
            new_object_path = self.directory_path.get_path().joinpath(f".git/objects/{object_dir}/{object_file}")
            
            shutil.copy(block_path, new_object_path)
        
        
        head_path = self.directory_path.get_path().joinpath(".git/HEAD")
        
        current_portal = self.under_construction_area.current_portal.get_current_portal()[13:]
        current_portal = "main" if current_portal == "master" else current_portal
        
        current_head = f"ref: refs/heads/{current_portal}" 
        
        with open(head_path, "w+") as head_handle:
            head_handle.write(current_head)
            
        
        portals_path = self.directory_path.get_path().joinpath(".shed/ptrs/portals/")
        portals = portals_path.glob("*")
        
        for portal_path in portals:
            
            portal_name = str(portal_path.relative_to(portals_path))
            
            head_path = self.directory_path.get_path().joinpath(f".git/refs/heads/{portal_name}") if portal_name != "master" else self.directory_path.get_path().joinpath(".git/refs/heads/main")
            
            shutil.copy(portal_path, head_path)
        
        print("200: git repository created successfully, changes are ready to be pushed")
        return True
    
    
    def add_remote(self):
        return
    
    
    def push_to_github(self):
        return


# A = Repository()
# A.create()
# # A.show_difference()
# A.turn_into_git_repository()

# # P = Path("source/tree.py")
# # # # # print(P.exists())
# # # # # # P = Path("tree.py")
# # # # # # print(P.exists())
# # # # # # print("**********************************************")
# # # # # # A.show_status()
# # A.add_file(P)
# # # # # # print("**********************************************")
# # # # # A.show_status()
# # A.build("new tesssssssst")
# # # # # print("**********************************************")
# A.show_status()