from source.directory_path import DirectoryPath
from source.current_portal import CurrentPortal
from source.file import File
from source.user import User
from source.shell import Shell
from source.tree import Tree

from pathlib import Path
import json, glob


class UnderConstructionArea:
    
    def __init__(self, *args, **kwargs):

        self.current_shell = {}

        self.new_shell = {} 

        self.directory_path = kwargs.get("directory_path", DirectoryPath())

        self.area_path = self.__set_area_path()

        self.current_portal = CurrentPortal(self.directory_path.get_path())
        
        self.user = kwargs.get("user", User(directory_path = self.directory_path.get_path()))
    

    def create(self):
        if self.directory_path.get_path() == None:
            print("error404: repo not found")
            return False
        
        if self.area_path.exists():
            self.read_area()
            return True
        
        tree_hash = self.current_portal.get_current_portal_tree_hash()
        
        if tree_hash == False:
            self.write_area()
            return True
        
        tree_object = Tree(hash_ = tree_hash, directory_path = self.directory_path.get_path(), path = self.directory_path.get_path())
        
        tree_object.read()
        
        tree_content = tree_object.traverse_content()
        
        for file in tree_content:
            file_name, file_mode, file_hash = file
            
            self.current_shell[file_name] = {"mode": file_mode, "hash": file_hash}
            self.new_shell[file_name] = {"mode": file_mode, "hash": file_hash, "status": "no change"}
        
        self.write_area()
        
        return True
        

    def add_file(self, file_path):
        
        if self.directory_path.get_path() == None:
            print("error404: repo not found")
            return False
        print(file_path)
        file_object = File(directory_path = self.directory_path.get_path(), path = file_path)
        
        file_object.create()
        
        hash_value = file_object.get_hash()
        
        file_name = file_object.get_name()
        print(file_name)
        
        if file_name not in self.new_shell:
            self.new_shell[file_name] = {"hash": hash_value, "mode":100644, "status": "created"}
            self.write_area()
            print("200:file tracked successfully")
            return True
        
        if hash_value == self.new_shell[file_name]["hash"]:
            print("no changes detected")
            return True
        
        if file_name in self.current_shell:
            
            if hash_value == self.current_shell[file_name]["hash"]:
                
                self.new_shell[file_name]["hash"] = hash_value
                self.new_shell[file_name]["status"] = "no change"
                self.write_area()
                
                print("changes undone")
                
                return True
        
        
        self.new_shell[file_name] = {"hash":hash_value, "mode": 100644, "status": "modified"}
        self.write_area()
        
        print("200: updates was tracked successfully")
        
        return True

                
    def build(self, message):
        
        if self.directory_path.get_path() == None:
            print("error404: repo not found")
            return False
        
        is_changed = False
        for file_meta_data in self.new_shell.values():
            if file_meta_data["status"] != "no change":
                is_changed = True
                break
        
        if not is_changed:
            print("no changes lately")
            return False
        
        new_shell_tree = Tree(name = "", directory_path = self.directory_path.get_path(), path = self.directory_path.get_path())
        
        for file_name, file_meta_data in self.new_shell.items():
            
            file_hash_ = file_meta_data["hash"]
            file_path = self.directory_path.get_path().joinpath(f"{file_name}").relative_to(self.directory_path.get_path())
            
            new_shell_tree.iterate_path(file_path, file_hash_)
        
        new_shell_tree.create()
        new_shell_tree_hash = new_shell_tree.get_hash()
        
        current_shell_tree_hash = self.current_portal.get_current_shell_hash()
        
        new_shell = Shell(message = message, tree_hash = new_shell_tree_hash, parent_hash = current_shell_tree_hash, user = self.user, directory_path = self.directory_path.get_path())

        new_shell.create()
        
        new_shell_hash = new_shell.get_hash()
        
        self.current_portal.set_current_pointer(new_shell_hash)
        
        self.area_path.unlink()
        
        self.create()
        
        print("200: updates was built successfully")
        
        return True

    
    def show_status(self):
        
        if self.directory_path.get_path() == None:
            print("error404: repo not found")
            return False
        
        all_files = self.list_all_files()
        
        under_construction_files = []
        modified_files = []
        not_tracked_files = []
        
        for file_path in all_files:
            file_object = File(path = file_path, directory_path = self.directory_path.get_path())
            file_name = file_object.get_name()
            
            if file_name not in self.new_shell:
                not_tracked_files.append(file_name)
                continue
            
            # fileBlobContent = createFileBlobContent(file_name)
            # fileHashHex = hashFileBlobContent(fileBlobContent)
            file_object.create_block_content()
            file_object.hash_block_content()
            
            file_hash = file_object.get_hash()
            
            if file_hash != self.new_shell[file_name]["hash"]:
                modified_files.append(file_name)
            
            if self.new_shell[file_name]["status"] != "no change":
                under_construction_files.append(file_name)
        
        # print(f"1{under_construction_files}")
        # print(f"2{modified_files}")
        # print(f"3{not_tracked_files}")
        
        current_portal = self.current_portal.get_current_portal()
        print(f"current portal {current_portal}")
        
        if under_construction_files:
            print("\nto be built files: ")
            for file in under_construction_files:
                print(file)
        
        
        if modified_files:
            print("\nupdates: ")
            for file in modified_files:
                print(file)
        
        
        if not_tracked_files:
            print("\ncreated but not tracked files: ")
            for file in not_tracked_files:
                print(file)
        return True
        
    
    def list_all_files(self):
        output = []
        all_pathes = self.directory_path.get_path().relative_to(self.directory_path.get_path()).glob('**/*')
        for path in all_pathes:
            
            if not path.is_file():
                continue
            
            if str(path)[0] == '.':
                continue
            
            output.append(path)
         
        return output
    
    
    def write_area(self):
        area_object = {"current_shell": self.current_shell, "new_shell": self.new_shell}

        with open(self.area_path, "w") as json_handle:
            json.dump(area_object, json_handle)
        
        return True
    
    
    def read_area(self):
        with open(self.area_path, "r") as json_handle:
            area_object = json.load(json_handle)

        self.current_shell = area_object["current_shell"]
        
        self.new_shell = area_object["new_shell"]
        
        return True

    
    def __set_area_path(self):
        if self.directory_path.get_path() == None:
            return None
        
        return self.directory_path.get_path().joinpath(".shed/UNDER_CONSTRUCTION_AREA")


    def show_difference(self):
        
        # read every file in new_shell
        # create a File object for this file with the given hash and path
        # the File class can read the compressed objec from the hash and the modified content
        # use diff lib to compare betweeen the two versions(create my own vresion of diff later)
        
        for file_name, file_meta_data in self.new_shell.items():
            # if file_meta_data["status"] != "modified":
            #     continue
            
            file_path = self.directory_path.get_path().joinpath(file_name)
            file_object = File(path = file_path, directory_path = self.directory_path.get_path(), hash_ =file_meta_data["hash"])
            print(file_object.get_difference())
        return

    
# B = UnderConstructionArea()
# B.show_difference()
# B.create()
# # test_path = Path("source/user.py")
# # # print(test_path.exists())
# print(B.current_shell)
# print(B.new_shell)

# # print("/////////////////////////////////////")
# # B.add_file(test_path)
# # # print(B.current_shell)
# # # print(B.new_shell)
# # B.build("jhj")

# B.show_status()