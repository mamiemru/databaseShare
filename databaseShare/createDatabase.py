from datas.models import *
db.connect()
db.create_tables([TicketDeCaisseTypeEnum, ItemArticleCategoryEnum, ItemArticleGroupEnum, ItemArticleStruct, ArticleStruct, TicketDeCaisseStruct, DatabaseRowStruct, FeuilleStruct]) 