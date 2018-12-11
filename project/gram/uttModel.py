import prefix
import param_replacement
import TC_output
import configparser
import json


class UttModel:
    def __init__(self):
        self.page1_param = self.get_page1_param()
        self.tc_param = self.get_tc_param()

    @staticmethod
    def get_page1_param():
        config = configparser.ConfigParser()
        config.read('../config_test.ini')
        page1_selected = eval(config.get('Page_Selected_Info', 'page1_selected'))[0]
        return page1_selected

    @staticmethod
    def get_tc_param():
        config = configparser.ConfigParser()
        config.read('../config_test.ini')
        tc_param = eval(config.get('Page_Selected_Info', 'generate_tc_file'))
        return tc_param

    @staticmethod
    def start_method_1():
        prefix.Interface_file()

    def start_method_2(self):
        json_data = param_replacement.utterance_output(self.page1_param, '../tmp_files/prefixOutput.json',
                                                       utterance_mode=True)

        with open('../out/variation_{type_name}.json'.format(type_name=self.page1_param), 'w',
                  encoding='utf-8') as output:
            json.dump(json_data, output, ensure_ascii=False)

    def start_method_3(self):
        json_data = param_replacement.utterance_output(self.page1_param, '../tmp_files/prefixOutput.json',
                                                       utterance_mode=False)
        tc = TC_output.TCOutputHandler(json_data)
        result = tc.start_transfer()
        with open('../out/tc.json', 'w', encoding='utf-8') as output:
            json.dump(result, output, ensure_ascii=False)


u = UttModel()
u.start_method_1()
u.start_method_2()
if u.tc_param:
    u.start_method_3()
