import os
p1 = '/folderA/folderB/folderC/folderE'
p2 = '/folderA/folderB/folderC/folderD/test.py'

print(os.path.join(p1,os.path.basename(p2)))
print(os.path.basename(p2))
