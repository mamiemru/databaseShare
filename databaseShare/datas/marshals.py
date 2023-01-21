
from flask_restx import fields
from flask_restx import Model

from datas.structs import *

enumMarshal = Model(
    'Enum', {
        'group': fields.String
    }
)

enumWithRequireFieldMarshal = Model(
    'EnumWithRequireField', {
        'name': fields.String,
        'required': fields.Boolean(default=False)
    }
)

itemArticleMarshal = Model(
    'ItemArticle', { 
        'id': fields.Integer, 
        'ident': fields.String,
        'prix': fields.Float, 
        'name': fields.String, 
        'category': fields.String, 
        'group': fields.String 
    }
)

articleMarshal = Model(
    'Article', { 
        'remise': fields.Float, 
        'item': fields.Nested(itemArticleMarshal), 
        'quantity': fields.Integer 
    }
)

ticketDeCaisseMarshal = Model(
    'TicketDeCaisse', { 
        'id': fields.String,
        'shop': fields.String, 
        'localisation': fields.String, 
        'date': fields.DateTime(), 
        'category': fields.String,
        'articles': fields.List(fields.Nested(articleMarshal)) 
    }
)

feuilleFactureMarshal = Model(
    'FeuilleFactureMarshal', {
        'name': fields.String,
        'cost': fields.Float
    }
)

feuilleMarshal = Model(
    'FeuilleMarshal', {
        'date': fields.Integer(),
        'factures': fields.Wildcard(fields.Nested(feuilleFactureMarshal)),
        'tickets': fields.List(fields.String)
    }
)