
import os
import json

from typing import List

from datas.models import Feuille

from datas.structs import FeuilleStruct

class FeuillesRepository:

    @staticmethod
    def list() -> List[str]:
        return [data.date for data in Feuille.select().order_by(Feuille.date)]

    @staticmethod
    def get(date):
        return Feuille.get_or_none(Feuille.date==date)
    
    @staticmethod
    def post(filename, feuille : FeuilleStruct):
        f = Feuille(date=filename, factures=json.dumps(feuille.factures))
        return f if f.save() else None