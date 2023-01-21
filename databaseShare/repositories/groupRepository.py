
from peewee import JOIN

from datas.models import ItemArticleGroupEnum
from datas.structs import EnumStruct

class GroupRepository:

    @staticmethod
    def get_by_name(name : str):
        return ItemArticleGroupEnum.get_or_none(ItemArticleGroupEnum.group==name)
    