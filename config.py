"""
Core environment variables
Last modification: 11-02-2023 - Giovanni Junco
"""
import os
from dotenv import load_dotenv

# Get path for .env file
ENV = os.path.join(os.path.dirname(__file__), '.env2')

if os.path.exists(ENV):
    # Load the data in .env
    load_dotenv(ENV)


development_config={
    'DEBUG' : True,
    'UPLOAD_FOLDER'  : os.getenv('SECRET_KEY'),
    "HOST_SQL" : os.getenv('HOST_SQL'),
    "USER_SQL" : os.getenv('USER_SQL'),
    "PWD_SQL" : os.getenv('PWD_SQL'),
    "DATABASE_SQL" : os.getenv('DATABASE_SQL'),
    "NEO4J_USERNAME" : os.getenv('NEO4J_USERNAME'),
    "NEO4J_PASSWORD" : os.getenv('NEO4J_PASSWORD'),
}
testing_config={
    'DEBUG' : True,
    ' UPLOAD_FOLDER'  : os.getenv('SECRET_KEY')
}

production_config={
    'DEBUG' : True,
    ' UPLOAD_FOLDER'  : os.getenv('SECRET_KEY')
}

config={
    'development': development_config,
    'testing': testing_config,
    'production': production_config,
    
}
config=config[os.getenv('ENVIRONMENT')]