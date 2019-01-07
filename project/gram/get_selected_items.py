#!user/bin/env python
#encoding:utf8
#!@tiem:2018/12/24 15:06
#!@filename:get_selected_items_new.py

import os
import json
import configparser

os.chdir('../')
def readjson(path):
    fp=path
    if os.path.exists(fp):
        try:
            with open(fp,'r',encoding='utf8') as f:
                fj=json.load(f)
        except Exception as e:
            print(e)
    else:
        print('程序中断，%s 文件不存在，请重新检查' % fp)
    return fj

if os.path.exists('config.ini'):
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        page1_selected = eval(config.get('Page_Selected_Info', 'page1_selected'))
        page2_selected = eval(config.get('Page_Selected_Info', 'page2_selected'))
    except Exception as e:
        print(e)
        print('程序中断，请检查config.ini文件')
    else:
        if len(page1_selected)!=0 and len(page2_selected)!=0:
            selected_item = []
            not_in_core=[]
            for i in page1_selected:
                if i in os.listdir("vocab/"):
                    path = "vocab/" + page1_selected[0] + "/" + "core.json"
                    try:
                        core_json = readjson(path)
                    except Exception as e:
                        print(e)
                        print("程序中断，%s 文件存在问题，请检查。"% path)
                    else:
                        for j in page2_selected:
                            for m in core_json:
                                if j == m['id']:
                                    selected_item.append(m)
                                else:
                                    not_in_core.append(j)
                        if len(selected_item)!= 0 :
                            with open('tmp_files/selected_items.json', 'w', encoding='utf8') as fw:
                                try:
                                    json.dump(selected_item, fw, ensure_ascii=False)
                                except Exception as e:
                                    print(e)
                                    print("程序中断，selected_items.json文件未完成写入,请检查。")
                                else:
                                    print("selected_items.json 文件写入完成。")
                                    # if len(not_in_core) !=0:
                                    #     print("%s 这些参数不在%s文件中，未写入。"%(set(not_in_core),path))

                        else:
                             print("程序中断，参数selected_items为空，未完成写入，请检查。")
                else:
                    print("在vocab文件夹中没有找到%s,请检查。"%i)
        else:
            print('%s or %s 中没有参数，请检查'%("page1_selected","page2_selected"))
else:
    print('config.ini 文件不存在！请仔细检查。')




