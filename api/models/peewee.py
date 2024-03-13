"""
Peewee DB MySQL - Tables usuarios publicaciones y contenidos
Last modification: 11-02-2023 - Giovanni Junco
"""
from peewee import *
from playhouse.reflection import *
from config import config




database = MySQLDatabase(
        config['DATABASE_SQL'], 
            user= config['USER_SQL'],
            passwd= config['PWD_SQL']
        )
print('Data Base:',database)
introspector = Introspector.from_database(database)
tables = introspector.generate_models()
licenses_neo4j = tables['auditando_license']

db = SqliteDatabase('queue.db')

class TransactionQueueChat(Model):
    ''' 
    Conexion a sqlite
    '''
    created = DateTimeField(null=True)
    modified = DateTimeField(null=True)
    queve_id = AutoField()
    user_id = BigIntegerField(null=True)
    time_limit = BigIntegerField(null=True)
    queve = BigIntegerField(null=True)
    amount_to_paid = FloatField(null=True)
    user_to = BigIntegerField(null=True)
    chat_id  = CharField(null=True)
    msg_id  = CharField(null=True)

    class Meta:
        ''' DOC '''
        database = db

db.connect()
