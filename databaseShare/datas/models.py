
from peewee import Model
from peewee import AutoField
from peewee import CharField
from peewee import FloatField
from peewee import IntegerField
from peewee import BooleanField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import CompositeKey
from peewee import SqliteDatabase

db = SqliteDatabase('database.sqlite')

class TicketDeCaisseTypeEnum(Model):
    id = AutoField()
    name = CharField(null=False)
    required = BooleanField(null=False, default=False)
    
    class Meta:
        database = db
        
class ItemArticleCategoryEnum(Model):
    id = AutoField()
    name = CharField(null=False)
    required = BooleanField(null=False, default=False)
    
    class Meta:
        database = db

class ItemArticleGroupEnum(Model):
    id = AutoField()
    group = CharField(null=False)
    
    class Meta:
        database = db
    
class ItemArticle(Model):
    id = AutoField()
    ident = CharField(null=False)
    prix = CharField(null=False)
    name = CharField(null=False)
    category = ForeignKeyField(ItemArticleCategoryEnum, field='name')
    group = ForeignKeyField(ItemArticleGroupEnum, field='group', null=True, default=None)
    
    class Meta:
        database = db
    
class Article(Model):
    id = IntegerField()
    item = ForeignKeyField(ItemArticle, field='id')
    remise = FloatField(null=False, default=0.0)
    quantity = IntegerField(null=False, default=1)
    
    class Meta:
        database = db
        primary_key = CompositeKey('id', 'item', 'remise', 'quantity')
    
class TicketDeCaisse(Model):
    id = AutoField()
    shop = CharField(null=False)
    localisation = CharField(null=False)
    date = DateTimeField(null=False)
    article = ForeignKeyField(Article, field='id')
    category = ForeignKeyField(TicketDeCaisseTypeEnum, field='id')
    
    class Meta:
        database = db
    
## DatabaseRowStruct is deprecated???
class DatabaseRowModel(Model):
    id = AutoField()
    shop = CharField(null=False)
    localisation = CharField(null=False)
    category = CharField(null=False)
    itemArticleCategorie = CharField(null=False)
    itemArticle = CharField(null=False)
    itemNomArticle = CharField(null=False)
    prix = FloatField(default=0.0)
    
    class Meta:
        database = db
    
class Feuille(Model):
    date = IntegerField(primary_key=True, null=False)
    factures = CharField(null=False, default="{}")
    
    class Meta:
        database = db
