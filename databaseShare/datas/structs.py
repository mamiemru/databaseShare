
#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import json
import math

from enum   import Enum
from typing import Tuple
from typing import List
from typing import Dict
from typing import Any

from dataclasses       import dataclass
from dataclasses       import field

from email.utils import parsedate_to_datetime

@dataclass
class EnumStruct(object):
    name: str

@dataclass
class EnumWithRequireFieldStruct(object):
    name: str
    required: bool

@dataclass
class ItemArticleStruct(object):
    id: str
    ident: str
    prix: float
    name: str
    category: str
    group: str

    def get(self, key, default=None):
        return getattr(self, key, default)
    
    def from_dict(dic : Dict):
        return ItemArticleStruct(**dic)

@dataclass
class ArticleStruct(object):
    remise: float
    item: ItemArticleStruct
    quantity : int = 1

    def get(self, key, default=None):
        return getattr(self, key, default)
    
    def from_dict(dic : Dict):
        return ArticleStruct(remise=dic.get('remise', 0.0), quantity=dic.get('quantity', 1), item=ItemArticleStruct.from_dict(dic.get('item', {})))
       
@dataclass
class TicketDeCaisseHeaderStruct(object):
    id: str
    shop: str
    localisation: str
    date: str
    category: str
    total: int = 0

    def getTicketId(self):
        if not self.date:
            return 0
        if self.date[-1] == 'Z':
            strptime = time.strptime(self.date[:-5], '%Y-%m-%dT%H:%M:%S')
        else:
            strptime = time.strptime(self.date, '%d/%m/%Y %H:%M:%S')
        return time.mktime(strptime) if self.date else 0

@dataclass
class TicketDeCaisseStruct(TicketDeCaisseHeaderStruct):
    articles: List[ArticleStruct] = field(default_factory=list)
    
    @staticmethod
    def from_dict(dic : Dict):
        return TicketDeCaisseStruct(
            id=dic.get('id', None),
            shop=dic.get('shop', None),
            localisation=dic.get('localisation', None),
            date=dic.get('date', None),
            category=dic.get('category', None),
            articles=[ArticleStruct.from_dict(article) for article in dic['articles']]
        )

    def get(self, key, default=None):
        return getattr(self, key, default)

    def sommeTotal(self) -> float:
        total = list()
        for article in self.articles:
            total.append(float(article.quantity*article.item.prix) - float(article.remise))
        return round(math.fsum(total),2)

    def resumer(self):
        return f"""{self.shop.strip().ljust(20)[:20]} {self.date.ljust(25)[:19]} {str(self.sommeTotal()).ljust(6)[:6]}€"""

    @staticmethod
    def empty():
        return TicketDeCaisseStruct(None, None, None, None, list(), None)

@dataclass
class TableFeuilleRowStruct(object):
    name : str
    date : str
    price : float
    priceOnlyRequired : float

    def __init__(self, name, price, date, required:bool=False):
        self.name  = name
        self.price = price
        self.date  = date
        self.priceOnlyRequired = price if required else 0.0

    @staticmethod
    def empty(name=None):
        return TableFeuilleRowStruct(name, 0.0, None, False)

@dataclass
class TableFeuilleBodyStruct(object):
    name: str
    header: TableFeuilleRowStruct
    rows: List[TableFeuilleRowStruct]

    def __init__(self, name):
        self.name = name
        self.header = TableFeuilleRowStruct.empty(name=None)
        self.header.name = name
        self.rows = list()

    def add(self, name, price, date, required=False):
        self.rows.append(TableFeuilleRowStruct(name=name, price=price, date=date, required=required))
        self.header.price += price
        if required:
            self.header.priceOnlyRequired += price

    def isSingleton(self) -> bool:
        return len(self.rows) == 1

    def getSingleton(self) -> TableFeuilleRowStruct:
        return self.rows[0]

    @staticmethod
    def empty(id=None):
        return TableFeuilleBodyStruct(id=id, header=TableFeuilleRowStruct.empty(), rows=list())

    def to_json(self):
        return {
            "name": self.name,
            "header": self.header.to_json(),
            "rows": [x.to_json() for x in self.rows]
        }

@dataclass
class TableFeuilleCategoryStruct(object):
    category: str
    header: TableFeuilleRowStruct
    body: Dict[str, TableFeuilleBodyStruct]

    def add(self, category, name, price, date, required):
        if not name in self.body:
            self.body[name] = TableFeuilleBodyStruct(name=name)
        self.body[name].add(name, price, date=date, required=required)
        self.header.price += price
        if required:
            self.header.priceOnlyRequired += price

    def isSingleton(self) -> bool:
        k = self.body.keys()
        if len(k) == 1:
            kk = list(k)[0]
            return self.body[kk].isSingleton()
        return False

    def getSingleton(self) -> TableFeuilleBodyStruct:
        return self.body[list(self.body.keys())[0]]

    @staticmethod
    def empty(category=None):
        return TableFeuilleCategoryStruct(category=category, header=TableFeuilleRowStruct.empty(), body=dict())

@dataclass
class TableFeuilleStruct(object):
    items: Dict[str, TableFeuilleCategoryStruct]
    
    def add(self, category, name, price, date, required):
        if not category in self.items:
            self.items[category] = TableFeuilleCategoryStruct.empty(category=category)
        self.items[category].add(category=category, name=name, price=price, date=date, required=required)

    @staticmethod
    def empty():
        return TableFeuilleStruct(items=dict())

@dataclass
class FeuilleStruct(object):
    date: str
    factures: Dict[str, float]
    tickets: List[TicketDeCaisseStruct]

    def get(self, key, default=None):
        return getattr(self, key, default)

@dataclass
class DatabaseRowStruct(object):
    id: int
    shop: str
    localisation: str
    category: str
    itemArticleCategorie: str
    itemArticle: str
    itemNomArticle: str
    prix: float
    dateAchatStr: str = None
    group: str = None

    @staticmethod
    def from_itemArticle(ticket : TicketDeCaisseStruct, itemArticle : ItemArticleStruct):
        return DatabaseRowStruct(
            id=None, shop=ticket.shop.strip(), localisation=ticket.localisation.strip(), category=ticket.category.strip(),
            itemArticleCategorie=itemArticle.category.strip(), itemArticle=itemArticle.id.strip(), itemNomArticle=itemArticle.name.strip(),
            prix=itemArticle.prix, dateAchatStr=ticket.date, group=itemArticle.group
        )

    @staticmethod
    def from_list(id, v : List[Any]):
        return DatabaseRowStruct(
            id=int(id.strip()), shop=v[0].strip(), localisation=v[1].strip(), category=v[2].strip(), itemArticleCategorie=v[3].strip(),
             group=v[4].strip(), itemArticle=v[5].strip(), itemNomArticle=v[6].strip(), prix=float(v[7].strip()), dateAchatStr=v[8].strip(),
        )

    def toArticleObject(self):
        return ArticleStruct(
            remise=0.0,
            quantity=1,
            item=ItemArticleStruct(
                id=self.itemArticle,
                prix=self.prix,
                name=self.itemNomArticle,
                category=self.itemArticleCategorie,
                group=self.group
            )
        )

    def get(self, key, default=None):
        return getattr(self, key, default)

@dataclass
class DatabaseStruct(object):
    rows: List[DatabaseRowStruct]

    def __iter__(self):
        for row in self.rows:
            yield row

    def __len__(self):
        return len(self.rows)

    def to_json(self):
        return [x.to_json() for x in self.rows]

    def reverse(self):
        self.rows.reverse()
        return self

    @staticmethod
    def empty():
        return DatabaseStruct(rows=list())

    def isEmpty(self):
        return len(self) == 0
    
    def isSingleton(self):
        return len(self) == 1
