import os, configparser

current_path = os.getcwd()
root_path = os.path.abspath(os.path.join(current_path, '../'))
gram_path = root_path + '/gram'
tmp_path = root_path + '/tmp_files'

config = configparser.ConfigParser()
config_path_name = root_path + '/config_test.ini'
config.read(config_path_name, encoding='utf8')


def _into_config():
    jenkins_text = r'' + tmp_path + '/parameter.txt'
    #jenkins_text = r'' + tmp_path + '/zch.txt'
    with open(jenkins_text, 'r', encoding='utf8') as fr:
        result = fr.readlines()
        config['Page_Selected_Info'] = {
            'page1_selected': result[0].strip(),
            'page2_selected': result[1].strip()
        }

    with open(config_path_name, 'w', encoding='utf-8') as config_file:
        config.write(config_file)


if __name__ == '__main__':
    _into_config()