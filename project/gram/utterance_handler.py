import json
import random

import re


class UtteranceHandler:
    """
    完成替换句型中的参数的功能
    """

    def __init__(self, type_name, json_path):
        """
        :param type_name: 类型名
        :param json_path: Json文件名
        """
        self.type_name = type_name
        self.json_path = json_path

    def get_param_list(self, param_name):
        """
        -工具方法-
        读取vocab文件，并转换为一个vocab列表
        """
        # print('正在对{param_name}的vocab进行处理'.format(param_name=param_name))
        param_list = []

        with open('../vocab/{type_name}/{file_name}.json'.format(file_name=param_name, type_name=self.type_name), 'r',
                  encoding='utf-8') as param_vocab:
            try:
                all_params = json.load(param_vocab)
            except ValueError:
                raise NameError('请检查vocab文件{param_name}.json的格式和编码'.format(param_name=param_name))

        for item in all_params:
            param_list.extend(item["word"])

        while '' in param_list:
            param_list.remove('')
        random.shuffle(param_list)
        return param_list

    def get_param(self, param_list, param_name):
        """
        -*-工具方法-*-
        检查参数列表并从参数列表中弹出需要的参数
        """
        if len(param_list) == 0:
            param_list = self.get_param_list(param_name)
            if len(param_list) == 0:
                raise NameError('{param_name}的vocab文件中没有获取到任何值，请检查文件'.format(param_name=param_name))
        return param_list.pop()

    def replace_param(self, utt, param_name, param_dict, tc_mode):
        """
        -*-逻辑方法-*-
        完成对句子中参数的 单次 替换
        """
        if not tc_mode:
            key = self.get_param(param_dict, param_name)
        else:
            key = '({param})|{param_name}|'.format(param=self.get_param(param_dict, param_name), param_name=param_name)
        param_mark = '[{param_name}]'.format(param_name=param_name)
        utt = utt.replace(param_mark, key, 1)
        return utt

    def construct_json(self, tc_mode):
        result_json = []
        with open(self.json_path, 'r', encoding='utf-8') as a_output:
            unhandled_data = json.load(a_output)

        # 第一层
        for goal_layer in unhandled_data:
            goal_dict = dict()
            goal_dict["GoalID"] = goal_layer["GoalID"]
            goal_dict["playByCategory"] = goal_layer["playByCategory"]

            # 第二层
            main_case = []
            for utt_layer in goal_layer["mainCase"]:
                utt_dict = dict()
                utt_dict["name"] = utt_layer["name"]

                # 第三层
                utt_dict["variation"] = []
                param_list = re.findall('\[(.*?)\]', utt_dict["name"])
                used_param_list = []
                utt_dict["variation"] = utt_layer["variation"]

                # 是否无参数
                if len(param_list) != 0:
                    for param_name in param_list:
                        # 是否有相同参数
                        if param_name not in used_param_list:
                            new_list = []
                            param_dict = self.get_param_list(param_name)
                            count = param_list.count(param_name)
                            for utt in utt_dict["variation"]:
                                for i in range(count):
                                    utt = self.replace_param(utt, param_name, param_dict, tc_mode)
                                new_list.append(utt)
                            utt_dict["variation"] = new_list
                            used_param_list.append(param_name)
                        else:
                            continue
                else:
                    pass
                main_case.append(utt_dict)
                goal_dict["mainCase"] = main_case
            result_json.append(goal_dict)
        return result_json


def utterance_output(type_name, json_path, tc_mode):
    utterance_handler = UtteranceHandler(type_name, json_path)
    result = utterance_handler.construct_json(tc_mode)
    return result


# print(utterance_output('qingtingFM', '../tmp_files/prefixOutput.json', tc_mode=True))
