from source.block import Block
from source.time_ import Time
from pathlib import Path
import zlib, hashlib


class Shell(Block):
    
    def __init__(self, *args, **kwargs):
        self.__message = kwargs.get("message", None)
        
        self.__tree_hash = kwargs.get("tree_hash", None)
        
        self.__parent_hash = kwargs.get("parent_hash", None)
        
        self.__user = kwargs.get("user", None)
        
        self.__time = Time()
        
        self.__directory_path = kwargs.get("directory_path", None)
        
        self.__hash = kwargs.get("hash", None)
        
        self.__block_content = None
        
    
    def read(self):
        pass
    
    def create(self):
        self.create_block_content()
        self.hash_block_content()
        self.store_block_content()
    
    
    def create_block_content(self):
                
        parent = f"parent {self.__parent_hash}\n" if self.__parent_hash else ""
        
        current_time = self.__time.get_time()

        body = bytes(f"tree {self.__tree_hash}\n{parent}author {self.__user.get_name()} <{self.__user.get_email()}> {current_time} {self.__time.get_time_zone_offset()}\ncommitter {self.__user.get_name()} <{self.__user.get_email()}> {current_time} {self.__time.get_time_zone_offset()}\n\n{self.__message}\n", 'utf-8')

        header = bytes(f"commit {len(body)}", 'utf-8') + b"\x00"
        
        self.__block_content = header + body
        
        return True
    
    
    def hash_block_content(self):
        
        hash_object = hashlib.sha1(self.__block_content)
        
        self.__hash = hash_object.hexdigest()
        
        return True

    
    def store_block_content(self):
        
        block_path = self.__directory_path.joinpath(f".shed/blocks/{self.__hash}")
        
        if not block_path.exists():
            compressed_content = zlib.compress(self.__block_content)
            
            with open(block_path, "wb") as block_handle:
                block_handle.write(compressed_content)
        
        return True
    
    
    def get_hash(self):
        return self.__hash