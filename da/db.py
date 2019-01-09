import pymongo

user="appserver"
pwd="pwdappserver"
#ip="127.0.0.1"
ip="172.31.22.208"
from pymongo import MongoClient
client = MongoClient("mongodb://%s:%s@%s/admin?replicaSet=replset" % (user, pwd, ip))

appdb = client.db
