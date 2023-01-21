
import os
import json

from typing import Any
from typing import List
from typing import Dict

from datas.models import *

from datas.structs import EnumStruct
from datas.structs import EnumWithRequireFieldStruct

class EnumsRepository:
    
    @staticmethod
    def list_ticketdecaisse_category() -> List[EnumWithRequireFieldStruct]:
        return [ EnumWithRequireFieldStruct(name=row.name, required=row.required) for row in TicketDeCaisseTypeEnum.select() ]
        
    @staticmethod
    def list_itemarticle_category() -> List[EnumWithRequireFieldStruct]:
        return [ EnumWithRequireFieldStruct(name=row.name, required=row.required) for row in ItemArticleCategoryEnum.select() ]
        
    @staticmethod
    def list_itemarticle_group() -> List[EnumWithRequireFieldStruct]:
        return [ EnumStruct(name=row.group) for row in ItemArticleGroupEnum.select() ]
        
    @staticmethod
    def get_ticketdecaisse_category(category_id : str):
        return TicketDeCaisseTypeEnum.get_or_none(TicketDeCaisseTypeEnum.id==category_id)
    
    @staticmethod
    def get_ticketdecaisse_category_by_name(name: str):
        return TicketDeCaisseTypeEnum.get_or_none(TicketDeCaisseTypeEnum.name==name)
    
    @staticmethod
    def get_itemarticle_category_by_name(name: str):
        return ItemArticleCategoryEnum.get_or_none(ItemArticleCategoryEnum.name==name)
    
    @staticmethod
    def get_itemarticle_category_by_group(group: str):
        return ItemArticleGroupEnum.get_or_none(ItemArticleGroupEnum.group==group)
