# from ..models import Role
from ..models import Role
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class RoleService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo']) * self.pageSize
        sql = 'select * from sos_role where 1=1'
        val = params.get('id', None)
        if (DataValidator.isNotNull(val)):
            sql += " and id = " + val
        sql += " limit %s, %s"
        print(sql)
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'name', 'description')
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
        return Role
