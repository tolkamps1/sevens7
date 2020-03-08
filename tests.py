from __future__ import print_function

import os 
import unittest
from datetime import datetime

import db
import db_init
import app 


class APIIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.db_name = 'test_seng275_tetris_dev.sl3' 
        # db_init.init(self.db_name)
        os.environ["TETRIS_DB_NAME"] = self.db_name
        db.test_db_conn()
        app.app.testing = True 
        self.app = app.app.test_client()
        self.headers = {'X-SENG275-Authentication': '123'} 
        app.authorized_tokens['123'] = True 

    def tearDown(self):
        db_init.drop_database(self.db_name)

    def _clear_db(self):
        db_init.drop_database(self.db_name) 
        db.test_db_conn() 
    
    def _create_game(self):
        """ create a new game in the db, and return it's corresponding ID """ 
        r = self.app.post('/tetris/games')
        return r.json['id'] 

    def test_sanity_check(self):
        resp_data = self.app.get('/').data 
        expected =  '<b> Hello World! </b>'
        self.assertEqual(resp_data, expected) 

    def test_nothing_really(self):
        resp = self.app.get('/tetris/games').json  # get a python object from the JSON endpoints
        self.assertListEqual(resp, [])

if __name__ == '__main__':
    unittest.main() 