import json
import re


class TCOutputHandler:
    def __init__(self, json_data):
        self.json_data = json_data
        self.capsule_name, self.mapping_dict = self.handle_mapping('../user/intent.json')

    def get_param_vocab(self, file_name):
        """
        获取vocab列表
        """
        vocab_dict = dict()
        vocab_data = self.vocab_name_confirmation(file_name)

        # root = re.search('vocab\((.*?)\)', vocab_data).group(1)
        branches = re.findall('\"(.*?)\"{', vocab_data)
        contents = re.findall('\"{(.*?)\}', vocab_data, re.M | re.S)
        if not contents:
            contents = re.findall('{(.*?)\}', vocab_data, re.M | re.S)

        for vocab_count in range(len(contents)):
            branch = ''
            if len(branches) > 0:
                branch = branches[vocab_count]
            content = contents[vocab_count]
            content = content.replace(' ', '').replace('\"', '').split('\n')
            for vocab_word in content:
                if '//' not in vocab_word and vocab_word:
                    if branch:
                        vocab_dict[vocab_word] = branch
                    else:
                        vocab_dict[vocab_word] = ''
        return vocab_dict

    @staticmethod
    def vocab_name_confirmation(name):
        """
        检验是否存在对应的vocab
        """
        # if not name[0].isupper():
        #     first = name[0].upper()
        #     rest = name[1:]
        #     name = first + rest
        suffixes = ['6t', 'bxb']
        for suffix in suffixes:
            try:
                with open('../user/{name}.vocab.{suffix}'.format(name=name, suffix=suffix), 'r', encoding='utf-8') as a:
                    return a.read()
            except FileNotFoundError:
                pass
        # raise FileNotFoundError('File name incorrect, please check it. The param name is {name}.'.format(name=name))
        print('Warning: File name incorrect, please check it. The param name is {name}.'.format(name=name))
        return ''

    @staticmethod
    def handle_mapping(file_path):
        """
        将用户传入的表单处理为映射表
        """
        mapping_dict = {'goal': {}, 'param': {}}

        with open(file_path, 'r', encoding='utf-8') as mapping:
            mapping_data = json.load(mapping)

        capsule_name = mapping_data[0]["capsule"]

        for item in mapping_data:
            for key, value in item['goal'].items():
                mapping_dict['goal'][key] = value
            for key, value in item['param'].items():
                mapping_dict['param'][key] = value

        return capsule_name, mapping_dict

    def generate_goal(self, goal_name):
        """
                负责生成intent的goal值
        """
        return 'goal{' + '{capsule_name}.{goal_name}@context(Outer)'.format(capsule_name=self.capsule_name,
                                                                            goal_name=goal_name) + '}'

    def generate_value(self, param_name, param_word, is_open, param_dict):
        """
        负责生成intent的value值
        """
        if is_open == 'false':
            branch_name = '({param_word})'.format(param_word=param_word)
        else:
            branch = param_dict.get(param_word)
            if branch:
                if branch == '':
                    branch_name = ''
                else:
                    branch_name = '({branch})'.format(branch=branch)
            else:
                branch_name = '({param_word})'.format(param_word=param_word)

        return 'value{' + '{capsule_name}.{param_name}{branch_name}'.format(capsule_name=self.capsule_name,
                                                                            param_name=param_name,
                                                                            branch_name=branch_name) + '}'

    def start_transfer(self):
        """
        将B.py输出的结果转为intent（不支持subplan）
        """
        result = []
        # json第一层
        for item in self.json_data:
            goal = self.mapping_dict['goal'].get(item['GoalID'])
            # json第二层
            for case in item['mainCase']:
                example = case['name']
                params = re.findall('\[(.*?)\]', example)
                # 判断无参数情况
                if len(params) == 0:
                    goal_intent = self.generate_goal(goal)
                    intent = 'intent{' + goal_intent + '}'
                    for utt in case['variation']:
                        utt_out = re.sub('(\[.*?\])', '', utt.replace('(', '').replace(')', ''))
                        result.append(self.construct_item(utt_out, intent, goal))
                else:
                    all_param_dict = {}
                    for param in params:
                        param_name_user = self.mapping_dict['param'][param]["parameterId"]
                        all_param_dict[param_name_user] = self.get_param_vocab(param_name_user)
                    # json第三层
                    for utt in case['variation']:
                        goal_intent = self.generate_goal(goal)
                        value_intent = ''
                        value_dict = {}
                        param_pairs = re.findall('(\(.*?\])', utt)

                        for param_pair in param_pairs:
                            param_name = re.search('\[(.*?)\]', param_pair).group(1)
                            param_word = re.search('\((.*?)\)', param_pair).group(1)
                            value_dict[param_name] = param_word

                        for param_name, param_word in value_dict.items():
                            param_name_user = self.mapping_dict['param'][param_name]["parameterId"]
                            is_open = self.mapping_dict['param'][param_name]["parameter_isConvert"]
                            param_vocab = all_param_dict.get(param_name_user)
                            value_intent += self.generate_value(param_name_user, param_word, is_open, param_vocab)

                        intent = 'intent{' + goal_intent + value_intent + '}'
                        utt_out = re.sub('(\[.*?\])', '', utt.replace('(', '').replace(')', ''))
                        result.append(self.construct_item(utt_out, intent, goal))
        print('TC_output.py excution is completed!\n--------------------------------------------------')
        return result

    def construct_item(self, utt, intent, goal):
        """
        构建Excel表格所需要的列
        """
        return {"Utterance": utt,
                "Expected Capsule": self.capsule_name + '.' + goal,
                "expected Intent": intent,
                "Capsule matching Y/N": "Y",
                "Dialog matching Y/N": "Y",
                "Source": "MWUC",
                "dialog": "",
                "lastgoal": "",
                "actual Intent": "",
                "Expected ANL": ""
                }
