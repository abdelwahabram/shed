import os

class RepositoryInitializer:
    def __init__(self):
        self.initialize()
    def initialize(self):
        dirs = ['.shed', '.shed/shells', '.shed/portals', ]
        for dir in dirs:
            os.mkdir(dir)
        currentBranch = open(".shed/CUR_PORTAL", "w")
        currentBranch.close()
        staging = open(".shed/UNDER_CONSTRUCTION_AREA", "w")
        staging.close()

print("changes to be tracked")
print("changes to be trackedagain")
print("changes to be trackedagainagain")
A = RepositoryInitializer()
