import os


class CommonUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_environ_variable(var_name):
        try:
            return os.environ[var_name]
        except KeyError:
            wd = os.getcwd()
            pos = wd.find("BigDataMonsters")
            if pos > 0:
                path = wd[0:pos+15]
            else:
                path = wd
            env_file_path = path + '/Eternal_Utils/utils.env'
            env_file = open(env_file_path, 'r')
            for line in env_file:
                key_values = line.split('=')
                if key_values[0] == var_name:
                    return key_values[1].replace('\n', '')

        return None
