from ..models import Subject
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class SubjectService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo']) * self.pageSize
        sql = "select * from sos_subject where 1=1"
        val = params.get("name", None)
        if (DataValidator.isNotNull(val)):
            sql += " and name like '" + val + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'name', 'description', 'courseId', 'courseName')
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
        return Subject
