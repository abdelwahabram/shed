from pathlib import Path
import json
class User:
    def __init__(self, *args, **kwargs):
        
        self.__name = kwargs.get("name", None)
        
        self.__email = kwargs.get("name", None)
        
        self.__directory_path = kwargs.get("directory_path", None)
        
        if self.__name != None and self.__email != None:
            self.store_user_data()
            return
        self.load_user_data()
    
    def get_name(self):
        return self.__name
    
    def get_email(self):
        return self.__email
    
    def set_name(self, name):
        self.__name = name
        return self.store_user_data()
        
    def set_email(self, email):
        self.__email = email
        return self.store_user_data()
    
    
    def load_user_data(self):
        if self.__directory_path == None:
            print("error404: repo doesn't exist")
            return False
        
        user_configuration_path = self.__directory_path.joinpath(".shed/userconf")
        if not user_configuration_path.exists():
            return False
        
        with open(user_configuration_path, "r") as user_configuration:
            user = json.load(user_configuration)
        
        self.__name = user["name"]

        self.__email = user["email"]
        
        return True
    
    def store_user_data(self):
        
        if self.__directory_path == None:
            print("error404: repo doesn't exist")
            return False
        
        user_configuration_path = self.__directory_path.joinpath(".shed/userconf")
        user = {"name": self.__name, "email": self.__email}

        with open(user_configuration_path, "w+") as user_configuration:
            json.dump(user, user_configuration)
            
        return True

# A = User(directory_path = Path())

# print(A.get_name())

# A.set_name("bebo")

# print(A.get_name())