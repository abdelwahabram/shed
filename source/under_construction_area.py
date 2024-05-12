from directory_path import DirectoryPath
from current_portal import CurrentPortal
from file import File
from pathlib import Path

from tree import Tree
class UnderConstructionArea:
    def __init__(self):

        self.current_shell = {}

        self.new_shell = {} 

        self.directory_path = DirectoryPath()

        self.area_path = self.__set_area_path()

        self.current_portal = CurrentPortal(self.directory_path.get_path())
    

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
        
        file_object = File(directory_path = self.directory_path.get_path(), path = file_path)
        
        file_object.create()
        
        hash_value = file_object.get_hash()
        
        file_name = file_object.get_name()
        
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

                
    def build(self):
        pass

    def write_area(self):
        pass

    def read_area(self):
        pass

    def __set_area_path(self):
        if self.directory_path.get_path() == None:
            return None
        
        return self.directory_path.get_path().joinpath(".shed/UNDER_CONSTRUCTION_AREA")


B = UnderConstructionArea()
B.create()
test_path = Path("source/tree.py")
print(test_path.exists())
print(B.current_shell)
print(B.new_shell)

print("/////////////////////////////////////")
B.add_file(test_path)
print(B.current_shell)
print(B.new_shell)