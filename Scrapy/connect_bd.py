from mongoengine import connect
import configparser
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi

# client = MongoClient("mongodb+srv://nataleia_orlovska:uj%40A6wY7!4!dc4u@clusterhw7.uaenqgk.mongodb.net/?retryWrites=true&w=majority")
# db = client.Home_Work_7


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASS')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')


connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)