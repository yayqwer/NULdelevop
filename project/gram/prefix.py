import random as Rd
import json
import configparser


config = configparser.ConfigParser()
config.read('../config_test.ini')
page1_selected = eval(config.get('Page_Selected_Info', 'page1_selected'))
page3_selected = eval(config.get('Page_Selected_Info', 'page3_selected'))

#文件路径
appendix = r"../vocab/"+page1_selected[0]+"/appendix.json"
core = r"../tmp_files/selected_items.json"
outpt = r"../tmp_files/prefixOutput.json"

#设置随机函数 输入n随机返回一个0-n的整数
def rando(n):
    n = n -1
    num = Rd.randint(0,n)
    return num

#获取前后缀文件函数
def appendixJson(path):
    appendixLiet = {}
    with open(path,"r") as file:
        fileJson = json.load(file)
        length =  len(fileJson)
        for i in range(length):
            fileJsonL = fileJson[i]
            num = fileJsonL["number"]
            appendixLiet[num] = fileJsonL["word"]
    return appendixLiet  #格式字典存储Key = number ,Value = []

#获取配置文件
def GetConfiguration():
    pass

#前后缀选取原则当传入参数
def RandomSampling(random,Value):     #传入参数为随机抽取的个数
    length = len(Value)
    if random <= length:
        xx = []
        for i in range(random):
            n = rando(length)
            xx.append(Value[n])
    else:
        n = random - length
        xx = Value
        for j in range(n):
            n = rando(length)
            xx.append(Value[n])
    return xx


#统计前后缀数量和配置文件中获取的生成数量比较。如果前后缀数>配置文件数（执行随机抽取）
#如果前后缀<配置文件数（超出部分执行随机抽取，未超出部分执行前后缀全文档遍历确保句式丰富）
def StatisticalPrefix(n):#传入参数n为配置文件中勾选的要生成的数量
    x = appendixJson(appendix)
    Value = []
    num = 0
    for i in x:
        num = num +len(x[i])
        for j in x[i]:
            Value.append(j)
    a = RandomSampling(n,Value)
    return a
# StatisticalPrefix(6)  #返回需要的前后缀库列表[x,x,x]



#读取主句文件函数  Filetype 取值1代表ID 2代表 word 3代表mianCase 4代表每个主句的个数
def resolveJson(path):
    with open(path,"r") as file:
        x = []
        list_id = []
        list_word = []
        list_mainCase = []
        list_num = []
        fileJson = json.load(file)
        for i in range(len(fileJson)):
            fontFamily = fileJson[i]
            id = fontFamily["id"]
            word = fontFamily["word"]
            mainCase = fontFamily["mainCase"]
            list_id.append(id)
            list_word.append(word)
            list_num.append(len(mainCase))
            for j in range(len(mainCase)):
                list_mainCase.append(mainCase[j])
        x.append(list_id)
        x.append(list_word)
        x.append(list_num)
        x.append(list_mainCase)
        return x       #返回列表[[id],[word],[num],[mainCase]

#将每条主句与前后缀结合
#参数说明 StatisticalPrefix为前后缀结合列表，resolveJson为主句结合列表
def integration(StatisticalPrefix,resolveJson):
    newList = []
    for i in resolveJson[3]:
        # StatisticalPrefix = StatisticalPrefix(10)
        langthS = len(StatisticalPrefix)
        for j in StatisticalPrefix:
            x = rando(langthS)
            k = StatisticalPrefix[x]
            a = k.split(":")
            langth = len(a)
            if langth == 1:
                tag = a[0] + i
            else:
                tag = a[0] + i + a[1]
            newList.append(tag)
    return newList   #返回匹配好前后缀的列表

#StatisticalPrefix = StatisticalPrefix(20)
#resolveJson = resolveJson(core)
#listAll = integration(StatisticalPrefix,resolveJson)
# print (resolveJson[0])
# print (resolveJson[1])
# print (resolveJson[2])
# print (resolveJson[3])
# print (listAll)

# 生成json文件  jsonStr = json.dumps(data)
def outputJson(name,main,fenlei,num,extend,n,path):
    #参数说明
    #name--->领域名称
    #main--->主句
    #fenlei->分类名称
    #num---->每个分类下有几个主句
    #extend->扩展(打算传入一个扩展好的全部列表用分割来取值)#
    #n------>传入扩展条数用于分割extend用
    langth = len(name)
    p = 0
    mun = 0
    shuzi = n
    test = []
    for i in range(langth):
        training = {}
        #training[name[i]] = fenlei[i]
        training["GoalID"] = name[i]
        training["playByCategory"] = fenlei[i]
        training["mainCase"] = []
        langtha = num[i]
        for j in range(langtha):
            voc = {}
            voc["name"] = main[mun]
            mun = mun + 1
            voc["variation"] = extend[p:n]
            p = p + shuzi
            n = p + shuzi
            training["mainCase"].append(voc)
        test.append(training)
    jsonStr = json.dumps(test,ensure_ascii=False)
    #print(jsonStr)
    with open(path,"w",encoding="utf-8") as file:
        file.write(jsonStr) 
#outputJson(resolveJson[0],resolveJson[3],resolveJson[1],resolveJson[2],listAll,20,outpt)

def Interface_file():
    global StatisticalPrefixx
    global resolveJsonx
    n = int(page3_selected[0])
    StatisticalPrefixx = StatisticalPrefix(n)
    resolveJsonx = resolveJson(core)
    listAll = integration(StatisticalPrefixx, resolveJsonx)
    outputJson(resolveJsonx[0], resolveJsonx[3], resolveJsonx[1], resolveJsonx[2], listAll, n, outpt)
Interface_file()
print ("prefix.py excution is completed!")
print('-'*50)


