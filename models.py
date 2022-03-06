import peewee
from datetime import date

today = date.today()
today = today.strftime("%m.%d.%y")

db = peewee.SqliteDatabase('database.db', check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Users(BaseModel):
    uid = peewee.IntegerField(unique = True)
    nickname = peewee.TextField(default = '')
    username = peewee.TextField(default = '')
    statusUser = peewee.TextField(default = 'deactivate')


class scrappIngfo(BaseModel):
    scrappUrl = peewee.TextField(default = '')
    scrappName = peewee.TextField(default = '')
    scrappCash = peewee.TextField(default = '')
    scrappStatus = peewee.TextField(default = 'wait')
    scrappDate = peewee.TextField(default = today)

class telethonMessage(BaseModel):
    scrappStatus = peewee.TextField(default = 'wait')
    scrappUrl = peewee.TextField(default = '')
    historyScrapp = peewee.TextField(default = '')
    text = peewee.TextField(default = '')


class clickCount(BaseModel):
    uid = peewee.TextField(default = '')
    scrappId = peewee.IntegerField()
    clickDate = peewee.TextField(default = today)

class words(BaseModel):
    white = peewee.TextField(default = '')
    black = peewee.TextField(default = '')


db.create_tables([Users])
db.create_tables([telethonMessage])
db.create_tables([words])
db.create_tables([scrappIngfo])
db.create_tables([clickCount])
