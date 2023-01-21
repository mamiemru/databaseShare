
from service.dateService import DateService
from legacy.sqlites import SqliteInterface
from datas.models import *

sqliteInterface = SqliteInterface()
legacyCon = sqliteInterface.connect()
db.connect()

TickerDeCaisseTypeEnumQuery = "SELECT * FROM TickerDeCaisseTypeEnum;"
ItemArticleCategorieEnumQuery = "SELECT * FROM ItemArticleCategorieEnum;"
ItemArticleGroupeEnumQuery = "SELECT * FROM ItemArticleGroupeEnum;"
ItemArticleQuery = "SELECT * FROM ItemArticle;"
ArticleQuery = "SELECT * FROM Article;"
TicketDeCaisseQuery = "SELECT * FROM TicketDeCaisse;"
DatabaseRowQuery = "SELECT * FROM DatabaseRow;"
FeuilleQuery = "SELECT * FROM Feuille;"

cur = legacyCon.cursor()

TicketDeCaisseTypeEnum.delete().execute()
for row in cur.execute(TickerDeCaisseTypeEnumQuery).fetchall():
    TicketDeCaisseTypeEnum(name=row[0], required=row[1] == 1).save()
    
ItemArticleCategoryEnum.delete().execute()
for row in cur.execute(ItemArticleCategorieEnumQuery).fetchall():
    ItemArticleCategoryEnum(name=row[0], required=row[1] == 1).save()
    
ItemArticleGroupEnum.delete().execute()
for row in cur.execute(ItemArticleGroupeEnumQuery).fetchall():
    ItemArticleGroupEnum(group=row[0]).save()

ItemArticle.delete().execute()
ItemArticle._meta.auto_increment = False
for row in cur.execute(ItemArticleQuery).fetchall():
    category = ItemArticleCategoryEnum.get(ItemArticleCategoryEnum.name==row[4])
    group    = ItemArticleGroupEnum.get_or_none(ItemArticleGroupEnum.group==row[5])
    ItemArticle(id=row[0], ident=row[1].upper(), prix=row[2], name=row[3], category=category, group=group).save(force_insert=True)
ItemArticle._meta.auto_increment = True
    
Article.delete().execute()
Article._meta.auto_increment = False
for row in cur.execute(ArticleQuery).fetchall():
    item = ItemArticle.get(ItemArticle.id==row[1])
    Article(id=row[0], item=item, remise=row[2], quantity=row[3]).save(force_insert=True)
Article._meta.auto_increment = True
    
TicketDeCaisse.delete().execute()
TicketDeCaisse._meta.auto_increment = False
for row in cur.execute(TicketDeCaisseQuery).fetchall():
    article = Article.get(Article.id==row[4])
    category = TicketDeCaisseTypeEnum.get(TicketDeCaisseTypeEnum.name==row[5])
    date = DateService.dateStrToDateIso8601(row[3])
    TicketDeCaisse(id=row[0], shop=row[1], localisation=row[2], date=date, article=article, category=category).save(force_insert=True)
TicketDeCaisse._meta.auto_increment = True

## DatabaseRow is deprecated???
    
Feuille.delete().execute()
Feuille._meta.auto_increment = False
for row in cur.execute(FeuilleQuery).fetchall():
    Feuille(date=row[0], factures=row[1]).save(force_insert=True)
Feuille._meta.auto_increment = True

cur.close()
sqliteInterface.disconnect()
db.close()