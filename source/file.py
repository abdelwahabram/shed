from source.block import Block
import hashlib, zlib
from difflib import unified_diff

class File(Block):
    def __init__(self, *args, **kwargs):
        
        
        self.path = kwargs.get("path", None)
        
        self.directory_path = kwargs.get("directory_path", None)
        
        self.__hash = kwargs.get("hash_", None)
        
        self.block_content = None
        
        self.__name = str(self.path.resolve().relative_to(self.directory_path))
    
    def read(self):
        block_path = self.directory_path.joinpath(f".shed/blocks/{self.__hash}")
        
        with open(block_path, "rb") as block_handle:
            compressed_content = block_handle.read()
        
        

        content = zlib.decompress(compressed_content).decode('utf-8')
        
        output = content.split('\n', 1)
        
        content = output[1] if len(output) == 2 else ""
        
        return content
    
    def create(self):
        self.create_block_content()
        self.hash_block_content()
        self.store_block_content()
            
    
    def create_block_content(self):
        with open(self.path, "r") as file_handle:
            file_content = file_handle.read()
        
        header = f"blob {len(file_content.encode('utf-8'))}\0"
        
        self.block_content = bytes(header + file_content, 'utf-8')
        
        return True
    
    def hash_block_content(self):
        
        hash_object = hashlib.sha1(self.block_content)
        
        self.__hash = hash_object.hexdigest()
        
        return True
    
    def store_block_content(self):
        
        block_path = self.directory_path.joinpath(f".shed/blocks/{self.__hash}")
        
        if not block_path.exists():
            compressed_content = zlib.compress(self.block_content)
            
            with open(block_path, "wb") as block_handle:
                block_handle.write(compressed_content)
        
        return True


    def get_hash(self):
        return self.__hash
    
    def get_name(self):
        self.__name = str(self.path.resolve().relative_to(self.directory_path))
        return self.__name          


    def get_difference(self):
        
        before_content = self.read()
        after_content = self.read_from_disk()
        
        difference = unified_diff(before_content.splitlines(keepends = True), after_content.splitlines(keepends = True), fromfile = f"{self.__name}:before", tofile = f"{self.__name}:after", lineterm = "\n")       
        return '\n'.join(list(difference))
    
    
    def read_from_disk(self):
        with open(self.path, "r") as file_handle:
            content = file_handle.read()
        return content