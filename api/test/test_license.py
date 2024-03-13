'''
    @author: Giovanni Junco
    @since: 17-01-2024
    @summary: Testing para ontener licensias
'''

import json
from . import BaseTestClass

PART1 = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
PART2 = ".eyJleHAiOjE2OTA1MjA1ODQsInN1YiI6MTgxfQ"
PART3 = ".FAO3xvRwub2pT0tUuOt06ewQx2THkZdgyWNs44Z0KrQ"
PART2_5 = ".eyJleHAiOjE2OTA1MjA1ODQsInN1YiI6MTgxfQq"
TOKEN = "".join([PART1, PART2, PART3])
BAD_TOKEN = "".join([PART1, PART2_5, PART3])

class GeneralAuthTestCase(BaseTestClass):
    ''' Unit tests of the token authentication system. executed on all microservices tests
        Required.
            ENDPOINT (str): Endpoint's url
            METHOD (str): GET, POST, PUT, DELETE
            QUERY (dict): complete structure requested by frontend
            QUERY_NAME (str): Name of mutation or query
            NEED_TOKEN (boolean): Determines whether to run the token test or not
    '''
    ENDPOINT = None
    METHOD = None
    QUERY= None
    QUERY_NAME= None
    NEED_TOKEN= None
    def test_auth_with_token(self):
        ''' Returns OK if test status is 200, token ok'''
        if self.METHOD == 'POST' and self.NEED_TOKEN:
            #send resquest post to test
            res = self.client.post(self.ENDPOINT,
                                data=json.dumps(self.QUERY), 
                                content_type='application/json' ,
                                headers={"Authorization": TOKEN})
            #request response to dict
            data = json.loads(res.data)
            #get request status number
            validate=data['data'][self.QUERY_NAME]['status']
            #validate status 200
            self.assertEqual(200, validate)

#Query mongo
class GetLicenseTestCase(GeneralAuthTestCase):
    '''
    @author: Giovanni Junco
    @since: 17-01-2024
    @summary: Testing para ontener licensias
    '''
    ENDPOINT = '/license/'
    METHOD = 'GET'
    QUERY=  {
        "license_id": -2,
        "user_owner": 1
    }
    def test_post_transaction_complete(self):
        '''        Returns OK if test status is 200, token ok        '''
        res = self.client.get(self.ENDPOINT,
                            data=json.dumps(self.QUERY),
                            content_type='application/json')
        self.assertEqual(200, res.status_code)
