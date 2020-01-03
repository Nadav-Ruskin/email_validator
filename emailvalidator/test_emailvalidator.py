# # from .. import server
# # import unittest
# # import requests
# # from flask import Flask

# # class MyTestCase(unittest.TestCase):


# #	 @pytest.fixture
# #	 def server.app():
# #		 server.app = server.create_server.app()
# #		 return server.app

# #	 def test_home(self):
# #		 result = self.client.post('/email/validate', json='{"email":"ruskin.nadav@gmail.com"}')
# #		 print('pls print dis {}'.format(result))
# #		 print('pls....')
# #		 assert(True)
# #		 # Make your assertions

# # project/test_basic.py
 
 
# import os
# import unittest
 
# from .. import server.app
 
 
# TEST_DB = 'test.db'
 
 
# class BasicTests(unittest.TestCase):
 
# 	############################
# 	#### setup and teardown ####
# 	############################
 
# 	# executed prior to each test
# 	def setUp(self):
# 		server.app.config['TESTING'] = True
# 		server.app.config['WTF_CSRF_ENABLED'] = False
# 		server.app.config['DEBUG'] = False
# 		server.app = server.app.test_client()
 
 
# ###############
# #### tests ####
# ###############
 
# 	def test_main_page(self):
# 		response = server.app.post('/email/validate', json='{"email":"ruskin.nadav@gmail.com"}')
# 		print('pls print dis {}'.format(response))
# 		# server.assertEqual(response.status_code, 200)
 
 
# if __name__ == "__main__":
# 	unittest.main()

from server import app
import unittest

# python -m unittest test_app


class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_main(self):
        response = self.app.post('/email/validate', json={"email":"ruskin.nadav@gmail.com"})
        data = response.data.decode("utf-8")
        assert(data == '{"dns":{"valid":true},"mailbox":{"code":250,"valid":true},"regex":{"valid":true},"reputation":{"reputation":"Favorable  |  Neutral","valid":true},"schema":{"valid":true}}\n')