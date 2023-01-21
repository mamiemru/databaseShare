
from typing import Tuple
from peewee import JOIN

from datas.models import *

from repositories.enumsRepository import EnumsRepository

from datas.structs import ArticleStruct
from datas.structs import TicketDeCaisseStruct

class TicketRepository:
    
    @staticmethod
    def get_tdcs_between_date(dateInf : str, dateSup : str):
        return TicketDeCaisse.select(TicketDeCaisse.id).where(TicketDeCaisse.id.between(dateInf, dateSup))

    @staticmethod
    def list() -> Tuple[str]:
        return [d.id for d in TicketDeCaisse.select(TicketDeCaisse.id).order_by(TicketDeCaisse.id)]
    
    @staticmethod
    def get(tdcId: str):
        return TicketDeCaisse.get_or_none(TicketDeCaisse.id==tdcId)
    
    @staticmethod
    def create(articleId : str, category : str, tdc : TicketDeCaisseStruct):
        newTdc = TicketDeCaisse(shop=tdc.shop, localisation=tdc.localisation, date=tdc.date, article=articleId, category=category)
        newTdc.save()
        return newTdc
    
    @staticmethod
    def update(articleId : str, category : str, tdc : TicketDeCaisseStruct):
        res = TicketDeCaisse.update(
                {
                    TicketDeCaisse.shop: tdc.shop, TicketDeCaisse.localisation: tdc.localisation, 
                    TicketDeCaisse.date: tdc.date, TicketDeCaisse.category: category
                }
            ).where(TicketDeCaisse.id==articleId)
        res.execute()
        return res

    @staticmethod
    def delete_sql(tdcId):
        Article.delete().where(Article.id==tdcId).execute()
        TicketDeCaisse().delete().where(TicketDeCaisse.id==tdcId).execute()
        return tdcId