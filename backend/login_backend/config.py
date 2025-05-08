import yaml
with open('login_backend/config.yaml','r') as file:
    config = yaml.safe_load(file)

class Config:
    USER_DATABASE_URL = f"mysql+pymysql://{config['mysql_db']['MYSQL_USER']}:{config['mysql_db']['MYSQL_PASSWORD']}@{config['mysql_db']['HOST']}:{config['mysql_db']['DATABASE_PORT']}/{config['mysql_db']['USER_DB']}"
    JWT_SECRET_KEY = config['JWT']['SECRET_KEY']
    JWT_ALGORITHM = config['JWT']['ALGORITHM']
    JWT_EXPIRE_MINUTES = config['JWT']['ACCESS_TOKEN_EXPIRE_MINUTES']