from source.block import Block
from pathlib import Path
import zlib, hashlib

class Tree(Block):
    
    def __init__(self, *args, **kwargs):
        
        self.name = kwargs.get('name', None)
        
        self.mode = kwargs.get('mode', None)
        
        self.hash_ = kwargs.get('hash_', None)
        
        self.directory_path = kwargs.get('directory_path', None)
        
        self.content = {}
        
        self.path = kwargs.get('path', None)
        
        self.block_content = None
        

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

            content_path = self.path.joinpath(content_name).resolve().relative_to(self.directory_path.resolve())

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
        for content_object in self.content.values():
            if not content_object.is_file():
                content_object.create()
        self.create_block_content()
        self.hash_block_content()
        self.store_block_content()
        return True

    
    def test(self):
        print(f"{self.name}   {self.mode}")
        for item in self.content.values():
            item.test()

    
    def iterate_path(self, path, hash_, level = 0):
        # iterate a given path and add it to the contents of the tree recursively
        # the path given is relative to the directory path
        # the mother tree has the same path as the dir path

        # print(level, path)
        # base
        if self.path.is_file():
            self.hash_ = hash_
            self.mode = "100644"
            return True
        
        if len(path.parts) == level:
            print("no leafs to be added")
            return False
        
        self.mode = "40000"
        content_name = path.parts[level]
        content_path = self.path.joinpath(content_name)
        
        
        # recursive
        if content_name not in self.content:    
            self.content[content_name] = Tree(name = content_name, directory_path = self.directory_path, path = content_path)

        return self.content[content_name].iterate_path(path, hash_, level + 1)
        
    
    def create_block_content(self):
        header = bytes()
        body = bytes()
        
        for content_name, content_object in self.content.items():
            content_hash_ = content_object.get_hash_bytes()
            content_mode = content_object.get_mode()
            
            content_line = bytes(f"{content_mode} {content_name}\0",'utf-8') + content_hash_
            body += content_line
        
        header = bytes(f"tree {len(body)}\x00", 'utf-8')
        
        self.block_content = header + body
        return True

    
    def hash_block_content(self):
        
        hash_object = hashlib.sha1(self.block_content)
        
        self.hash_ = hash_object.hexdigest()
        
        return True

    
    def store_block_content(self):
        
        block_path = self.directory_path.joinpath(f".shed/blocks/{self.hash_}")
        
        if not block_path.exists():
            compressed_content = zlib.compress(self.block_content)
            
            with open(block_path, "wb") as block_handle:
                block_handle.write(compressed_content)
        
        return True

    
    def get_hash_bytes(self):
        return bytes().fromhex(self.hash_)

    
    def get_mode(self):
        
        return self.mode    


    def is_file(self):
        return self.path.is_file()

    
    def get_hash(self):
        return self.hash_
    
    
# A = Tree(name = "", directory_path = Path(), path = Path())
# # print(Path().resolve())
# P = Path("old/zzzz/kkkk/m")
# print(P.exists())
# print(P)

# print(A.iterate_path(P, "3f7b0e3b8cb9cb019b45f629c30e8fc0cfda29eb", 0))

