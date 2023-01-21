
from typing import Any
from typing import Tuple
from typing import List
from typing import Dict

from datas.structs import ArticleStruct
from datas.structs import DatabaseStruct
from datas.structs import DatabaseRowStruct
from datas.structs import ItemArticleStruct
from datas.structs import TicketDeCaisseStruct

from repositories.databaseRepository import DatabaseRepository

## refacto à faire
class DatabaseService():

    SHOP = "shop"
    LOCALISATION = "localisation"
    CATEGORIE = "category"
    ITEM_ARTICLE_CATEGORIE = "itemArticleCategorie"
    ITEM_ARTICLE = "itemArticle"
    ITEM_NOM_ARTICLE = "itemNomArticle"
    PRIX = "prix"
    GROUPE = "group"

    @staticmethod
    def list() -> DatabaseStruct:
        return DatabaseRepository.read_sql()

    @staticmethod
    def get(key :str, database : DatabaseStruct = None) -> List[str]:
        db = database if database != None else DatabaseRepository.read_sql()
        for d in db.rows:
            if d.get(key, None) is None:
                exit(0)
        d = list(set([x.get(key, "") for x in db]))
        return d if d and d[0] else list()

    @staticmethod
    def getNoNone(key :str, database : DatabaseStruct = None) -> List[str]:
        db = database if database != None else DatabaseRepository.read_sql()
        d = list(filter(lambda x : x, set([x.get(key, None) for x in db])))
        return d if d and d[0] else list()

    @staticmethod
    def getOne(key :str, database : DatabaseStruct = None) -> List[str]:
        db = database if database else DatabaseRepository.read_sql()
        return [x.get(key, "") for x in db][0]

    @staticmethod
    def getLastOne(key :str, database : DatabaseStruct = None) -> List[str]:
        db = database if database else DatabaseRepository.read_sql()
        return [x.get(key, "") for x in db][-1]

    @staticmethod
    def getOneOreNone(key :str, database : DatabaseStruct = None) -> List[str]:
        db = database if database else DatabaseRepository.read_sql()
        d = [x.get(key, "") for x in db]
        return d[0] if len(d) == 1 else ''

    @staticmethod
    def filter(*keyValue : Tuple[str, str], database : DatabaseStruct = None, removeDuplicate=False) -> DatabaseStruct:
        if not database:
            database = DatabaseRepository.read_sql()
        result : List[DatabaseRowStruct] = list()

        d : Dict[str, str] = {key:value for key,value in keyValue}
        articleNames = list()

        for row in database.rows:
            row : DatabaseRowStruct = row
            itemOk = True
            for key,value in d.items():
                if value != row.get(key):
                    itemOk = False
            if itemOk and (not removeDuplicate or not row.itemArticle in articleNames):
                result.append(row)
                articleNames.append(row.itemArticle)

        return DatabaseStruct(rows=list(result))

    @staticmethod
    def filterByItemArticle(ticket : TicketDeCaisseStruct, itemArticle : ItemArticleStruct, database : DatabaseStruct = None) -> DatabaseStruct:
        return DatabaseService.filter(
            ('shop', ticket.shop), ('localisation', ticket.localisation), ('category', ticket.category),
            ('itemArticleCategorie', itemArticle.category), ('itemArticle', itemArticle.id), ('itemNomArticle', itemArticle.name),
            database=database
        )

    @staticmethod
    def getFullInformationsFromArticleIdent(ident : str) -> DatabaseStruct:
        return DatabaseRepository.getFullInformationsFromArticleIdent(ident)

    @staticmethod
    def getFullInformationsFromShopName(shop : str) -> DatabaseStruct:
        return DatabaseRepository.getFullInformationsFromShopName(shop)

    @staticmethod
    def getFullInformationsFromGroupe(group : str) -> DatabaseStruct:
        return DatabaseRepository.getFullInformationsFromGroupe(group)

    @staticmethod
    def getFullInformationsFromCategory(itemArticleCategory : str) -> DatabaseStruct:
        return DatabaseRepository.getFullInformationsFromCategory(itemArticleCategory)

    @staticmethod
    def retrieve_all_item_articles_idents() -> List[str]:
        return DatabaseRepository.retrieve_all_item_articles_idents()

    @staticmethod
    def get_article_by_item_article_ident(ident, n=0) -> ArticleStruct:
        d : DatabaseStruct = DatabaseRepository.getFullInformationsFromArticleIdent(ident)
        return d.rows[n].toArticleObject() if d and d.rows else None
