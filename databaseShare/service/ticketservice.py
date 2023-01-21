
from typing import List
from peewee import IntegrityError

from datas.structs import *
from datas.models import db

from repositories.ticketrepository  import TicketRepository
from repositories.articleRepository import ArticleRepository
from repositories.itemArticleRepository import ItemArticleRepository
from repositories.enumsRepository import EnumsRepository

from service.dateService import DateService

class TicketService():
    
    @staticmethod
    def list(limit: int = 0) -> List[str]:
        db.connect()
        tdcArray : List[str] = TicketRepository().list()
        db.close()
        return tdcArray if len(tdcArray) <= limit else tdcArray[-limit:]
    
    @staticmethod
    def get(tdcId : str) -> TicketDeCaisseStruct:
        db.connect()
        tdc = TicketRepository.get(tdcId=tdcId)
    
        if tdc:
            articles = ArticleRepository.get_article_by_id(tdcId=tdc.article.id)
            category = EnumsRepository.get_ticketdecaisse_category(category_id=tdc.category)
            
            if articles and category:
                tdc = TicketDeCaisseStruct(
                    id=tdc.id,
                    shop=tdc.shop,
                    localisation=tdc.localisation,
                    date=tdc.date,
                    category=category.name,
                    articles=[
                        ArticleStruct(
                            remise=a.remise, quantity=a.quantity, item=ItemArticleStruct(
                                id=a.id, ident=a.ident, prix=a.prix, name=a.name, category=a.category, group=a.group
                            )
                        ) for a in articles
                    ]
                )
                db.close()
                return tdc
        
        db.close()
        return None
    
    @staticmethod
    def post(tdc : TicketDeCaisseStruct) -> TicketDeCaisseStruct:
        db.connect()
        
        tdcArticlesId  = tdc.getTicketId()
        tdcCategory    = EnumsRepository.get_ticketdecaisse_category_by_name(tdc.category)
        
        if tdcArticlesId and tdcCategory:
            for article in tdc.articles:
                itemArticle = EnumsRepository.get_itemarticle_category_by_name(article.item.category)
                if itemArticle:
                    itemArticleId = ItemArticleRepository.get_or_create(article.item)
                    ArticleRepository.create(tdcArticlesId, itemArticleId, article)
                else:
                    db.close()
                    raise ValueError(f"ItemArticleCategorieEnum doesnt not contains name={itemArticle.category}")
                
            newTdc = TicketRepository.create(tdcArticlesId, tdcCategory, tdc)
            db.close()
            return TicketService.get(newTdc)
        else:
            db.close()
            raise ValueError(f"TickerDeCaisseTypeEnum doesnt not contains name={ticket.category}")
        
        db.close()
        return None
    
    @staticmethod
    def put(tdc : TicketDeCaisseStruct, tdcArticlesId : str) -> TicketDeCaisseStruct:
        
        db.connect()
        tdcCategory = EnumsRepository.get_ticketdecaisse_category_by_name(tdc.category)
        
        if tdcArticlesId and tdcCategory:
            TicketRepository.update(tdcArticlesId, tdcCategory, tdc)
        else:
            db.close()
            raise ValueError(f"TickerDeCaisseTypeEnum doesnt not contains name={ticket.category}")
        
        db.close()
        return TicketService.get(tdcArticlesId)
    
    @staticmethod
    def delete(tdcId : str) -> str:
        return TicketRepository.delete_sql(tdcId)