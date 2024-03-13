'''Archivo de configuración para test de servicio
de transacciones'''

import os
import unittest
from api import app


class BaseTestClass(unittest.TestCase):
    '''
    Parent class: configure test environment 
    '''
    def setUp(self):
        '''Load flask app'''
        self.app = app
        self.client = self.app.test_client()
