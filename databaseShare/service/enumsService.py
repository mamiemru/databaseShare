
from typing import List

from datas.structs import EnumStruct
from datas.structs import EnumWithRequireFieldStruct

from repositories.enumsRepository import EnumsRepository

class EnumsService():

    @staticmethod
    def list_ticketdecaisse_category() -> List[EnumWithRequireFieldStruct]:
        return EnumsRepository.list_ticketdecaisse_category()
    
    @staticmethod
    def get_ticketdecaisse_category(category : str):
        return EnumsRepository.get_ticketdecaisse_category_by_name(category)
    
    @staticmethod
    def list_itemarticle_category() -> List[EnumWithRequireFieldStruct]:
        return EnumsRepository.list_itemarticle_category()
    
    @staticmethod
    def get_itemarticle_category(category : str):
        return EnumsRepository.get_itemarticle_category_by_name(category)
    
    @staticmethod
    def list_itemarticle_group() -> List[EnumStruct]:
        return EnumsRepository.list_itemarticle_group()
    
    @staticmethod
    def get_itemarticle_group(group : str):
        return EnumsRepository.get_itemarticle_category_by_group(group)

