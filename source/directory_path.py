import os, pathlib


class DirectoryPath:
    def __init__(self):
        self.__directory_path = None
        self.__find()
        return

    def __find(self):
        current_path = pathlib.Path()

        while True:

            repository_path = current_path.joinpath(".shed")

            if repository_path.exists():
                self.__directory_path = current_path.resolve()
                return True
            
            # if this is a mounting point(aka: the root of the file system or a partition): return false
            if os.path.ismount(current_path):

                return False

            current_path = current_path.parent.resolve()
        return False

    def get_path(self):
        return self.__directory_path

    
    def set_path(self, path):
        self.__directory_path = path.resolve()
