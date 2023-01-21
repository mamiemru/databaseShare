
import peewee
import dataclasses

from flask import Flask
from flask_restx import Api
from flask_restx import fields
from flask_restx import Resource
from flask_restx import reqparse
from flask_cors import CORS
from http import HTTPStatus

from service.ticketservice   import TicketService
from service.enumsService    import EnumsService
from service.feuillesService import FeuillesService

from datas.structs  import *
from datas.marshals import *

app = Flask(__name__)
api = Api(app)
CORS(app)

api.models[itemArticleMarshal.name] = itemArticleMarshal
api.models[articleMarshal.name] = articleMarshal
api.models[ticketDeCaisseMarshal.name] = ticketDeCaisseMarshal
api.models[enumMarshal.name] = enumMarshal
api.models[enumWithRequireFieldMarshal.name] = enumWithRequireFieldMarshal
api.models[feuilleFactureMarshal.name] = feuilleFactureMarshal
api.models[feuilleMarshal.name] = feuilleMarshal

ticketdecaisse_namespace         = api.namespace('ticketdecaisse')
ticketdecaisseCategory_namespace = api.namespace('ticketdecaisse/category')
itemArticleCategory_namespace    = api.namespace('ticketdecaisse/article/item/category')
itemArticleGroup_namespace       = api.namespace('ticketdecaisse/article/item/group')
feuille_namespace                = api.namespace('feuille')

@ticketdecaisse_namespace.route('/tdc/list/<int:last_n>')
class TicketDeCaisseListEndpoint(Resource):

    def get(self, last_n=None):
        return TicketService.list(last_n), 200

@ticketdecaisse_namespace.route('/tdc/<int:id>')
class TicketDeCaisseEndpoint(Resource):

    @api.marshal_with(ticketDeCaisseMarshal)
    def get(self, id : str):
        tdc : TicketDeCaisseStruct = TicketService.get(id)
        return tdc, HTTPStatus.OK if tdc else HTTPStatus.NOT_FOUND

    def delete(self, id):
        return TicketService.delete(id), 200
        
    @ticketdecaisse_namespace.expect(ticketDeCaisseMarshal, validate=False)
    @api.marshal_with(ticketDeCaisseMarshal)
    def put(self, id):
        tdc : TicketDeCaisseStruct = TicketDeCaisseStruct.from_dict(api.payload)
        
        try:
            tdc = TicketService.put(tdc, id)
        except peewee.IntegrityError:
            return None, HTTPStatus.CONFLICT
        
        if tdc:
            return tdc, HTTPStatus.OK
        
        return None, HTTPStatus.NOT_FOUND
    
@ticketdecaisse_namespace.route('/tdc')
class TicketDeCaisseNewEndpoint(Resource):

    @ticketdecaisse_namespace.expect(ticketDeCaisseMarshal, validate=False)
    @api.marshal_with(ticketDeCaisseMarshal)
    def post(self):
        tdc : TicketDeCaisseStruct = TicketDeCaisseStruct.from_dict(api.payload)
        
        try:
            tdc = TicketService.post(tdc)
        except peewee.IntegrityError:
            return None, HTTPStatus.CONFLICT
        
        if tdc:
            return tdc, HTTPStatus.CREATED
        
        return None, HTTPStatus.NOT_FOUND
    
@ticketdecaisseCategory_namespace.route('/list')
class TicketDeCaisseCategoryListEndpoint(Resource):
 
    @api.marshal_list_with(enumWithRequireFieldMarshal)
    def get(self):
        return  EnumsService.list_ticketdecaisse_category()
    
@ticketdecaisseCategory_namespace.route('/exists/<string:category>')
class TicketDeCaisseCategoryExistsEndpoint(Resource):

    @api.marshal_with(enumWithRequireFieldMarshal)
    def get(self, category : str):
        enu = EnumsService.get_ticketdecaisse_category(category=category.upper())

        if enu:
            return enu, HTTPStatus.OK
        
        return None, HTTPStatus.NOT_FOUND

@itemArticleCategory_namespace.route('/list')
class TicketDeCaisseCategoryListEndpoint(Resource):
 
    @api.marshal_list_with(enumWithRequireFieldMarshal)
    def get(self):
        return EnumsService.list_itemarticle_category()
    
@itemArticleCategory_namespace.route('/exists/<string:category>')
class TicketDeCaisseCategoryExistsEndpoint(Resource):

    @api.marshal_with(enumWithRequireFieldMarshal)
    def get(self, category : str):
        enu = EnumsService.get_itemarticle_category(category=category.upper())

        if enu:
            return enu, HTTPStatus.OK
        
        return None, HTTPStatus.NOT_FOUND
    
@itemArticleGroup_namespace.route('/list')
class TicketDeCaisseCategoryListEndpoint(Resource):
 
    @api.marshal_list_with(enumMarshal)
    def get(self):
        return EnumsService.list_itemarticle_group()
    
@itemArticleGroup_namespace.route('/exists/<string:group>')
class TicketDeCaisseCategoryExistsEndpoint(Resource):

    @api.marshal_with(enumMarshal)
    def get(self, group : str):
        enu = EnumsService.get_itemarticle_group(group=group.upper())

        if enu:
            return enu, HTTPStatus.OK
        
        return None, HTTPStatus.NOT_FOUND
    
@feuille_namespace.route('/list')
class TicketDeCaisseCategoryListEndpoint(Resource):
 
    def get(self):
        return FeuillesService.list()
    
@feuille_namespace.route('/<int:feuille_id>')
class FeuilleEndpoint(Resource):
    
    @api.marshal_with(feuilleMarshal)
    def get(self, feuille_id: int):
        f = FeuillesService.get(feuille_id)

        if f:
            return f, HTTPStatus.OK
        
        return None, HTTPStatus.NOT_FOUND

if __name__ == '__main__':
    app.run(debug=True)