#!usr/bin/env python
#encoding: utf-8
"""
Created on Mon Dec 10 14:54:18 2018

@author: samsung
"""
import os 


def excute_script():
   print('excution is start:')
   try:
       os.system('python3 jenkins_to_config.py')
   except Exception as error1:
        print("jenkins_to_config.py执行错误:")
        print(error1)
   else:
        print("jenkins_to_config.py程序执行完成。")
        try:
            os.system('python3 get_selected_items.py')
        except Exception as error2:
            print("get_selected_items.py执行错误:")
            print(error2)
        else:
            print("get_selected_items.py程序执行完成。")
            try:
                os.system('python3 uttModel.py')
            except Exception as error3:
                print("uttModel.py执行错误:")
                print(error3)
            else:
                print("uttModel.py程序执行完成。")
                print('全部程序已执行完毕。')




  # os.system('python3 json_to_xlsx.py')   
if __name__=="__main__":
    excute_script()
    
