from ..models import Marksheet
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class MarksheetService(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"]) * self.pageSize
        sql = "select * from sos_marksheet where 1=1"
        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            sql += " and name like '" + val + "%%'"
        sql += " limit %s, %s"
        print('---------^^^^^^',sql)
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "rollNumber", "name", "physics", "chemistry", "maths")
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
