# python批量更换后缀名
import os
import sys
os.chdir(r'C:\Users\69081\Desktop\1')

# 列出当前目录下所有的文件
files = os.listdir('./')
print(files)

for fileName in files:
	portion = os.path.splitext(fileName)
	# 修改文件后缀为jpg
	if portion[1] == ".gif":
		newName = portion[0] + ".jpg"
		os.rename(fileName, newName)
