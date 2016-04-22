# import json
# import unittest
# import os
# from Gnip_Client.GNIPDataTrimmer import DataTrimmer
#
#
# class TestDataTrimmer(unittest.TestCase):
#     def setUp(self):
#         path = os.getcwd() + '/Gnip_Client/Gnip_Searches/Gnip_Search_0.json'
#         fo = open(path, 'w+')
#         fo.write('{"results": [{"body": "test body tweet"}]}')
#         fo.close()
#         # register remove function
#         self.addCleanup(os.remove, path)
#
#     def test___init__(self):
#         assert True
#
#     def test_get_file_location(self):
#         data_trimmer = DataTrimmer()
#         expected = os.getcwd() + '/Gnip_Client/Gnip_Searches/Gnip_Search_0.json'
#         self.assertEqual(expected, data_trimmer.get_file_location(0))
#
#     def test_get_tweets(self):
#         data_trimmer = DataTrimmer()
#         expected_set = set([])
#         expected_set.add("test body tweet")
#         self.assertEqual(expected_set, data_trimmer.get_tweets(0, 1))
#
#     def test_load_json_blob(self):
#         data_trimmer = DataTrimmer()
#         expected = json.loads('{"results": [{"body": "test body tweet"}]}')
#         self.assertEqual(expected, data_trimmer.load_json_blob(0))
#
# if __name__ == '__main__':  # pragma: no cover
#     unittest.main()
