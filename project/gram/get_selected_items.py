# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 16:32:32 2018

@author: samsung
"""

#!/usr/bin/env python
import os 
import json
import configparser

# change current path 
os.chdir(r'../')

#get the selected info 
#
# page1_selected=['music']
# page2_selected=["playBySinger","playBySong"]

config = configparser.ConfigParser()
config.read('config_test.ini')
page1_selected = eval(config.get('Page_Selected_Info', 'page1_selected'))
page2_selected = eval(config.get('Page_Selected_Info', 'page2_selected'))

#creat read json function
def readjson(path):
    file = open(path, "r",encoding='utf-8')
    filejson = json.load(file)
    file.close()
    return (filejson)

#get selected items from core.json
selected_item = []
for i in page1_selected:
    path = "vocab/" + page1_selected[0] + "/" + "core.json"
    core_json = readjson(path)
    for j in page2_selected:
        for m in core_json:    
            if j ==m['id']:
                selected_item.append(m)

#save selected_items as selected_items.json file
with open('tmp_files/selected_items.json','w') as fw:
   json.dump(selected_item,fw,ensure_ascii=False)
   print('done!')
    
