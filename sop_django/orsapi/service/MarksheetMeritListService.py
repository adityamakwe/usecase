from ..models import Marksheet
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class MarksheetMeritListService(BaseService):

    def search(self, params):
        sql = "select id, rollNumber, name, physics, chemistry, maths, (physics + chemistry + maths) as total, (physics + chemistry + maths) / 3 as percentage from sos_marksheet where physics >= 33 and chemistry >= 33 and maths >= 33 order by total desc limit 0,10"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        columnName = ("id", "rollNumber", "name", "physics", "chemistry", "maths", "total", "percentage")
        res = {
            "data": [],
        }
        params["index"] = ((params['pageNo'] - 1) * self.pageSize)
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Marksheet
