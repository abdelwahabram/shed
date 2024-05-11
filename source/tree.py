from block import Block
from pathlib import Path
import zlib

class Tree(Block):
    
    def __init__(self, *args, **kwargs):
        
        self.name = kwargs.get('name', None)
        
        self.mode = kwargs.get('mode', None)
        
        self.hash_ = kwargs.get('hash_', None)
        
        self.directory_path = kwargs.get('directory_path', None)
        
        self.content = {}
        
        self.path = kwargs.get('path', None)
        

    def read(self):

        tree_hash_path = self.directory_path.joinpath(f".shed/blocks/{self.hash_}")

        with open(tree_hash_path, "rb") as tree_handle:
            compressed_tree_content = tree_handle.read()
        
        tree_content = zlib.decompress(compressed_tree_content)
        first_line, tree_content = tree_content.split(b"\x00", 1)

        while tree_content:
            
            content_mode, tree_content = tree_content.split(b" ", 1)
            content_mode = content_mode.decode()
            
            content_name, tree_content = tree_content.split(b"\x00", 1)
            content_name = content_name.decode()

            content_hex_hash, tree_content = tree_content[:20].hex(), tree_content[20:]

            content_path = self.path.joinpath(content_name).resolve().relative_to(self.directory_path)

            if content_mode == "100644":
                self.content[content_name] = [str(content_path), content_mode, content_hex_hash]
                continue
            
            content_tree = Tree(name = content_name, mode = content_mode, hash_ = content_hex_hash, directory_path = self.directory_path, path = content_path)
            self.content[content_name] = content_tree
            
            content_tree.read()


    def traverse_content(self):
        content_list = []
        for name, item in self.content.items():
            
            if type(item) == list:
                content_list.append(item)
                continue

            content_list += item.traverse_content()

        return content_list

 
    def create(self):
        pass


