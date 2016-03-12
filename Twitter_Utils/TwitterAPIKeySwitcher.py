import json
import os
from Eternal_Utils.CommonUtils import CommonUtils
import logging

class TwitterAPIKeyHandler:
    def __init__(self):
        self.api_key_array = []
        self.number_of_keys = int(CommonUtils.get_environ_variable('NUMBER_OF_TWITTER_KEYS_AVAILABLE'))
        wd = os.getcwd()
        pos = wd.find("BigDataMonsters")
        if pos > 0:  # pragma: no cover
            path = wd[0:pos+15]
        else:
            path = wd
        self.key_check_write_path = path + '/Twitter_Utils/data/Active_API_Log.json'
        self.logger = logging.getLogger(__name__)

    def get_api_keys_from_environment(self):
        """
        Gets all API keys we have saved to our environment.
        :return: returns an array of individual dictionary entries with key info.
        """
        for key in range(0, self.number_of_keys):
            app_key = 'TWITTER_APP_KEY_' + str(key)
            app_secret = 'TWITTER_APP_SECRET_' + str(key)
            oauth_token = 'TWITTER_OAUTH_TOKEN_' + str(key)
            oauth_token_secret = 'TWITTER_OAUTH_TOKEN_SECRET_' + str(key)

            app_key = os.environ[app_key]
            app_secret = os.environ[app_secret]
            oauth_token = os.environ[oauth_token]
            oauth_token_secret = os.environ[oauth_token_secret]

            individual_key = dict(app_key=app_key,
                                  app_secret=app_secret,
                                  oauth_token=oauth_token,
                                  oauth_token_secret=oauth_token_secret)
            self.api_key_array.append(individual_key)

        return self.api_key_array

    def check_which_key_to_use(self):
        """
        Iterates through keys on disk to see which key is available for use.
        """
        try:
            with open(self.key_check_write_path) as f:
                data = json.load(f)
                for idx, entry in enumerate(data):
                    if not entry['in_use']:
                        print entry
                        self.update_json_file(data, idx)
                        return idx
            # TODO - What do we do if none is found?
        except IOError:
            print 'File not found while checking which key to use in TwitterAPIKeys'
            return self.write_initial_keys_state_to_disk()

    def clear_api_key_at_index_for_use(self, index):
        """
        Changes in_use for key at index to False
        :param index: index where key is located in our array of API keys
        """
        try:
            with open(self.key_check_write_path) as f:
                data = json.load(f)
                if data[index]['in_use']:
                    self.update_json_file(data, index)
                    return True
        except IOError:
            print 'File not found while clearing key for use in TwitterAPIKeys'
            raise IOError

    def update_json_file(self, json_file, index):
        """
        Update key entry to opposite of it's entry.
        :param json_file: json_file of keys, format array[dict{}]
        :param index: index within array of json_file
        """
        try:
            data = json_file
            if data[index]['in_use']:
                data[index]['in_use'] = False
            else:
                data[index]['in_use'] = True

            json_file = open(self.key_check_write_path, 'w+')
            json_file.write(json.dumps(data))
            print json_file
            json_file.close()
            return True

        except IOError:
            self.logger.exception(IOError)
            self.logger.error('File not found while updating JSON file in TwitterAPIKeys at ' + self.key_check_write_path)
            raise IOError

    # TODO - Create a makefile for clearing the keys API file for fresh installs in the future.
    def write_initial_keys_state_to_disk(self):
        """
        When no keys are found in disk we write the number of keys
        """
        key_array = []
        for key in range(0, self.number_of_keys):
            key_name = 'Key_' + str(key)
            if key != 0:
                key_entry = {'key_name': key_name, 'in_use': False}
            else:
                key_entry = {'key_name': key_name, 'in_use': True}
            key_array.append(key_entry)

        content = json.dumps(key_array)
        try:
            with open(self.key_check_write_path, 'w+') as f:
                f.write(content)
            f.close()
            print 'Key file written'
            return 0
        except IOError:
            self.logger.exception(IOError)
            self.logger.error('IOError while writing initial key state to disk in TwitterAPIKeys at ' + self.key_check_write_path)
            return None
