
import json

from datas.structs import FeuilleStruct

from service.dateService             import DateService
from repositories.ticketrepository   import TicketRepository
from repositories.feuillesRepository import FeuillesRepository

class FeuillesService():

    @staticmethod
    def list():
        return FeuillesRepository.list()

    @staticmethod
    def get(tiumestamp : int) -> FeuilleStruct:
        dateInf  = int(DateService.dateToMonthTimestamp(DateService.timestampToDate(tiumestamp)))
        dateSup  = int(DateService.dateToMonthTimestamp(DateService.dateAdd1Month(DateService.timestampToDate(tiumestamp))))
        
        feuille  = FeuillesRepository.get(tiumestamp)
        tdcs     = TicketRepository.get_tdcs_between_date(dateInf, dateSup)
        factures = [{'name': k, 'cost': v} for k,v in json.loads(feuille.factures).items()]
        return FeuilleStruct(date=feuille.date, factures=factures, tickets=[tdc.id for tdc in tdcs])
        

