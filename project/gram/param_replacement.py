import json
import random
import re


class UtteranceHandler:
    """
    完成替换json中句型的参数的功能，主要参与的方法为：
    get_param: 从参数字典里面获取参数（不放回抽样）
    replace_param: 替换句中参数
    generate_json: 读取解析旧Json文件并构建新Json文件
    """

    def __init__(self, type_name, json_path):
        """
        :param type_name: 类型名
        :param json_path: Json文件名
        """
        self.key_index = '0'
        self.type_name = type_name
        self.json_path = '../out/{json_path}.json'.format(json_path=json_path)

    def get_param_dict(self, param_name):
        """
        -工具方法-
        读取vocab文件，并转换为一个vocab字典
        :param param_name: 具体文件名，如album，singer，song...
        :return: vocab字典，{'1':[],'2':[],'3':[],...}
        """
        param_dict = {}

        with open('../vocab/{type_name}/{file_name}.json'.format(file_name=param_name, type_name=self.type_name), 'r') \
                as jsf:
            all_params = json.load(jsf)

        for item in all_params:
            param_dict[item['number']] = item['word']

        return param_dict

    def get_random_number(self, param_dict):
        """
        -工具方法-
        依据参数字典自动产生随机数，用于随机取参数的字数
        :param param_dict:参数字典
        :return:一个随机数，取值范围为vocab
        """
        key_list = list(param_dict.keys())
        num_min = int(min(key_list))
        num_max = int(max(key_list))
        randnum = str(random.randint(num_min, num_max))

        while randnum == self.key_index:
            randnum = str(random.randint(num_min, num_max))
        return randnum

    def dict_content_check(self, param_dict_old, param_name):
        """
        -工具方法-
        参数字典检查，当遇到参数对应字数列表长度为0（全部弹出完毕）的情况下，重新获取参数字典。
        :param param_dict_old: 旧的参数字典
        :param param_name: 参数名
        :return: 返回一个参数字典
        """
        if len(param_dict_old[str(self.key_index)]) == 0:
            param_dict_new = self.get_param_dict(param_name)
            # 以下情况是更换后列表长度仍然为0（代表原本就没有值），此时对随机数进行更换
            if param_dict_new[str(self.key_index)] == 0:
                self.key_index = self.get_random_number(param_dict_old)
                return param_dict_old
            return param_dict_new
        return param_dict_old

    @staticmethod
    def get_param_name(utt):
        """
        -工具方法-
        接受句型，返回参数名
        :param utt: 句型
        :return: 参数名
        """
        param_list = re.findall('\[(.*?)\]', utt)
        return param_list

    def get_param(self, param_dict, param_name):
        """
        -*-逻辑方法-*-
        随机取出参数字典中需要的参数
        :param param_dict: 参数字典
        :param param_name: 参数vocab名
        :return: 参数本身
        """
        self.key_index = self.get_random_number(param_dict)
        if len(param_dict[str(self.key_index)]) == 0:
            param_dict = self.dict_content_check(param_dict, param_name)
        # 打乱参数列表的顺序
        for key, value in param_dict.items():
            random.shuffle(value)
        # 不放回取出参数
        param = param_dict[str(self.key_index)].pop()
        if param == '':
            return self.get_param(param_dict, param_name)
        else:
            return param

    def replace_param(self, utt, param_name, param_dict, replace_num=-1):
        """
        -*-逻辑方法-*-
        接受utt，和需要替换的参数vocab名，返回替换后的句子
        :param utt: 待替换句
        :param param_name: 参数名
        :param param_dict: 参数字典
        :param replace_num: 替换次数
        :return: 替换好的句子
        """
        param = self.get_param(param_dict, param_name)
        param_mark = '[{param_name}]'.format(param_name=param_name)
        utt = utt.replace(param_mark, param, replace_num)
        return utt

    def generate_json(self):
        """
        解析原Json文件，替换第三层的句子，并构建新的Json文件
        :return:
        """
        result_json = []
        with open(self.json_path, 'r') as jsf:
            data = json.load(jsf)
        # 第一层
        for goal in data:
            goal_dict = dict()
            goal_dict["playByCategory"] = goal["playByCategory"]
            maincase = []
            # Json第二层
            for utt_group in goal["mainCase"]:
                utt_dict = dict()
                utt_dict["name"] = utt_group["name"]
                utt_dict["variation"] = []
                # Json第三层
                param_list = self.get_param_name(utt_dict["name"])
                for param_name in param_list:
                    param_dict = self.get_param_dict(param_name)
                    for utt in utt_group["varation"]:
                        utt_dict["variation"].append(self.replace_param(utt, param_name, param_dict))
                maincase.append(utt_dict)
            if __name__ == '__main__':
                goal_dict["mainCase"] = maincase
            result_json.append(goal_dict)

        with open('../out/model_output_{type_name}.json'.format(type_name=self.type_name), 'w') as a:
            json.dump(result_json, a, ensure_ascii=False)


def the_greatest_method_ever(type_name, json_path):
    utterance_handler = UtteranceHandler(type_name, json_path)
    utterance_handler.generate_json()


the_greatest_method_ever('music', 'a')
