import sys
from time import time
import os
import uuid
from config import config
from neo4j import GraphDatabase
from logs import get_error
from logs import do_log

#establish connection
driver=GraphDatabase.driver(uri='bolt://localhost:7687',auth=('neo4j','1234abcd'))
session=driver.session()
def init_neo4j():
    try: 
        global driver, session
        print('A:',driver._closed, session._closed)
        if driver._closed:
            driver=GraphDatabase.driver(uri='bolt://localhost:7687',auth=('neo4j','1234abcd'))
        if session._closed:
            session=driver.session()
    except:
        get_error('init_neo4j, models neo4j',sys.exc_info())

class License:
    def __init__(self, license_id):
        ''' load license id and connect with Neo4j'''
        self.license_id = license_id
        init_neo4j()

    def neo4jclass_dict(self, data):
        '''** merge between dicts'''
        return {**dict(data)['n']._properties, **{'license_id':dict(data)['n'].element_id}}
    
    def find(self, user_owner=0):
        ''' Serach all nodes
            use LIMIT pagination'''
        try:
            q1=f"MATCH (n:License WHERE n.user_owner = {user_owner}) RETURN n"
            
            if self.license_id > -1:
                q1=f"MATCH (n) WHERE id(n)={self.license_id} RETURN n"
            """ open_time = time()            
            close_time = time()
            do_log(' neo4j find:',round(close_time-open_time,3),'','info') # mas de 2 segundos -> 0.004s """ 
            return [ self.neo4jclass_dict(row) for row in session.run(q1)]
        except Exception as e:
            get_error('find, models neo4j',sys.exc_info())
            return str(e)

    def register(self,license_data):
        ''' Crwate node with labels'''
        q1="""
        create (n:License
            {
                NAME:$license_name, user_owner:$user_owner, 
                orders_quantity:$orders_quantity, users_quantity:$users_quantity,
                pesos_col:$pesos_col, createdAt:$created,
                is_active:$is_active, is_banned:$is_banned, modified:$modified
            }
        )  RETURN n
        """
        try:
            return [ self.neo4jclass_dict(row) for row in session.run(q1,license_data)]      
        except Exception as e:
            get_error('POST, models neo4j',sys.exc_info())
            return str(e)
        
    
    def update(self, license_data):
        ''' Update licens'''
        try:
            update=''
            if 'license_name' in license_data:
                update='n.NAME = $license_name'
            for k in license_data.keys():
                update+=', ' if update else '' 
                update+=f'n.{k} = ${k}'            
            q1=f"""
                MATCH (n) WHERE elementid(n)=$license_id
                SET {update}
                RETURN n
            """      
            return [ self.neo4jclass_dict(row) for row in session.run(q1,license_data)]
        except Exception as e:
            get_error('PUT, models neo4j',sys.exc_info())
            return (str(e))
    
    def delete(self):
        q1=f"match (n) WHERE elementid(n)={self.license_id} detach delete (n)"
        try:
            session.run(q1)
            return 'license_deleted'
        except Exception as e:
            get_error('Delete, models neo4j',sys.exc_info())
            return (str(e))
