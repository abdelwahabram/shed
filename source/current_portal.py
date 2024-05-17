from pathlib import Path
import zlib


class CurrentPortal:
    def __init__(self, repository_path: Path):
        self.repository_path = repository_path


    def get_current_portal_tree_hash(self):
        current_shell_hash = self.get_current_shell_hash()
    
        if current_shell_hash == "":
            # if this is a fresh repository with no commits before
            return False

        current_shell_path = self.repository_path.joinpath(f".shed/blocks/{current_shell_hash}")

        # later we might leave this to the shell class read method
        with open(current_shell_path, "rb") as current_shell_handle:
            compressed_current_shell_content = current_shell_handle.read()
        

        current_shell_content = zlib.decompress(compressed_current_shell_content).decode()
        
        first_line, current_shell_content = current_shell_content.split("\n", 1)

        tree_hash = first_line[-40:]

        return tree_hash

    def get_current_shell_hash(self):

        current_portal = self.get_current_portal()

        current_pointer_path = self.repository_path.joinpath(f".shed/{current_portal}")

        with open(current_pointer_path, "r") as current_shell_handle:
            current_shell = current_shell_handle.readline()

        return current_shell[:-1]
        

    def get_current_portal(self):
        current_portal_path = self.repository_path.joinpath(".shed/CUR_PORTAL")

        with open(current_portal_path, "r") as current_portal_handle:
            current_portal = current_portal_handle.readline()[5:-1]
        
        return current_portal

    def set_current_pointer(self, ptr):
        current_portal = self.get_current_portal()
        current_pointer_path = self.repository_path.joinpath(f".shed/{current_portal}")
        
        with open(current_pointer_path, "w") as current_pointer_handle:
            current_pointer_handle.write(f"{ptr}\n")
            
        return True