#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:54:18 2018

@author: samsung
"""
import os 


def excute_script():
   print('excution is start:')
   os.system('python3 jenkins_to_config.py')
   os.system('python3 get_selected_items.py')
   os.system('python3 uttModel.py')
  # os.system('python3 json_to_xlsx.py')   
if __name__=="__main__":
    excute_script()
    
