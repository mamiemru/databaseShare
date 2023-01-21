
from typing import List

from peewee import JOIN
from datas.models import *

from datas.structs import DatabaseStruct
from datas.structs import DatabaseRowStruct

## refacto à faire
class DatabaseRepository:
    
    @staticmethod
    def getFullInformationsFromArticleIdent(ident : str) -> DatabaseStruct:
        db.connect()
        query = TicketDeCaisse.select(
            Article.item, TicketDeCaisse.shop, TicketDeCaisse.localisation, TicketDeCaisse.category, ItemArticle.category.alias('itemArticleCategory'),
            ItemArticle.ident, ItemArticle.name, ItemArticle.prix, TickerDeCaisse.date, ItemArticle.group
        ).join(ArticleModel, JOIN.LEFT).join(ItemArticleModel, JOIN.LEFT).where(ItemArticle.ident==ident)
        datas = DatabaseStruct(rows=[
            DatabaseRowStruct(
                id=row.item, shop=row.shop, localisation=row.localisation, category=row.category, itemArticleCategorie=row.itemArticleCategory, 
                itemArticle=row.ident, itemNomArticle=row.name, prix=row.prix, dateAchatStr=row.date, group=row.group
            ) for row in query.objects()
        ])
        db.close()
        return datas

    @staticmethod
    def getFullInformationsFromShopName(shop : str) -> DatabaseStruct:
        db.connect()
        query = TicketDeCaisse.select(
            Article.item, TicketDeCaisse.shop, TicketDeCaisse.localisation, TicketDeCaisse.category, ItemArticle.category.alias('itemArticleCategory'),
            ItemArticle.ident, ItemArticle.name, ItemArticle.prix, TickerDeCaisse.date, ItemArticle.group
        ).join(ArticleModel, JOIN.LEFT).join(ItemArticleModel, JOIN.LEFT).where(TicketDeCaisse.shop==shop)
        datas = DatabaseStruct(rows=[
            DatabaseRowStruct(
                id=row.item, shop=row.shop, localisation=row.localisation, category=row.category, itemArticleCategorie=row.itemArticleCategory, 
                itemArticle=row.ident, itemNomArticle=row.name, prix=row.prix, dateAchatStr=row.date, group=row.group
            ) for row in query.objects()
        ])
        db.close()

    @staticmethod
    def getFullInformationsFromGroupe(group : str) -> DatabaseStruct:
        db.connect()
        query = TicketDeCaisse.select(
            Article.item, TicketDeCaisse.shop, TicketDeCaisse.localisation, TicketDeCaisse.category, ItemArticle.category.alias('itemArticleCategory'),
            ItemArticle.ident, ItemArticle.name, ItemArticle.prix, TickerDeCaisse.date, ItemArticle.group
        ).join(ArticleModel, JOIN.LEFT).join(ItemArticleModel, JOIN.LEFT).where(ItemArticle.group==group)
        datas = DatabaseStruct(rows=[
            DatabaseRowStruct(
                id=row.item, shop=row.shop, localisation=row.localisation, category=row.category, itemArticleCategorie=row.itemArticleCategory, 
                itemArticle=row.ident, itemNomArticle=row.name, prix=row.prix, dateAchatStr=row.date, group=row.group
            ) for row in query.objects()
        ])
        db.close()

    @staticmethod
    def getFullInformationsFromCategory(itemArticleCategory : str) -> DatabaseStruct:
        db.connect()
        query = TicketDeCaisse.select(
            Article.item, TicketDeCaisse.shop, TicketDeCaisse.localisation, TicketDeCaisse.category, ItemArticle.category.alias('itemArticleCategory'),
            ItemArticle.ident, ItemArticle.name, ItemArticle.prix, TickerDeCaisse.date, ItemArticle.group
        ).join(ArticleModel, JOIN.LEFT).join(ItemArticleModel, JOIN.LEFT).where(ItemArticle.gcategory==itemArticleCategory)
        datas = DatabaseStruct(rows=[
            DatabaseRowStruct(
                id=row.item, shop=row.shop, localisation=row.localisation, category=row.category, itemArticleCategorie=row.itemArticleCategory, 
                itemArticle=row.ident, itemNomArticle=row.name, prix=row.prix, dateAchatStr=row.date, group=row.group
            ) for row in query.objects()
        ])
        db.close()

    @staticmethod
    def retrieve_all_item_articles_idents(cur=None) -> List[str]:
        db.connect()
        datas = [data.ident for data in ItemArticle.select(ItemArticle.ident)]
        db.close()
        return datas

    @staticmethod
    def read_sql(cur=None) -> DatabaseStruct:
        db.connect()
        query = TicketDeCaisse.select(
            Article.item, TicketDeCaisse.shop, TicketDeCaisse.localisation, TicketDeCaisse.category, ItemArticle.category.alias('itemArticleCategory'),
            ItemArticle.ident, ItemArticle.name, ItemArticle.prix, TickerDeCaisse.date, ItemArticle.group
        ).join(ArticleModel, JOIN.LEFT).join(ItemArticleModel, JOIN.LEFT)
        datas = DatabaseStruct(rows=[
            DatabaseRowStruct(
                id=row.item, shop=row.shop, localisation=row.localisation, category=row.category, itemArticleCategorie=row.itemArticleCategory, 
                itemArticle=row.ident, itemNomArticle=row.name, prix=row.prix, dateAchatStr=row.date, group=row.group
            ) for row in query.objects()
        ])
        db.close()
        return datas
        
    @staticmethod
    def write_sql(db : DatabaseStruct, cur=None):
        pass
    
    @staticmethod
    def editSql(dbrow : DatabaseRowStruct, cur=None):
        pass
