
from peewee import JOIN

from datas.models import Article
from datas.models import ItemArticle
from datas.structs import ArticleStruct

class ArticleRepository:

    @staticmethod
    def get_article_by_id(tdcId : str):
        return Article.select(Article, ItemArticle).join(ItemArticle, JOIN.LEFT_OUTER).where(Article.id==tdcId).objects()
    
    @staticmethod
    def create(articleId : str, itemArticleId : str, article : ArticleStruct):
        a = Article(id=articleId, item=itemArticleId, remise=article.remise, quantity=article.quantity)
        a.save(force_insert=True)
        return a