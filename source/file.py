from block import Block
import hashlib, zlib

class File(Block):
    def __init__(self, *args, **kwargs):
        
        
        self.path = kwargs.get("path", None)
        
        self.directory_path = kwargs.get("directory_path", None)
        
        self.__hash = kwargs.get("hash_", None)
        
        self.block_content = None
        
        self.__name = str(self.path.resolve().relative_to(self.directory_path))
    
    def read(self):
        return
    
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
        