import hashlib
import zlib
# a = hashlib.sha1("hello".encode())
# print(a)
# a.hashlib.

# hexa = "68bc17f9ff2104a9d7b6777058bb4c343ca72609"

# r = bytes.fromhex(hexa)
# g = 5
# header = f"tree {g}\n"
# h = bytes(header, 'utf-8')
# print(h + r)
# print(r)

# objs = [".git/objects/3a/f7257939102e630a0a689e6444e4db5300a594",
#     ".git/objects/7c/66d9f66ddce80278afe5577874798bd32b42c4",
#     ".git/objects/86/87f3f82ed15e37fa584cc6693014843f3ca82f",
#     ".git/objects/ad/601ca799156b8ae4703d2e5939b479eb6e3e67",
#     ".git/objects/c0/74a2b09555fdbaec98c07f92d4effeba5217c8",
#     ".git/objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391"

# ]
# for obj in objs:
#     with open(obj, "rb") as f:
#         f = f.read()
#         data = zlib.decompress(f)
#         print(data)

# obj = ".git/objects/1f/1f32aa42956b4b656aeffc3726d43be686a662"
# obj =".shed/shells/3af7257939102e630a0a689e6444e4db5300a594"
obj = ".git/objects/ac/601ca799156b8ae4703d2e5939b479eb6e3e67"

with open(obj, "rb") as f:
    f = f.read()
    data = zlib.decompress(f)
    print(data)