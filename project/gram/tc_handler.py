import json


class TCHandler:
    def __init__(self, json_data, type_name):
        self.type_name = type_name
        self.json_data = json_data
        self.mapping_dict = self.handle_mapping('../user/intent.json')

    @staticmethod
    def handle_mapping(file_path):
        """
        将用户传入的表单处理为映射表
        """
        mapping_dict = {"capsule": {}, "goal": {}}

        with open(file_path, 'r', encoding='utf-8') as mapping:
            mapping_data = json.load(mapping)

        for item in mapping_data:
            for key, value in item['capsule'].items():
                mapping_dict["capsule"][key] = value

        for item in mapping_data:
            for key, value in item['goal'].items():
                mapping_dict["goal"][key] = value
        # print(mapping_dict)
        return mapping_dict

    @staticmethod
    def construct_item(utt, intent, goal, capsule):
        """
        构建Excel表格所需要的列
        """
        return {"Utterance": utt,
                "Expected Capsule": capsule + '.' + goal,
                "expected Intent": intent,
                "Capsule matching Y/N": "Y",
                "Dialog matching Y/N": "Y",
                "Source": "MWUC",
                "dialog": "",
                "lastgoal": "",
                "actual Intent": "",
                "Expected ANL": ""
                }

    def start_transfer(self):
        """
        将结果转为可用excel类型
        """
        result = []
        for goal_layer in self.json_data:
            capsule_name = self.mapping_dict["capsule"].get(self.type_name)
            if not capsule_name:
                capsule_name = 'viv' + self.type_name
            # print(capsule_name)
            goal = self.mapping_dict["goal"].get(goal_layer['GoalID'])
            if not goal:
                goal = goal_layer['GoalID']
            for utt_layer in goal_layer["mainCase"]:
                for utt in utt_layer["variation"]:
                    item = self.construct_item(utt, '', goal, capsule_name)
                    result.append(item)

        return result


def tc_handler(json_data, type_name):
    tc = TCHandler(json_data, type_name)
    result = tc.start_transfer()
    print("TC.py execution is completed!\n--------------------------------------------------")
    return result
