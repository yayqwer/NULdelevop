import random as Rd
import json

#文件路径
appendix = r"vocab/music/appendix.json"
core = r"vocab/music/core.json"
outpt = r"out/prefixOutput.json"

#设置随机函数 输入n随机返回一个0-n的整数
def rando(n):
    n = n -1
    num = Rd.randint(0,n)
    return num

#获取前后缀文件函数
def appendixJson(path):
    appendixLiet = {}
    with open(path,"rb") as file:
        fileJson = json.load(file)
        print(type(fileJson))
        length =  len(fileJson)
        for i in range(length):
            fileJsonL = fileJson[i]
            num = fileJsonL["number"]
            appendixLiet[num] = fileJsonL["word"]
    return appendixLiet  #格式字典存储Key = number ,Value = []

print(appendixJson(appendix))

# with open(r"vocab/music/appendix.json","rb") as f:
#     file_json = json.load(f)
#     print(file_json)
#     print(type(file_json))