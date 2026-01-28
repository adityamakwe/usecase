from ..models import User
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class UserService(BaseService):

    def authenticate(self, params):
        loginId = params.get("loginId", None)
        password = params.get("password", None)

        q = self.get_model().objects.filter()

        if (DataValidator.isNotNull(loginId)):
            q = q.filter(loginId=loginId)

        if (DataValidator.isNotNull(password)):
            q = q.filter(password=password)

        if (q.count() == 1):
            return q[0]
        else:
            return None

    def search(self, params):
        pageNo = ((params["pageNo"]) * self.pageSize)
        sql = "select * from sos_user where 1=1"
        val = params.get("firstName", None)
        val2 = params.get("loginId",None)
        val3 = params.get("roleId", None)
        print('=================',val3)
        if DataValidator.isNotNull(val):
            sql += " and firstName like '" + val + "%%'"
        if DataValidator.isNotNull(val2):
            sql += " and loginId like '" + val2 + "%%'"
        if DataValidator.isNotNull(val3):
            sql += " and roleId = " + val3

        sql += " limit %s, %s"
        print(sql)
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "firstName", "lastName", "loginId", "password", "confirmPassword",
                      "dob", "address", "gender", "mobileNumber", "roleId", "roleName")
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
        return User
