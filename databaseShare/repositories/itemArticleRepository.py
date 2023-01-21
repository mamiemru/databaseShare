
from peewee import JOIN

from datas.models import ItemArticle
from datas.structs import ItemArticleStruct

from repositories.groupRepository import GroupRepository

class ItemArticleRepository:
    
    def get_or_create(itemArticle : ItemArticleStruct):
        oldItemArticle = ItemArticle.get_or_none(ItemArticle.ident==itemArticle.ident, ItemArticle.prix==itemArticle.prix)
        if oldItemArticle:
            return oldItemArticle.id
        group = GroupRepository.get_by_name(itemArticle.group)
        newItemArticle = ItemArticle(ident=itemArticle.ident, prix=itemArticle.prix, name=itemArticle.name,category=itemArticle.category, group=group.id if group else None)
        newItemArticle.save()
        return newItemArticle.id

    @staticmethod
    def get_article_by_id(tdcId : str):
        return Article.select(Article, ItemArticle).join(ItemArticle, JOIN.LEFT_OUTER).where(Article.id==tdcId).objects()